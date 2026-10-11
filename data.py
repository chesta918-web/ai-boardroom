HEALTHCARE = [
    {
        "name": "Ambient scribing (OPD consults)",
        "value": 4, "deploy": 3, "trust": 3, "bain_wave": 1, "confidence": "Medium",
        "why": "A cardiac group drafts prescriptions in under a minute, about 90% needing no edits. But EMR is only about 35% and doctors must stay in the loop.",
        "source": "Bain & HealthQuad 2026, Fig 6 (p.8), case study (p.14). Register: F01, F12, F13",
    },
    {
        "name": "Claims and billing automation",
        "value": 4, "deploy": 4, "trust": 4, "bain_wave": 1, "confidence": "Medium",
        "why": "Claims-query automation cut discharge turnaround by 6 to 7 hours at one group. 57% of hospital executives are ready for NHCX. Payer-side AI adjudication adds some new risk.",
        "source": "Bain 2026 (p.14, Fig 6). Deloitte FY27 via Omnicuris. Register: F11, F17",
    },
    {
        "name": "Appointment scheduling and routing",
        "value": 3, "deploy": 5, "trust": 4, "bain_wave": 1, "confidence": "Medium",
        "why": "Scheduling infrastructure is already live at many players. Bain says chatbots and front-door tools show limited incremental value, and clinical triage meets resistance.",
        "source": "Bain 2026, Fig 6 (p.8) and p.9",
    },
    {
        "name": "Finance, HR and procurement automation",
        "value": 3, "deploy": 5, "trust": 5, "bain_wave": 1, "confidence": "Medium",
        "why": "83% of hospitals have ERP integrated. No clinical exposure and audit-friendly. Finance AI is live, HR results are mixed.",
        "source": "Bain 2026, Fig 6 (p.8). Deloitte FY27 via Omnicuris. Register: F19",
    },
    {
        "name": "Radiology and pathology AI",
        "value": 4, "deploy": 2, "trust": 2, "bain_wave": 2, "confidence": "Medium",
        "why": "Strong population-level value but per-patient ROI is unproven. PACS is not AI-ready, GPU cost is high, models are trained on Western data, and a doctor must certify.",
        "source": "Bain 2026, Fig 6 (p.8) and p.5. Register: F14",
    },
    {
        "name": "Post-discharge and chronic care monitoring",
        "value": 4, "deploy": 1, "trust": 2, "bain_wave": 3, "confidence": "Medium",
        "why": "Clear demand and flagged as whitespace, but EMR is too thin for longitudinal models and reimbursement and operating models are unclear.",
        "source": "Bain 2026, p.1 and Fig 6 (p.8). Register: F01, F03",
    },
]
LOGISTICS = [
    {
        "name": "Route optimization (road freight)",
        "value": 4, "deploy": 4, "trust": 5, "confidence": "Medium",
        "why": "Road is 41.7% of total logistics cost and fuel is 42.1% of road cost. Larger fleets usually have GPS and dispatch systems. Low risk.",
        "source": "NCAER-DPIIT 2025 via secondary sources. Register: L02, L03",
    },
    {
        "name": "Demand forecasting",
        "value": 3, "deploy": 3, "trust": 5, "confidence": "Low",
        "why": "Warehousing and storage is 24.8% of cost, so better forecasts help inventory and capacity. Needs clean order history, which many firms lack. Value score is my judgment.",
        "source": "NCAER-DPIIT 2025 via secondary. Register: L02",
    },
    {
        "name": "Empty-run reduction (load matching)",
        "value": 5, "deploy": 2, "trust": 3, "confidence": "Low",
        "why": "Empty runs are reported at about 40% of road freight, but that figure is unverified. Needs many fragmented fleets to share data.",
        "source": "FreightFox brief citing NCAER. Register: L09. Verify before use",
    },
    {
        "name": "Warehouse labour and slotting",
        "value": 2, "deploy": 3, "trust": 5, "confidence": "Low",
        "why": "Manpower is about 30% of warehouse cost, which is unverified. Operational use, low risk.",
        "source": "FreightFox brief citing NCAER. Register: L02, L10",
    },
    {
        "name": "SME freight benchmarking and consolidation",
        "value": 4, "deploy": 2, "trust": 4, "confidence": "Medium",
        "why": "SMEs spend about 16.9% of output on logistics versus 7.6% for large firms. But SMEs have thin data and little digital infrastructure.",
        "source": "NCAER-DPIIT 2025 via FreightFox. Register: L07",
    },
    {
        "name": "Rail and coastal mode-shift advisor",
        "value": 3, "deploy": 3, "trust": 4, "confidence": "Medium",
        "why": "Rail costs about Rs 1.96 per tonne-km, with three sources agreeing. Do not quote the road figure until you verify it, since sources conflict.",
        "source": "NCAER-DPIIT 2025 via secondary. Register: L04, L05",
    },
]
SECTORS = {"Healthcare": HEALTHCARE, "Logistics": LOGISTICS}
def compute_scores(uc):
    impact = uc["value"] * 2
    feasibility = uc["deploy"] + uc["trust"]
    return impact, feasibility
