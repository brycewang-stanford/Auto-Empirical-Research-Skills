---
name: Checking ChEMBL for Structured SAR Data
description: Check if medicinal chemistry papers are in ChEMBL database to access curated bioactivity data
when_to_use: After finding relevant medicinal chemistry paper. When paper describes SAR data, compound series, or activity measurements. When evaluating papers with IC50, MIC, Ki, or other bioactivity values. Before attempting to parse activity tables from PDFs.
version: 1.0.0
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/kthorn/research-superpower
  项目名称: research-superpower
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Checking ChEMBL for Structured SAR Data

## Overview

ChEMBL is a manually curated database of ~99,000 medicinal chemistry papers with extracted, standardized bioactivity data. If a paper is in ChEMBL, you can access structured data without parsing PDFs.

**Core principle:** Check ChEMBL first for medicinal chemistry papers. Curated data is more reliable than table parsing.

## When to Use

Use this skill when:
- Paper describes medicinal chemistry / drug discovery
- Abstract mentions compound series, SAR, or activity data
- Paper has IC50, MIC, Ki, EC50, or other bioactivity measurements
- Before attempting to extract data from tables/figures
- Paper scored ≥ 7 in relevance evaluation

**When NOT to use:**
- Non-medicinal chemistry papers (cell biology, genomics, etc.)
- Papers without activity measurements
- Reviews without primary data
- Very recent papers (< 6 months, likely not curated yet)

## ChEMBL API Basics

**Base URL:** `https://www.ebi.ac.uk/chembl/api/data/`

**No authentication required**

**CRITICAL: ChEMBL can ONLY be queried by DOI, NOT by PMID**
- The API returns PMID in results, but does not accept it as a query parameter
- Always use DOI for lookups: `?doi=10.1234/example`
- PMID queries will return 0 results even if paper exists in ChEMBL

**Two-step process:**
1. Check if paper (by DOI) is in ChEMBL
2. If yes, retrieve bioactivity data

## Step 1: Check if Paper in ChEMBL

**Query by DOI (ONLY method that works):**
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/document.json?doi=DOI"
```

**⚠️ IMPORTANT: Must use DOI, not PMID**
```bash
# ✅ CORRECT - Use DOI
doi="10.1021/jm401507s"
curl -s "https://www.ebi.ac.uk/chembl/api/data/document.json?doi=$doi"

# ❌ WRONG - PMID won't work (will return 0 results)
pmid="24446688"
curl -s "https://www.ebi.ac.uk/chembl/api/data/document.json?pubmed_id=$pmid"  # Does NOT work!
```

**If you only have PMID:** Fetch DOI from PubMed first, then query ChEMBL with the DOI.

**Response structure:**
```json
{
  "documents": [
    {
      "document_chembl_id": "CHEMBL3120156",
      "doi": "10.1021/jm401507s",
      "title": "Discovery and development of simeprevir (TMC435), a HCV NS3/4A protease inhibitor.",
      "abstract": "Hepatitis C virus is a blood-borne infection...",
      "pubmed_id": 24446688,
      "journal": "J Med Chem",
      "year": 2014,
      "doc_type": "PUBLICATION"
    }
  ],
  "page_meta": {
    "total_count": 1
  }
}
```

**Key fields:**
- `document_chembl_id` - Use this to retrieve activity data
- `doc_type` - "PUBLICATION" (from literature) or "DATASET" (deposited)
- `pubmed_id` - PMID is in the response, but cannot be used to query ChEMBL
- If `total_count` = 0, paper not in ChEMBL

**Parse response:**
```bash
response=$(curl -s "https://www.ebi.ac.uk/chembl/api/data/document.json?doi=$doi")

if [ $(echo "$response" | jq -r '.page_meta.total_count') -gt 0 ]; then
  chembl_id=$(echo "$response" | jq -r '.documents[0].document_chembl_id')
  echo "✓ Found in ChEMBL: $chembl_id"
else
  echo "✗ Not in ChEMBL"
fi
```

## Step 2: Get Activity Data Count

**Query activity endpoint:**
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=CHEMBL3120156&limit=1"
```

**Extract total count:**
```bash
activity_url="https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=$chembl_id&limit=1"
activity_count=$(curl -s "$activity_url" | jq -r '.page_meta.total_count')

echo "→ $activity_count bioactivity data points"
```

## Step 3: Report to User and Update Summary

**Report immediately:**
```
📄 [15/127] Screening: "Discovery and development of simeprevir"
   Abstract score: 9 → Fetching full text...
   ✓ ChEMBL: CHEMBL3120156 (101 activity data points)
   → IC50 data for HCV NS3 protease inhibitors available
```

**Add to SUMMARY.md:**
```markdown
### [Discovery and development of simeprevir (TMC435), a HCV NS3/4A protease inhibitor](https://doi.org/10.1021/jm401507s) (Score: 9)

**DOI:** [10.1021/jm401507s](https://doi.org/10.1021/jm401507s)
**PMID:** [24446688](https://pubmed.ncbi.nlm.nih.gov/24446688/)
**ChEMBL:** [CHEMBL3120156](https://www.ebi.ac.uk/chembl/document_report_card/CHEMBL3120156/) (101 data points)

**Key Findings:**
- IC50 data for HCV NS3/4A protease inhibitors (from ChEMBL)
- Lead compound simeprevir (TMC435) approved for HCV treatment
- Structures and full activity data: [ChEMBL API](https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=CHEMBL3120156)

**ChEMBL Activity Summary:**
- IC50 values for HCV NS3/4A protease
- PK parameters (AUC, Cmax, clearance)
- DMPK assays (metabolic stability, permeability)
```

**Always include ChEMBL status:**
- If found: Add ChEMBL ID with link and data point count
- If not found: Note "Not in ChEMBL" (still valuable information)

## Step 4: Update Tracking Files

**Add to papers-reviewed.json:**
```json
{
  "10.1021/jm401507s": {
    "pmid": "24446688",
    "status": "relevant",
    "score": 9,
    "chembl_id": "CHEMBL3120156",
    "chembl_activities": 101,
    "has_structured_data": true
  }
}
```

## Optional: Extract Structured Data

**For papers with rich ChEMBL data (>20 activities), consider extracting:**

```bash
# Get all IC50 data
curl -s "https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=CHEMBL3120156&standard_type=IC50&limit=100" > chembl_data.json

# Summary statistics
jq '[.activities[] | .standard_value | tonumber] | "Min: \(min), Max: \(max), Count: \(length)"' chembl_data.json
```

**Report to user:**
```
📊 ChEMBL data extracted:
   - IC50 values for HCV NS3/4A protease
   - All structures downloaded
   - Data saved to: chembl_CHEMBL3120156_ic50.json
```

## Integration with Other Skills

**During evaluating-paper-relevance workflow:**

1. **After abstract screening (score ≥7)**
2. **Before deep dive into full text**
3. **Check ChEMBL** using this skill
4. **If found:**
   - Note ChEMBL ID in SUMMARY.md
   - Extract activity data (faster than PDF parsing)
   - Still fetch full text for methods, discussion, context
5. **If not found:**
   - Proceed with normal PDF evaluation
   - Parse tables manually if needed

**Workflow integration point:**
```
Stage 2: Deep Dive
├─ 1. Fetch Full Text (PMC → DOI → Unpaywall)
├─ 1.5. Check ChEMBL ← ADD THIS STEP
│   ├─ Query by DOI
│   ├─ If found: note ChEMBL ID + activity count
│   └─ Report to user
├─ 2. Scan for Relevant Content
└─ 3. Extract Findings
```

## Common Activity Types in ChEMBL

| Type | Description | Units |
|------|-------------|-------|
| IC50 | Half-maximal inhibitory concentration | nM, µM |
| MIC | Minimum inhibitory concentration | µg/mL, nM |
| Ki | Inhibition constant | nM, µM |
| EC50 | Half-maximal effective concentration | nM, µM |
| Kd | Dissociation constant | nM, µM |
| Potency | General potency measurement | Various |

**Filter by activity type:**
```bash
curl "https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=ID&standard_type=MIC"
```

## ChEMBL Coverage

**~99,000 documents** (as of 2025)

**Well represented:**
- Medicinal chemistry papers
- SAR studies with compound series
- Lead optimization campaigns
- Papers in major journals (J Med Chem, Bioorg Med Chem, Eur J Med Chem, etc.)

**Poorly represented:**
- Very recent papers (6-12 month curation lag)
- Papers without extractable structures/activities
- Non-drug-discovery research
- Purely mechanistic studies

**Typical hit rate:**
- ~30-40% of medicinal chemistry papers
- Higher for SAR-focused journals

## Advantages of ChEMBL Data

**vs. PDF table parsing:**
- ✓ Structures already extracted (SMILES format)
- ✓ Units standardized (all IC50s in nM)
- ✓ Values validated and curated
- ✓ Machine-readable JSON
- ✓ No OCR errors
- ✓ Linked to assay protocols
- ✓ Queryable (filter by activity range, target, etc.)

**When to still use PDF:**
- Full experimental procedures
- Synthesis routes
- Papers not in ChEMBL
- Very recent papers
- Context and interpretation

## Progress Reporting

**CRITICAL: Report ChEMBL check for every relevant paper**

**Example workflow report:**
```
📄 [15/50] Screening: "Novel MmpL3 inhibitors..."
   Abstract score: 8 → Checking ChEMBL...
   ✓ ChEMBL: CHEMBL3456789 (34 data points)
   → Fetching full text...
   → Added to SUMMARY.md with ChEMBL link
```

**For papers not in ChEMBL:**
```
📄 [16/50] Screening: "Another paper..."
   Abstract score: 9 → Checking ChEMBL...
   ✗ Not in ChEMBL (likely too recent or review paper)
   → Fetching full text via Unpaywall...
```

## Helper Script Pattern

For research sessions with many medicinal chemistry papers:

**Create `check_chembl.py`:**
```python
#!/usr/bin/env python3
import requests
import json
import sys

def check_chembl(doi):
    """Check if DOI is in ChEMBL and return summary

    IMPORTANT: Must use DOI, not PMID. ChEMBL API does not accept PMID queries.
    """

    # Query document (ONLY works with DOI)
    doc_url = f"https://www.ebi.ac.uk/chembl/api/data/document.json?doi={doi}"
    try:
        doc_response = requests.get(doc_url, timeout=10).json()
    except:
        return None

    # Check if found
    if doc_response.get('page_meta', {}).get('total_count', 0) == 0:
        return {'in_chembl': False}

    doc = doc_response['documents'][0]
    chembl_id = doc['document_chembl_id']

    # Get activity count
    act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id={chembl_id}&limit=1"
    try:
        act_response = requests.get(act_url, timeout=10).json()
        activity_count = act_response.get('page_meta', {}).get('total_count', 0)
    except:
        activity_count = 0

    return {
        'in_chembl': True,
        'chembl_id': chembl_id,
        'activity_count': activity_count,
        'doc_type': doc.get('doc_type'),
        'title': doc.get('title')
    }

if __name__ == "__main__":
    doi = sys.argv[1]
    result = check_chembl(doi)

    if result and result['in_chembl']:
        print(f"✓ {result['chembl_id']} ({result['activity_count']} activities)")
    else:
        print("✗ Not in ChEMBL")
```

**Usage:**
```bash
python3 check_chembl.py "10.1021/jm401507s"
# Output: ✓ CHEMBL3120156 (101 activities)
```

## Common Mistakes

**Querying by PMID:** Using PMID instead of DOI → Always returns 0 results, ChEMBL only accepts DOI queries
**Skipping ChEMBL check:** Not checking medicinal chemistry papers → Missing structured data that's already extracted
**Checking non-medchem papers:** Checking genomics/cell biology papers → Wasting time, won't be in ChEMBL
**Not reporting status:** Silent ChEMBL checks → User can't see what's happening
**Not adding to SUMMARY.md:** Forgetting to include ChEMBL ID → Harder for user to access data later
**Only using ChEMBL:** Not fetching full text when paper in ChEMBL → Missing context, methods, discussion
**Parsing PDFs when in ChEMBL:** Manually extracting tables when structured data available → Wasting time and introducing errors

## Quick Reference

| Task | Command |
|------|---------|
| Check if DOI in ChEMBL | `curl "https://www.ebi.ac.uk/chembl/api/data/document.json?doi=DOI"` |
| Get activity count | `curl "https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=ID&limit=1"` |
| Get all activities | `curl "https://www.ebi.ac.uk/chembl/api/data/activity.json?document_chembl_id=ID&limit=1000"` |
| Filter by activity type | `curl "...activity.json?document_chembl_id=ID&standard_type=MIC"` |
| ChEMBL paper page | `https://www.ebi.ac.uk/chembl/document_report_card/CHEMBL_ID/` |

## Permissions

Add to `.claude/settings.local.json.template`:
```json
"Bash(curl*https://www.ebi.ac.uk/chembl/api/data/*)",
"WebFetch(domain:www.ebi.ac.uk)"
```

## Success Criteria

ChEMBL check successful when:
- Every medicinal chemistry paper (score ≥7) checked
- ChEMBL status reported to user immediately
- ChEMBL ID added to SUMMARY.md (if found)
- Activity count noted in summary
- papers-reviewed.json updated with ChEMBL status

## Next Steps

After checking ChEMBL:
- If found: Consider extracting structured data for highly relevant papers (≥9)
- Continue with full text evaluation for context
- For papers not in ChEMBL: Proceed with normal PDF/table parsing
- Update SUMMARY.md with all findings

## Resources

- **Full Documentation:** See `docs/CHEMBL_INTEGRATION.md`
- **ChEMBL API Docs:** https://chembl.gitbook.io/chembl-interface-documentation/
- **ChEMBL Interface:** https://www.ebi.ac.uk/chembl/
