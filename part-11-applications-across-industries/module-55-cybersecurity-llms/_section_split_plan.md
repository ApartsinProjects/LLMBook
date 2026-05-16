# Chapter 55 (Cybersecurity) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-55.7.html` - **legacy survivor titled "Section 55.5: Cybersecurity & LLMs", actually old Ch 27.5 content**)
- `index.html` body: **1,698 words** with 5 modern h2 sections (40.1-40.5)
- Pattern: **Hybrid: inline new content + legacy file to retire**
- Effort: ~3-4 hours

## Plan: split index + retire 55.7

### New sections from index.html

| New file              | Title                                                | Source h2 |
| --------------------- | ---------------------------------------------------- | --------- |
| `section-55.1.html`   | Defensive (Blue Team) Use Cases                      | 40.1      |
| `section-55.2.html`   | Offensive (Red Team) Use Cases                       | 40.2      |
| `section-55.3.html`   | LLM-Specific Attack Surface                          | 40.3      |
| `section-55.4.html`   | Architectural Pattern: Trust Boundaries              | 40.4      |
| `section-55.5.html`   | Where to Read More                                   | 40.5      |

Rich h3 coverage (SOC triage, phishing analysis, code review, postmortems, threat intel, detection-as-code, phishing gen, vuln research, malware adaptation) distributes naturally into 55.1 (blue) and 55.2 (red).

### Fate of `section-55.7.html`
Legacy `27.5.x` (Threat Intelligence, Log Analysis, Vuln Detection, Adversarial Uses) - all subsumed by new 40.x material. Likely safe to **delete** outright; spot-check for unique citations to migrate.

## Steps
1. Extract 5 new sections from index.
2. Renumber `40.x` -> `55.x`.
3. Migrate any unique citations/examples from 55.7 -> 55.1/55.2/55.3.
4. Delete `section-55.7.html`.
5. Replace index body with TOC; update `book_structure.yaml`.
