#!/usr/bin/env python3
"""
ARIS FigureSpec → SVG Renderer v2

Converts a FigureSpec JSON into publication-quality SVG for academic papers.
Deterministic: same spec = same SVG, every time.

Usage:
    python3 figure_renderer.py render spec.json [--output figures/output.svg] [--preview]
    python3 figure_renderer.py validate spec.json
    python3 figure_renderer.py schema
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString


# ============================================================
# Constants & Defaults
# ============================================================

ARROW_SIZE = 8
SELF_LOOP_RADIUS = 25

# Allowed values for sanitization
ALLOWED_SHAPES = {"rect", "rounded", "circle", "diamond", "ellipse"}
ALLOWED_STYLES = {"solid", "dashed", "dotted"}
ALLOWED_ANCHORS = {"start", "middle", "end"}
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

DEFAULT_STYLE = {
    "font_family": "Arial, Helvetica, sans-serif",
    "font_size": 14,
    "bg_color": "#FFFFFF",
    "palette": ["#2563EB", "#10B981", "#7C3AED", "#EA580C", "#C62828",
                "#0D47A1", "#1B5E20", "#4A148C", "#BF360C", "#37474F"],
}

DEFAULT_NODE = {
    "width": 120,
    "height": 50,
    "shape": "rounded",
    "text_color": "#333333",
    "font_size": None,
}

DEFAULT_EDGE = {
    "style": "solid",
    "color": "#555555",
    "thickness": 2,
    "curve": False,
}


# ============================================================
# Sanitization
# ============================================================

def sanitize_color(val: str, fallback: str = "#555555") -> str:
    """Validate hex color, reject anything else."""
    if isinstance(val, str) and HEX_COLOR_RE.match(val):
        return val
    return fallback


def sanitize_text(val: str) -> str:
    """Strip XML-illegal characters from text. ElementTree escapes &<>, but some code points are invalid in XML."""
    if not isinstance(val, str):
        return str(val)
    # Remove XML-illegal code points: C0 controls (except \t\n\r), C1, surrogates, noncharacters
    val = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", val)
    # Remove BMP noncharacters (U+FDD0-U+FDEF, U+FFFE-U+FFFF) and surrogates
    val = re.sub(r"[\ud800-\udfff\ufdd0-\ufdef\ufffe\uffff]", "", val)
    return val


def estimate_text_width(text: str, font_size: int) -> float:
    """Estimate text width in px. Rough but consistent."""
    # Average character width ≈ 0.6 × font_size for sans-serif
    # CJK characters ≈ 1.0 × font_size
    width = 0
    for ch in text:
        if ord(ch) > 0x2E80:  # CJK range
            width += font_size * 1.0
        else:
            width += font_size * 0.6
    return width


# ============================================================
# Color Utilities
# ============================================================

def lighten_color(hex_color: str, factor: float = 0.85) -> str:
    """Lighten a hex color for node fills."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


# ============================================================
# Geometry: Shape-Aware Edge Clipping
# ============================================================

def clip_to_shape(cx, cy, target_x, target_y, w, h, shape):
    """Clip a line from (cx,cy) toward (target_x,target_y) to the shape boundary."""
    dx = target_x - cx
    dy = target_y - cy
    if dx == 0 and dy == 0:
        return cx, cy - h / 2  # default: top

    if shape == "circle":
        # True circle: use max(w,h)/2 to match renderer
        r = max(w, h) / 2
        angle = math.atan2(dy, dx)
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    elif shape == "ellipse":
        # Ellipse clipping: x²/a² + y²/b² = 1
        a = w / 2
        b = h / 2
        angle = math.atan2(dy, dx)
        return cx + a * math.cos(angle), cy + b * math.sin(angle)

    elif shape == "diamond":
        # Diamond: |x/a| + |y/b| = 1
        a = w / 2
        b = h / 2
        angle = math.atan2(dy, dx)
        cos_a = abs(math.cos(angle))
        sin_a = abs(math.sin(angle))
        if cos_a * b + sin_a * a == 0:
            return cx, cy
        scale = (a * b) / (cos_a * b + sin_a * a)
        return cx + scale * math.cos(angle), cy + scale * math.sin(angle)

    else:
        # Rectangle clipping
        a = w / 2
        b = h / 2
        if abs(dx) * b > abs(dy) * a:
            scale = a / abs(dx)
        else:
            scale = b / abs(dy)
        return cx + dx * scale, cy + dy * scale


# ============================================================
# Validation
# ============================================================

def validate_spec(spec: dict) -> list:
    """Validate FigureSpec, return list of issues."""
    issues = []

    # Top-level must be a dict
    if not isinstance(spec, dict):
        return [f"CRITICAL: spec must be a JSON object, got {type(spec).__name__}"]

    # Structure validation — ensure top-level fields are correct types
    canvas = spec.get("canvas", {})
    if not isinstance(canvas, dict):
        issues.append("CRITICAL: 'canvas' must be a dict")
        canvas = {}
    st_raw = spec.get("style", {})
    if not isinstance(st_raw, dict):
        issues.append("CRITICAL: 'style' must be a dict")
    if not isinstance(spec.get("nodes", []), list):
        issues.append("CRITICAL: 'nodes' must be a list")
    if not isinstance(spec.get("edges", []), list):
        issues.append("CRITICAL: 'edges' must be a list")
    if not isinstance(spec.get("groups", []), list):
        issues.append("CRITICAL: 'groups' must be a list")
    if not isinstance(spec.get("labels", []), list):
        issues.append("CRITICAL: 'labels' must be a list")

    # Early return if structure is fundamentally broken
    if any(i.startswith("CRITICAL: '") for i in issues):
        return issues

    # Canvas validation
    for dim in ("width", "height"):
        val = canvas.get(dim)
        if val is not None:
            if isinstance(val, bool) or not isinstance(val, (int, float)):
                issues.append(f"CRITICAL: canvas.{dim} must be a number")
            elif val <= 0:
                issues.append(f"CRITICAL: canvas.{dim} must be positive")

    # Style validation
    st = spec.get("style", {})
    fs = st.get("font_size")
    if fs is not None and (isinstance(fs, bool) or not isinstance(fs, (int, float)) or fs <= 0):
        issues.append(f"CRITICAL: style.font_size must be a positive number")
    pal = st.get("palette")
    if pal is not None:
        if not isinstance(pal, list) or len(pal) == 0:
            issues.append(f"CRITICAL: style.palette must be a non-empty list of hex colors")
        else:
            for pi, pc in enumerate(pal):
                if not isinstance(pc, str) or not HEX_COLOR_RE.match(pc):
                    issues.append(f"CRITICAL: style.palette[{pi}] '{pc}' is not a valid hex color (#RRGGBB)")

    nodes = spec.get("nodes", [])
    if not nodes:
        issues.append("WARN: no nodes defined (labels/groups-only figure)")

    node_ids = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            issues.append(f"CRITICAL: nodes[{i}] must be a dict, got {type(node).__name__}")
            continue
        nid = node.get("id")
        if not nid:
            issues.append(f"CRITICAL: node[{i}] missing 'id'")
            continue
        if nid in node_ids:
            issues.append(f"CRITICAL: duplicate node id '{nid}'")
        node_ids.add(nid)
        if "label" not in node:
            issues.append(f"WARN: node '{nid}' missing 'label'")
        for coord in ("x", "y"):
            if coord not in node:
                issues.append(f"CRITICAL: node '{nid}' missing '{coord}'")
            elif isinstance(node[coord], bool) or not isinstance(node[coord], (int, float)):
                issues.append(f"CRITICAL: node '{nid}' {coord} must be a number, got {type(node[coord]).__name__}")
        for dim in ("width", "height"):
            val = node.get(dim)
            if val is not None and (isinstance(val, bool) or not isinstance(val, (int, float))):
                issues.append(f"CRITICAL: node '{nid}' {dim} must be a number, got {type(val).__name__}")
            elif val is not None and val <= 0:
                issues.append(f"CRITICAL: node '{nid}' {dim} must be positive ({val})")
        shape = node.get("shape", "rounded")
        if shape not in ALLOWED_SHAPES:
            issues.append(f"WARN: node '{nid}' unknown shape '{shape}', will use 'rounded'")

    for i, edge in enumerate(spec.get("edges", [])):
        if not isinstance(edge, dict):
            issues.append(f"CRITICAL: edges[{i}] must be a dict")
            continue
        src, dst = edge.get("from"), edge.get("to")
        if not src or not dst:
            issues.append(f"CRITICAL: edge[{i}] missing 'from' or 'to'")
        else:
            if src not in node_ids:
                issues.append(f"CRITICAL: edge[{i}] 'from' references unknown node '{src}'")
            if dst not in node_ids:
                issues.append(f"CRITICAL: edge[{i}] 'to' references unknown node '{dst}'")
        style = edge.get("style", "solid")
        if style not in ALLOWED_STYLES:
            issues.append(f"WARN: edge[{i}] unknown style '{style}', will use 'solid'")

    for i, group in enumerate(spec.get("groups", [])):
        if not isinstance(group, dict):
            issues.append(f"CRITICAL: groups[{i}] must be a dict")
            continue
        node_ids_list = group.get("node_ids", [])
        if not isinstance(node_ids_list, list):
            issues.append(f"WARN: group[{i}] node_ids must be a list")
            continue
        for nid in node_ids_list:
            if nid not in node_ids:
                issues.append(f"WARN: group[{i}] references unknown node '{nid}'")

    # Edge numeric validation
    for i, edge in enumerate(spec.get("edges", [])):
        for field in ("thickness",):
            val = edge.get(field)
            if val is not None and (isinstance(val, bool) or not isinstance(val, (int, float))):
                issues.append(f"WARN: edge[{i}] {field} must be a number")

    # Group numeric validation
    for i, group in enumerate(spec.get("groups", [])):
        val = group.get("padding")
        if val is not None and (isinstance(val, bool) or not isinstance(val, (int, float))):
            issues.append(f"WARN: group[{i}] padding must be a number")

    # Free label numeric + anchor validation
    for i, label in enumerate(spec.get("labels", [])):
        if not isinstance(label, dict):
            issues.append(f"CRITICAL: labels[{i}] must be a dict")
            continue
        anchor = label.get("anchor")
        if anchor and anchor not in ALLOWED_ANCHORS:
            issues.append(f"WARN: label[{i}] unknown anchor '{anchor}', will use 'middle'")
        for field in ("x", "y", "font_size"):
            val = label.get(field)
            if val is not None and (isinstance(val, bool) or not isinstance(val, (int, float))):
                issues.append(f"WARN: label[{i}] {field} must be a number")

    # Node font_size validation
    for node in nodes:
        if not isinstance(node, dict):
            continue
        nid = node.get("id", "?")
        nfs = node.get("font_size")
        if nfs is not None and (isinstance(nfs, bool) or not isinstance(nfs, (int, float)) or nfs <= 0):
            issues.append(f"WARN: node '{nid}' font_size must be a positive number")

    # Overlap detection (shape-aware bounding for circles)
    def _effective_bounds(n):
        w = n.get("width", DEFAULT_NODE["width"])
        h = n.get("height", DEFAULT_NODE["height"])
        if n.get("shape") == "circle":
            d = max(w, h)
            return d, d
        return w, h

    for i, a in enumerate(nodes):
        if not isinstance(a, dict):
            continue
        for j, b in enumerate(nodes):
            if i >= j or not isinstance(b, dict):
                continue
            ax, ay = a.get("x", 0), a.get("y", 0)
            bx, by = b.get("x", 0), b.get("y", 0)
            aw, ah = _effective_bounds(a)
            bw, bh = _effective_bounds(b)
            if (abs(ax - bx) < (aw + bw) / 2 - 5 and
                    abs(ay - by) < (ah + bh) / 2 - 5):
                issues.append(f"WARN: nodes '{a.get('id')}' and '{b.get('id')}' may overlap")

    return issues


# ============================================================
# SVG Renderer
# ============================================================

def render_svg(spec: dict) -> str:
    """Render FigureSpec to SVG string."""
    canvas = spec.get("canvas", {})
    width = canvas.get("width", 800)
    height = canvas.get("height", 400)
    style = {**DEFAULT_STYLE, **spec.get("style", {})}
    palette = style["palette"]
    base_fs = style["font_size"]

    svg = Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "viewBox": f"0 0 {width} {height}",
        "width": str(width),
        "height": str(height),
        "font-family": sanitize_text(style["font_family"]),
    })

    # Background
    SubElement(svg, "rect", {
        "width": str(width), "height": str(height),
        "fill": sanitize_color(style.get("bg_color", "#FFFFFF")),
    })

    # Defs: arrow markers
    defs = SubElement(svg, "defs")
    marker_colors = {"default": sanitize_color(DEFAULT_EDGE["color"])}
    for i, c in enumerate(palette):
        marker_colors[f"c{i}"] = sanitize_color(c)

    for name, color in marker_colors.items():
        marker = SubElement(defs, "marker", {
            "id": f"arrow-{name}",
            "markerWidth": str(ARROW_SIZE + 2),
            "markerHeight": str(ARROW_SIZE + 2),
            "refX": str(ARROW_SIZE),
            "refY": str(ARROW_SIZE // 2),
            "orient": "auto",
            "markerUnits": "strokeWidth",
        })
        SubElement(marker, "polygon", {
            "points": f"0 0, {ARROW_SIZE} {ARROW_SIZE // 2}, 0 {ARROW_SIZE}",
            "fill": color,
        })

    # Build node lookup with defaults applied
    node_map = {}
    for i, node in enumerate(spec.get("nodes", [])):
        n = {**DEFAULT_NODE, **node}
        n["fill"] = sanitize_color(n.get("fill") or lighten_color(palette[i % len(palette)]))
        n["stroke"] = sanitize_color(n.get("stroke") or palette[i % len(palette)])
        n["text_color"] = sanitize_color(n.get("text_color", DEFAULT_NODE["text_color"]))
        n["label"] = sanitize_text(n.get("label", ""))
        if n.get("sublabel"):
            n["sublabel"] = sanitize_text(n["sublabel"])
        if n.get("shape") not in ALLOWED_SHAPES:
            n["shape"] = "rounded"
        node_map[n["id"]] = n

    # --- Render groups (background layer) ---
    for group in spec.get("groups", []):
        gnodes = [node_map[nid] for nid in group.get("node_ids", []) if nid in node_map]
        if not gnodes:
            continue
        pad = group.get("padding", 20)
        def _node_extent(n):
            w, h = n["width"], n["height"]
            if n.get("shape") == "circle":
                d = max(w, h)
                return d, d
            return w, h

        min_x = min(n["x"] - _node_extent(n)[0] / 2 for n in gnodes) - pad
        min_y = min(n["y"] - _node_extent(n)[1] / 2 for n in gnodes) - pad
        max_x = max(n["x"] + _node_extent(n)[0] / 2 for n in gnodes) + pad
        max_y = max(n["y"] + _node_extent(n)[1] / 2 for n in gnodes) + pad

        SubElement(svg, "rect", {
            "x": f"{min_x:.1f}", "y": f"{min_y:.1f}",
            "width": f"{max_x - min_x:.1f}", "height": f"{max_y - min_y:.1f}",
            "fill": sanitize_color(group.get("fill", "#F5F5F5")),
            "stroke": sanitize_color(group.get("stroke", "#E0E0E0")),
            "stroke-width": "1", "rx": "8",
        })
        if group.get("label"):
            lbl = SubElement(svg, "text", {
                "x": f"{min_x + 8:.1f}", "y": f"{min_y + 16:.1f}",
                "font-size": str(base_fs - 2),
                "fill": "#999999", "font-weight": "bold",
            })
            lbl.text = sanitize_text(group["label"])

    # --- Render edges ---
    for edge in spec.get("edges", []):
        e = {**DEFAULT_EDGE, **edge}
        src = node_map.get(e.get("from"))
        dst = node_map.get(e.get("to"))
        if not src or not dst:
            continue

        color = sanitize_color(e["color"])
        e_style = e["style"] if e["style"] in ALLOWED_STYLES else "solid"

        # Find matching arrow marker
        marker_id = "arrow-default"
        for ci, pc in enumerate(palette):
            if color.lower() == pc.lower():
                marker_id = f"arrow-c{ci}"
                break

        # Dash pattern
        dash_map = {"solid": "", "dashed": "8,4", "dotted": "3,3"}
        dash = dash_map.get(e_style, "")

        # Self-loop (shape-aware: find top boundary)
        if src["id"] == dst["id"]:
            cx, cy = src["x"], src["y"]
            r = SELF_LOOP_RADIUS
            src_shape = src.get("shape", "rounded")
            # Find top anchor point based on shape
            top_x, top_y_pt = clip_to_shape(cx, cy, cx, cy - 100, src["width"], src["height"], src_shape)
            path_d = (f"M {top_x - 10},{top_y_pt} "
                      f"C {cx - r},{top_y_pt - r * 1.5} {cx + r},{top_y_pt - r * 1.5} {top_x + 10},{top_y_pt}")
            attrs = {
                "d": path_d,
                "stroke": color,
                "stroke-width": str(e["thickness"]),
                "fill": "none",
                "marker-end": f"url(#{marker_id})",
            }
            if dash:
                attrs["stroke-dasharray"] = dash
            SubElement(svg, "path", attrs)
        else:
            # Shape-aware clipping
            sx, sy = clip_to_shape(src["x"], src["y"], dst["x"], dst["y"],
                                   src["width"], src["height"], src.get("shape", "rounded"))
            dx, dy = clip_to_shape(dst["x"], dst["y"], src["x"], src["y"],
                                   dst["width"], dst["height"], dst.get("shape", "rounded"))

            if e.get("curve"):
                # Quadratic bezier with midpoint offset
                mx = (sx + dx) / 2
                my = (sy + dy) / 2
                # Offset perpendicular to the line
                length = math.sqrt((dx - sx) ** 2 + (dy - sy) ** 2) or 1
                offset = 30
                nx = -(dy - sy) / length * offset
                ny = (dx - sx) / length * offset
                path_d = f"M {sx:.1f},{sy:.1f} Q {mx + nx:.1f},{my + ny:.1f} {dx:.1f},{dy:.1f}"
            else:
                path_d = f"M {sx:.1f},{sy:.1f} L {dx:.1f},{dy:.1f}"

            attrs = {
                "d": path_d,
                "stroke": color,
                "stroke-width": str(e["thickness"]),
                "fill": "none",
                "marker-end": f"url(#{marker_id})",
            }
            if dash:
                attrs["stroke-dasharray"] = dash
            SubElement(svg, "path", attrs)

        # Edge label
        if e.get("label"):
            label_text = sanitize_text(e["label"])
            if src["id"] == dst["id"]:
                lx = src["x"]
                src_shape = src.get("shape", "rounded")
                _, top_pt = clip_to_shape(src["x"], src["y"], src["x"], src["y"] - 100,
                                          src["width"], src["height"], src_shape)
                ly = top_pt - SELF_LOOP_RADIUS * 1.2
            elif e.get("curve"):
                # Bezier midpoint at t=0.5: B(0.5) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2
                mx_ctrl = (sx + dx) / 2
                my_ctrl = (sy + dy) / 2
                length = math.sqrt((dx - sx) ** 2 + (dy - sy) ** 2) or 1
                offset = 30
                nx_ctrl = -(dy - sy) / length * offset
                ny_ctrl = (dx - sx) / length * offset
                qx, qy = mx_ctrl + nx_ctrl, my_ctrl + ny_ctrl
                lx = 0.25 * sx + 0.5 * qx + 0.25 * dx
                ly = 0.25 * sy + 0.5 * qy + 0.25 * dy - 8
            else:
                lx = (sx + dx) / 2
                ly = (sy + dy) / 2 - 8

            tw = estimate_text_width(label_text, base_fs - 3) + 8
            SubElement(svg, "rect", {
                "x": f"{lx - tw / 2:.1f}", "y": f"{ly - 10:.1f}",
                "width": f"{tw:.1f}", "height": "16",
                "fill": "#FFFFFF", "rx": "3", "opacity": "0.85",
            })
            lbl = SubElement(svg, "text", {
                "x": f"{lx:.1f}", "y": f"{ly + 2:.1f}",
                "font-size": str(base_fs - 3),
                "fill": "#777777", "text-anchor": "middle",
            })
            lbl.text = label_text

    # --- Render nodes ---
    for node in spec.get("nodes", []):
        n = node_map[node["id"]]
        x, y = n["x"], n["y"]
        w, h = n["width"], n["height"]
        left, top = x - w / 2, y - h / 2
        shape = n.get("shape", "rounded")
        fill = n["fill"]
        stroke = n["stroke"]

        if shape == "circle":
            r = max(w, h) / 2
            SubElement(svg, "circle", {
                "cx": f"{x:.1f}", "cy": f"{y:.1f}", "r": f"{r:.1f}",
                "fill": fill, "stroke": stroke, "stroke-width": "2",
            })
        elif shape == "ellipse":
            SubElement(svg, "ellipse", {
                "cx": f"{x:.1f}", "cy": f"{y:.1f}",
                "rx": f"{w / 2:.1f}", "ry": f"{h / 2:.1f}",
                "fill": fill, "stroke": stroke, "stroke-width": "2",
            })
        elif shape == "diamond":
            points = (f"{x:.1f},{top:.1f} {x + w / 2:.1f},{y:.1f} "
                      f"{x:.1f},{top + h:.1f} {x - w / 2:.1f},{y:.1f}")
            SubElement(svg, "polygon", {
                "points": points,
                "fill": fill, "stroke": stroke, "stroke-width": "2",
            })
        else:
            rx = "8" if shape == "rounded" else "0"
            SubElement(svg, "rect", {
                "x": f"{left:.1f}", "y": f"{top:.1f}",
                "width": f"{w:.1f}", "height": f"{h:.1f}",
                "fill": fill, "stroke": stroke,
                "stroke-width": "2", "rx": rx,
            })

        # Main label (supports \n for multi-line)
        fs = n.get("font_size") or base_fs
        # Handle multi-line: first replace literal \\n with \n, then split
        raw_label = n["label"].replace("\\n", "\n")
        label_lines = [line for line in raw_label.split("\n") if line]
        has_sub = bool(n.get("sublabel"))
        total_lines = len(label_lines) + (1 if has_sub else 0)
        line_height = fs + 2
        start_y = y - (total_lines - 1) * line_height / 2 + fs * 0.35

        for li, line in enumerate(label_lines):
            lbl = SubElement(svg, "text", {
                "x": f"{x:.1f}",
                "y": f"{start_y + li * line_height:.1f}",
                "font-size": str(fs),
                "fill": n["text_color"],
                "text-anchor": "middle",
                "font-weight": "bold",
            })
            lbl.text = line

        # Sublabel
        if has_sub:
            sub = SubElement(svg, "text", {
                "x": f"{x:.1f}",
                "y": f"{start_y + len(label_lines) * line_height:.1f}",
                "font-size": str(fs - 3),
                "fill": "#888888",
                "text-anchor": "middle",
            })
            sub.text = sanitize_text(n["sublabel"])

    # --- Free labels ---
    for label in spec.get("labels", []):
        anchor = label.get("anchor", "middle")
        if anchor not in ALLOWED_ANCHORS:
            anchor = "middle"
        lbl = SubElement(svg, "text", {
            "x": f"{label.get('x', 0):.1f}",
            "y": f"{label.get('y', 0):.1f}",
            "font-size": str(label.get("font_size", base_fs)),
            "fill": sanitize_color(label.get("color", "#555555")),
            "text-anchor": anchor,
        })
        lbl.text = sanitize_text(label.get("text", ""))

    # Pretty print
    raw = tostring(svg, encoding="unicode")
    pretty = parseString(raw).toprettyxml(indent="  ")
    # Remove xml declaration line
    lines = pretty.split("\n")
    return "\n".join(lines[1:])


# ============================================================
# PNG Preview
# ============================================================

def svg_to_png(svg_path: str, png_path: str) -> bool:
    """Convert SVG to PNG preview."""
    import subprocess

    # Try rsvg-convert
    try:
        result = subprocess.run(
            ["rsvg-convert", "-o", png_path, svg_path],
            capture_output=True, timeout=30
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try cairosvg
    try:
        os.environ.setdefault("DYLD_LIBRARY_PATH", "/opt/homebrew/lib")
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path)
        return True
    except Exception:
        pass

    print("Warning: could not convert SVG to PNG (install rsvg-convert or cairosvg)")
    return False


# ============================================================
# Schema (for documentation)
# ============================================================

SCHEMA_DOC = """\
FigureSpec JSON Schema:
{
  "title": "string — figure title (metadata only, not rendered)",
  "canvas": {"width": int, "height": int},
  "style": {
    "font_family": "CSS font string",
    "font_size": int (default 14),
    "bg_color": "#RRGGBB",
    "palette": ["#color1", "#color2", ...]
  },
  "nodes": [{
    "id": "string (required, unique)",
    "label": "string (required, supports \\\\n for multi-line)",
    "x": int (required, center x),
    "y": int (required, center y),
    "width": int (default 120),
    "height": int (default 50),
    "shape": "rounded | rect | circle | ellipse | diamond",
    "fill": "#RRGGBB (auto from palette)",
    "stroke": "#RRGGBB (auto from palette)",
    "text_color": "#RRGGBB (default #333333)",
    "font_size": int (override),
    "sublabel": "string (smaller text below label)"
  }],
  "edges": [{
    "from": "node_id (required)",
    "to": "node_id (required, same as from = self-loop)",
    "label": "string",
    "style": "solid | dashed | dotted",
    "color": "#RRGGBB (default #555555)",
    "thickness": int (default 2),
    "curve": bool (default false)
  }],
  "groups": [{
    "id": "string",
    "label": "string",
    "node_ids": ["id1", "id2"],
    "fill": "#RRGGBB",
    "stroke": "#RRGGBB",
    "padding": int (default 20)
  }],
  "labels": [{
    "text": "string",
    "x": int, "y": int,
    "font_size": int,
    "color": "#RRGGBB",
    "anchor": "start | middle | end"
  }]
}
"""


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="ARIS FigureSpec → SVG Renderer")
    subparsers = parser.add_subparsers(dest="command")

    p_render = subparsers.add_parser("render", help="Render FigureSpec JSON to SVG")
    p_render.add_argument("spec_file", help="FigureSpec JSON file")
    p_render.add_argument("--output", "-o", default=None, help="Output SVG path")
    p_render.add_argument("--preview", action="store_true", help="Also generate PNG preview")

    p_validate = subparsers.add_parser("validate", help="Validate FigureSpec JSON")
    p_validate.add_argument("spec_file", help="FigureSpec JSON file")

    subparsers.add_parser("schema", help="Print FigureSpec schema documentation")

    args = parser.parse_args()

    if args.command == "schema":
        print(SCHEMA_DOC)
        return

    if args.command == "validate":
        with open(args.spec_file, encoding="utf-8") as f:
            spec = json.load(f)
        issues = validate_spec(spec)
        critical = sum(1 for i in issues if i.startswith("CRITICAL"))
        if not issues:
            print("✅ FigureSpec is valid")
        else:
            for issue in issues:
                print(f"  {issue}")
            print(f"\n{len(issues)} issues ({critical} critical)")
        sys.exit(1 if critical else 0)

    if args.command == "render":
        with open(args.spec_file, encoding="utf-8") as f:
            spec = json.load(f)

        issues = validate_spec(spec)
        critical = [i for i in issues if i.startswith("CRITICAL")]
        if critical:
            print("❌ Cannot render — critical issues:")
            for i in critical:
                print(f"  {i}")
            sys.exit(1)

        if issues:
            print(f"⚠️  {len(issues)} warnings:")
            for i in issues:
                print(f"  {i}")

        svg_content = render_svg(spec)

        # Output path
        if args.output:
            output = args.output
        else:
            base = Path(args.spec_file).stem
            output = str(Path(args.spec_file).parent / f"{base}.svg")

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"✅ SVG written: {output}")

        if args.preview:
            png_path = str(Path(output).with_suffix(".png"))
            if svg_to_png(output, png_path):
                print(f"✅ PNG preview: {png_path}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
