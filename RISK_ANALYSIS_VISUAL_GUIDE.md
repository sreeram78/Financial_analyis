# Risk Analysis Tab — Visual Preview & Navigation Guide

## Tab Location
**Dashboard Tab 9** in the main navigation bar (between "Scenarios" and "Stakeholder Views")

---

## Tab Structure (Top to Bottom)

### 1. RISK PORTFOLIO OVERVIEW (KPI Cards)
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Total Risks     │  │  Current CCC     │  │  CCC Expansion   │  │  Mitigation      │
│                  │  │                  │  │  Risk            │  │  Opportunity     │
│  12 Risks        │  │  274 days        │  │                  │  │                  │
│  4 CRITICAL      │  │  vs. peer 183d   │  │  +20 to +100d    │  │  $1.2–$2.0B      │
│  3 HIGH          │  │                  │  │  Mild to severe  │  │  WC release      │
│  4 MEDIUM-LOW    │  │  ~91 days above  │  │  stress          │  │  over 24 months  │
│                  │  │  peer median     │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```
**Use:** High-level snapshot of risk portfolio and improvement opportunity.

---

### 2. RISK HEATMAP (Bubble Chart)
```
Severity (X-axis: Low → Critical)
│
$3.5B ┤     ●(Horizon)              ●(Reimbursement)    ● ●(Manufacturing)
      │                           
$3.0B ┤   ●(Economic)             
      │
$2.5B ┤                             ●(Concentration)
      │  ●(Biosimilar)  ●(Cyber)
$2.0B ┤                
      │     ●(Clinical)   ●(Litigation)
$1.5B ┤                          
      │
$1.0B ┤  ●(Tax) ●(Climate)
      │
      └─────────────────────────────────────────────
        Low      Medium       High     V.High  Critical
        
Legend: ● Red = CRITICAL  ● Gold = HIGH  ● Blue = MEDIUM  ● Gray = LOW
        (Bubble size = WC pressure in $M)
```
**Use:** Identify which risks are both severe AND high-impact. Focus on top-right quadrant.

**Insights:**
- 4 CRITICAL risks (red dots, top-right) deserve 80% of mitigation focus
- Horizon, Manufacturing, Reimbursement, Economic = the "Big 4"
- Budget/resource allocation should weight by position + size

---

### 3. WC COMPONENT IMPACT CHARTS (3 Horizontal Bars, Side-by-Side)

#### Chart A: DSO Extension by Risk (Horizontal Bar)
```
Risk #1: Reimbursement & Pricing       ━━━━━━━━━━━━━━━━━━━━━╡ +20 days
Risk #2: Economic Conditions & Solvency ━━━━━━━━━━━━━━━━━━━━━━━╡ +30 days
Risk #10: Concentration & Consolidation ━━━━━━━━━━━━━━━━━━━━╡ +20 days
Risk #6: Cybersecurity & IT             ━━━━━━━━━╡ +15 days
Risk #7: International Ops & FX         ━━━━━━━━╡ +15 days

(Color gradient: Red=CRITICAL, Gold=HIGH, Blue=MEDIUM)
```
**Key Takeaway:** Top 3 risks could extend DSO by 65+ days. Collections is a major lever.

#### Chart B: DIO Expansion by Risk (Horizontal Bar)
```
Risk #3: Horizon Integration             ━━━━━━━━━━━━━━━━━━━━━━━╡ +25 days
Risk #4: Manufacturing Disruptions       ━━━━━━━━━━━━━━━━━━━━━━━╡ +30 days
Risk #12: Climate & Natural Disasters    ━━━━━━━━━━━━━━━━━╡ +20 days
Risk #5: Biosimilar Competition          ━━━━━━━━━━━━┐ +20 days
Risk #8: Clinical Trial Delays           ━━━━━━━━━━┐ +15 days

(Color gradient: Red=CRITICAL, Gold=HIGH, Blue=MEDIUM)
```
**Key Takeaway:** Inventory is the #1 pain point. Horizon + Manufacturing alone = 55+ DIO days. Mitigation priority: dual-sourcing, JIT, safety stock optimization.

#### Chart C: DPO Pressure by Risk (Horizontal Bar)
```
Risk #2: Economic Conditions             ←━━━━━━━━━ -15 days (pressure)
Risk #3: Horizon Integration             ←━━━━━━━━━ -15 days
Risk #4: Manufacturing                  ←━━━━━━━━━ -15 days
Risk #12: Climate & Disaster             ←━━━━━━ -10 days
Risk #10: Concentration                  ←━━━━━━ -10 days

(Left/Red = DPO compression; Top risks are economically fragile)
```
**Key Takeaway:** Economic stress & supplier consolidation compress payables. Mitigation: supply-chain financing, term extension negotiation, diversification.

---

### 4. DETAILED RISK ASSESSMENT & MITIGATION (Expandable Risk Cards)

#### Filter Controls
```
[All Risks] [CRITICAL] [HIGH] [MEDIUM] [LOW]
```
**Use:** Click a severity filter to focus on specific risk tier.

#### Risk Card (Example: Risk #1)
```
┌─────────────────────────────────────────────────────────────────┐
│ Risk #1: Reimbursement & Pricing Pressures          [CRITICAL] │
│                                                                 │
│ Key Drivers:                                                    │
│ • Medicare price-setting (ENBREL -40% Jan 2026)               │
│ • State PDABs (8 enacted; 17 pending in 2024)                 │
│ • PBM consolidation (6 entities = 94% of Rx)                  │
│                                                                 │
│ WC Impact:      AR ↑↑↑ | Inv ↑ | AP ↓ | CF ↓↓↓              │
│ Financial:      $500M WC pressure                              │
│                                                                 │
│ ┌───────────────────────────────────────────────────────────┐ │
│ │ TOP 3 MITIGATIONS (of 5):                                 │ │
│ │ 1. Supply-chain financing for wholesalers (Q2 2025)       │ │
│ │    → -10 DSO days, $200-300M WC release                   │ │
│ │ 2. Quarterly rebate accrual updates (Monthly)             │ │
│ │    → Reduce disputes by 25-30%                            │ │
│ │ 3. Diversify payer base from top 6 PBMs (2025-2026)       │ │
│ │    → Reduce rebate pressure by 15-20%                     │ │
│ └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│ [See full risk list: risk_wc_analysis.md]                     │
└─────────────────────────────────────────────────────────────────┘
```

**Interaction:** Click "CRITICAL" filter to show only 4 CRITICAL risks. Click risk name to expand details (if expandable).

---

### 5. CCC SCENARIO MODELING (5-Scenario Bar Chart)

```
CCC (Days)
400 ├─────────────────────────────────────────────────────────────
    │
380 ├─────  ███████  Severe stress                                
    │       │       │ (7+ risks materialize)                    
360 ├─────  │       │                                             
    │       │       │                                             
340 ├─────  │       │  ███████  Moderate stress                  
    │       │       │  │       │ (5-6 risks)                     
320 ├─────  │       │  │       │                                  
    │       │       │  │       │  ███████  Mild stress            
310 ├─────  │       │  │       │  │       │ (3-4 risks)          
    │       │       │  │       │  │       │                      
290 ├─────  │       │  │       │  │       │  ███████   Base      
    │       │       │  │       │  │       │  │       │  (274d)   
270 ├─────  │       │  │       │  │       │  │       │           
    │       │       │  │       │  │       │  │       │           
250 ├─────  │       │  │       │  │       │  │       │  ███████
    │       │       │  │       │  │       │  │       │  │      │
230 ├─────  │       │  │       │  │       │  │       │  │      │ Mitigated (-30-50d)
    │       │       │  │       │  │       │  │       │  │      │
    └───────────────────────────────────────────────────────────
      Base  Mild    Mod.   Moderate  Severe          Mitigated
      274d  +30-50d  Stress
```

**Color coding:**
- 🔵 Base (274d) = Current state
- 🟡 Mild (310d) = 3-4 risks
- 🔴 Moderate (345d) = 5-6 risks
- 🔴🔴 Severe (380d) = 7+ risks (worst case)
- 🟢 Mitigated (230d) = Best case (all strategies executed)

**Interpretation:**
- Current 274d already concerning (91d above peers)
- Mild stress takes us to 310d (+36d, CCC becomes critical)
- Severe stress → 380d (business viability risk)
- Mitigation execution → 230d (beats peer benchmark by 47d)

---

### 6. MITIGATION POTENTIAL CHART (Stacked Bar)

```
WC Release ($M)
800 ├──────────────────────────────────────────────────────────────
    │
700 ├──────────────────────────────────────────────────────────────
    │
600 ├──  ████████  SCF & Collections      ████████  DPO Harmonization
    │   │        │                         │        │
500 ├──  │        │  ██████  Inventory    │        │  ██████  Dual-Source CMOs
    │   │        │  │      │  Optimization  │        │  │      │
400 ├──  │        │  │      │  ████████     │        │  │      │
    │   │        │  │      │  │          │  │        │  │      │
300 ├──  │        │  │      │  │          │  │        │  │      │  ██████
    │   │        │  │      │  │          │  │        │  │      │  │      │
200 ├──  │        │  │      │  │          │  │        │  │      │  │      │
    │   │        │  │        Mfg Diversif  │        │  │      │  │      │
100 ├──  │        │  │      │  │          │  │        │  │      │  │      │
    │   │        │  │      │  │          │  │        │  │      │  │      │
0   └───────────────────────────────────────────────────────────────
      Scen1    Scen2    Scen3        Scen4         Scen5
      
    🔵 Q1-Q2 (Quick Wins)     🟡 Q3-Q4 + 2026 (Mid/Long-term)
```

**Breakdown:**
- **SCF & Collections:** $200M (Q1-Q2) + $100M (later) = $300M total
- **Inventory Optimization:** $150M (Q1-Q2) + $400M (later) = $550M total
- **Mfg Diversification:** $100M (Q1-Q2) + $200M (later) = $300M total
- **DPO Harmonization:** $50M (Q1-Q2) + $150M (later) = $200M total
- **Dual-Source CMOs:** $75M (Q1-Q2) + $125M (later) = $200M total

**Total:** $1.2B–$2.0B WC release over 24 months

---

## NAVIGATION TIPS

### Quick Start (5 minutes)
1. Look at **KPI cards** (total risks, CCC gap, opportunity size)
2. Scan **Risk Heatmap** (identify Big 4 critical risks)
3. Review **CCC Scenarios** (understand downside & mitigation upside)

### Medium Dive (15 minutes)
4. Study **WC Component Impact charts** (which metrics are exposed?)
5. Skim **Risk Cards** (filtering by CRITICAL, then HIGH)
6. Review **Mitigation Potential** (where is $$ coming from?)

### Deep Dive (30+ minutes)
7. Read full **Detailed Risk Assessment** for each CRITICAL risk
8. Cross-reference with **Amgen_Risk_Factors_Working_Capital_Impact.md** for driver details
9. Plan **cross-functional mitigation** (who owns what? what's timeline?)

---

## Key Metrics at a Glance

| Metric | Current | Risk Range | Mitigated Target | Peer Benchmark |
|--------|---------|-----------|------------------|---|
| **CCC** | 274d | 310–380d | 220–240d | 183d |
| **DSO** | 94.9d | 115–125d | 75–85d | 50–60d |
| **DIO** | 249.7d | 270–300d | 200–220d | 150–180d |
| **DPO** | 70.2d | 55–60d | 85–105d | 60–70d |
| **Op Assets** | $45B | $48–52B | $38–40B | — |

---

## Sharing & Distribution

**For Print/PDF:**
- Use browser Print function (Ctrl+P or Cmd+P)
- Landscape orientation recommended for charts
- Charts render cleanly at 100% zoom

**For Presentations:**
- Screenshot individual cards/charts
- Share full dashboard as standalone HTML
- Include link to this preview guide for context

**For Discussion:**
- Print Risk Assessment Cards (one per page)
- Distribute to working groups (one risk per group)
- Assign mitigation ownership + timelines

---

## Q&A / Interpretation

**Q: Why is DIO so high (249.7 days)?**  
**A:** Amgen sells biologics & specialty pharma (oncology, immunology, rare disease). These products:
- Require higher safety stock due to specialized distribution (fewer wholesalers)
- Have small patient populations → batch production inefficiency
- Face supply chain concentration (Horizon's 30+ CMOs, Puerto Rico)
- Experience demand volatility (rare disease → low volume)
- Result in higher obsolescence risk
- Peer comparison (150–180 days) represents more commoditized, fast-moving products

**Mitigation:** Inventory optimization (JIT, consignment), dual-sourcing, demand planning.

---

**Q: Why is DSO so high (94.9 days)?**  
**A:** Reimbursement pressure creates cash-flow delays:
- Payer disputes (prior auth delays, rebate clawbacks)
- Discount/rebate calculations take 30–45 days to settle
- Wholesaler dynamics (consolidated buyers demand longer terms)
- Government payers (Medicare, Medicaid) = slower remittance

**Mitigation:** SCF for wholesalers, collections acceleration, rebate accuracy.

---

**Q: Is 274d CCC achievable?**  
**A:** Current CCC is 274d. Peer median is 183d. The 91-day gap is partly structural (specialty pharma is inherently higher WC intensity), but 30–50 days is recoverable through mitigation. Target of 220–240d is realistic.

---

**Q: When should this be implemented?**  
**A:** Phased over 24 months:
- **NOW (Q2 2025):** SCF, collections, rebate accuracy (fastest ROI)
- **Q3–Q4 2025:** Horizon ERP integration, manufacturing diversification, inventory optimization
- **2026–2027:** Structural changes (dual-sourcing, direct-to-pharmacy, disaster resilience)

**Quick wins (Q2-Q3) fund mid/long-term initiatives.**

---

**Document Last Updated:** June 9, 2025
