# Building the Thematic Map

The thematic map is a visual representation of the analysis. It shows the themes, their sub-themes, and the relationships between them.

Braun and Clarke produce three maps over the analysis — initial (Phase 4), developed (Phase 5), and final (Phase 6). The final map goes into the write-up. The earlier maps are working documents; share them with the user during iteration if useful, but they do not have to be polished.

## What the final map should show

- **Overarching themes** (the main themes) — usually one shape per theme, centrally placed.
- **Sub-themes** — smaller shapes connected to their parent theme.
- **Relationships** between themes, where they exist — connecting lines, with optional labels.

What it should **not** show:

- Every code (the map is not a code map — Phase 3 produces that)
- Discarded candidate themes from earlier phases
- Counts, percentages, or other numeric clutter
- Decorative elements that do not carry analytic meaning

Braun and Clarke's Figure 4 is the simplest version: two overarching themes ("Vagina as asset" and "Vagina as liability"), each with three sub-themes radiating outward. No connecting lines between themes. Clean and readable.

## How to draw it — matplotlib approach

For a final map suitable for inclusion in the docx, use matplotlib. The output should be a PNG at 300 DPI (or higher) so it renders cleanly in print.

A simple radial layout works for most cases:

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# Style settings — keep monochrome or low-saturation
THEME_FACE = '#E8E8E8'
SUBTHEME_FACE = '#FFFFFF'
EDGE = '#333333'
FONT = {'family': 'serif', 'fontsize': 11}

def draw_theme(ax, x, y, label, width=2.6, height=1.0):
    """Draw an overarching theme as an ellipse."""
    ellipse = mpatches.Ellipse((x, y), width, height,
                                facecolor=THEME_FACE,
                                edgecolor=EDGE, linewidth=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, label, ha='center', va='center',
            fontweight='bold', **FONT)

def draw_subtheme(ax, x, y, label, width=2.0, height=0.6):
    """Draw a sub-theme as a rectangle with rounded corners."""
    rect = mpatches.FancyBboxPatch((x - width/2, y - height/2),
                                    width, height,
                                    boxstyle="round,pad=0.05",
                                    facecolor=SUBTHEME_FACE,
                                    edgecolor=EDGE, linewidth=1.0)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', **FONT)

def connect(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=EDGE, linewidth=0.8, zorder=0)

# Theme 1 — left side
draw_theme(ax, 3, 6, 'Theme name 1')
draw_subtheme(ax, 1, 4, 'Sub-theme 1a')
draw_subtheme(ax, 3, 3.5, 'Sub-theme 1b')
draw_subtheme(ax, 5, 4, 'Sub-theme 1c')
connect(ax, 3, 5.5, 1, 4.3)
connect(ax, 3, 5.5, 3, 3.8)
connect(ax, 3, 5.5, 5, 4.3)

# Theme 2 — right side
draw_theme(ax, 9, 6, 'Theme name 2')
draw_subtheme(ax, 7, 4, 'Sub-theme 2a')
draw_subtheme(ax, 9, 3.5, 'Sub-theme 2b')
draw_subtheme(ax, 11, 4, 'Sub-theme 2c')
connect(ax, 9, 5.5, 7, 4.3)
connect(ax, 9, 5.5, 9, 3.8)
connect(ax, 9, 5.5, 11, 4.3)

plt.tight_layout()
plt.savefig('phase6_final_map.png', dpi=300, bbox_inches='tight',
            facecolor='white')
plt.close()
```

Adapt the layout to the number of themes and sub-themes. For three or more themes, arrange them in a triangle or along the top of the figure rather than left-right.

## When themes have relationships

If overarching themes are related (e.g. one feeds into another, or they sit in tension), add a connecting line between them with a short label:

```python
ax.annotate('', xy=(7.7, 6), xytext=(4.3, 6),
            arrowprops=dict(arrowstyle='<->', color=EDGE, lw=1.0))
ax.text(6, 6.3, 'in tension with', ha='center', style='italic',
        fontsize=10, color=EDGE)
```

## Map captions in the write-up

The figure caption should be more than "Figure 1: Thematic map". Give the reader something useful:

> **Figure 1.** Final thematic map showing two overarching themes ("Deciding in the dark" and "Trusting the gut") and the six sub-themes that constitute them. Sub-themes within each overarching theme are presented in no particular order.

If there are relationships between themes, name them in the caption.

## When to save which version

| Phase | File name | What it shows |
|---|---|---|
| 4 | `phase4_initial_map.png` | Candidate themes, rough — may have many themes, some of which will be discarded |
| 5 | `phase5_refined_map.png` | Refined themes after Phase 5 review |
| 6 | `phase6_final_map.png` | The final map for the write-up |

Only the Phase 6 map needs to be polished. Phases 4 and 5 maps can be quick sketches — they exist to help the analyst think, not to be read by the user.

## Style notes

- Keep the map readable in greyscale. Many readers print papers in black and white.
- Avoid colour-coding by category if the meaning depends on the colour — readers with colour-vision differences may miss the distinction.
- Use one shape for themes and a different shape for sub-themes. This carries meaning even without colour.
- Keep labels short. Long labels make the map hard to read. If the theme name does not fit, the theme name may be too long for the write-up too.
