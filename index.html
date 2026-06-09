# Amgen Inc. — Financial Intelligence Dashboard

A single-file, interactive dashboard over Amgen's (NASDAQ: **AMGN**) reported financials, covering the
**P&L, Balance Sheet and Free Cash Flow** with one-click drill-downs, a five-year trend layer,
a KPI library, statistical anomaly flags, product-level analysis, a working-capital / cash-conversion
cycle view, a valuation framework, an editable scenario model (base / bull / bear), and tailored
read-outs for **seven stakeholder personas** (Business CFO, Director — FP&A, Director of Business,
Treasurer, Strategy / Corp Dev, Market Leads, Equity Analyst).

Open `index.html` in any browser — no build step, no server, no dependencies beyond a CDN chart library.

---

## What's inside

| File | Purpose |
|------|---------|
| `index.html` | The dashboard. Self-contained (HTML + CSS + JS, data embedded). Just open it. |
| `data.json` | The full dataset (statements, KPIs, anomalies, products, WC, DuPont, debt wall, market, scenarios). |
| `data_annual.csv` | FY2021–FY2025 P&L / Balance Sheet / Cash Flow line items, for transparency. |
| `data_products_q1fy26.csv` | Q1 FY2026 product-level sales (US / ex-US / YoY). |
| `build_data.py` | Rebuilds `data.json` from the verified source figures; runs KPI, WC, DuPont, anomaly, debt-wall and scenario-preset engines. |
| `build_html.py` | Regenerates `index.html` by embedding `data.json` and rendering all stakeholder personas in Python. |

### Dashboard tabs (9)
- **Landing** — all three statements on one page, each as a compact table with **columns for FY21 → FY25 + Q1'26** and a **5-year sparkline** on the right of every line item. Click expandable rows to drill into composition (product mix, COGS split, intangibles, debt structure, inventory, capex).
- **5-Yr Trends** — revenue & net income, margin profile, FCF vs dividends, leverage, R&D intensity, balance-sheet composition.
- **KPI Library** — 12 KPIs from the P&L, balance sheet and FCF, each with a 5-year sparkline.
- **Working Capital + WoCA** — DSO / DIO / DPO / CCC trend, operating cycle, DuPont decomposition of ROE, plus a **WoCA peer-comparison block** (Pfizer, Merck, AbbVie, Lilly, BMY, Gilead, Regeneron, Vertex + industry median): CCC ranking chart, stacked components, full matrix with per-metric ranks and colour-coded efficiency tiers.
- **Anomalies** — statement-line z-score flags (FY21→FY25) and product-level flags (Q1'26).
- **Product Drill-down** — Q1 FY2026 sales by product, US/ex-US, and therapeutic area.
- **Valuation** — EV bridge, debt-maturity wall (indicative), stylised SOTP, dividend-discount sensitivity, and an EV/FCF sensitivity grid.
- **Scenarios** — *interactive* base / bull / bear presets with editable sliders (revenue growth, gross margin, R&D %, SG&A %, capex, tax rate). Live 3-year P&L projection.
- **Stakeholder Views** — **seven** lenses, all generated in Python from the live dataset: Business CFO, Director — FP&A, Director of Business (BU), Treasurer, Strategy / Corp Dev, Market Leads, Equity Analyst.

---

## Important scope note — "transactional level"

Public SEC filings disclose **line-item and product/geography detail, not journal entries or invoices.**
The anomaly engine therefore runs at the **deepest publicly available granularity** (statement line +
product), and this is clearly labelled throughout the dashboard. The same engine (`build_data.py` →
`detect()`) can be pointed at an **internal GL / ERP extract** to extend detection to true
journal-entry / transaction level — the method (z-score vs the line's own history) is identical.

## Anomaly method
For each line, the year-over-year % change is scored against its own 5-year distribution
(z-score). `|z| ≥ 1.7` ⇒ **HIGH**; other material moves ⇒ **WATCH**. Product flags compare each
product's Q1'26 growth against the portfolio mean growth.

---

## Architecture — Python is the source of truth

All financial data, KPI computations, anomaly detection **and stakeholder insight HTML** are generated
in Python (`build_data.py` → `build_html.py`). The output is a single self-contained `index.html`.
JavaScript handles only client-side interactivity (tab switching, chart rendering, drill-down toggles)
and contains **no hardcoded numbers or insight text** — those all come from Python at build time.

```
build_data.py   ← verified Amgen financials → data.json (KPIs, anomalies, products)
      ↓
build_html.py   ← reads data.json, computes personas in Python, injects into HTML template
      ↓
index.html      ← single self-contained dashboard (open in any browser)
```

```bash
python3 build_data.py     # regenerates data.json (+ prints anomalies & KPIs)
python3 build_html.py      # regenerates index.html with the embedded data
```

Edit the figures at the top of `build_data.py` (or swap in your own CSV/GL feed) and re-run both scripts.

---

## Push to GitHub

```bash
# 1. From this folder, initialise the repo
cd amgen-fin
git init
git add .
git commit -m "Amgen financial intelligence dashboard"

# 2. Create an empty repo on GitHub (no README), then connect it.
#    Replace YOUR-USERNAME and REPO-NAME.
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git
git push -u origin main
```

If you prefer the GitHub CLI:

```bash
gh repo create REPO-NAME --public --source=. --remote=origin --push
```

### Publish it as a live site (GitHub Pages)
1. On GitHub: **Settings → Pages**.
2. **Source:** *Deploy from a branch* → Branch **main** → Folder **/ (root)** → **Save**.
3. After ~1 minute your dashboard is live at:
   `https://YOUR-USERNAME.github.io/REPO-NAME/`

Because `index.html` is the entry file at the repo root, Pages serves it automatically.

---

## Sources
- Amgen Form **10-Q**, period ended **Mar 31, 2026** (SEC EDGAR).
- Amgen **Q4 / FY2025** results (Feb 3, 2026) and **Q4 / FY2024** results (Feb 4, 2025).
- Amgen **2023 Form 10-K** and Letter to Shareholders; FY2021–FY2022 reported actuals.

All figures in USD millions unless noted. Headline revenue, net income, EPS, FCF and balance-sheet
totals are reported actuals; a few FY2024–FY2025 expense sub-lines are modeled from reported growth
rates/margins where the granular line was not in the retrieved source text (flagged in the dashboard
footer). **Not investment advice** — Amgen's own filings govern.
