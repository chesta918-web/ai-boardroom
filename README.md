# The AI Boardroom

Three AI agents (Optimist, Skeptic, CFO) debate which AI projects an Indian hospital or logistics firm should fund first. The impact vs feasibility matrix moves as they argue, and the debate ends with a ranked roadmap and a "drop this if..." rule for every project.

**Live app:** https://ai-boardroom-abdbhsto58wkyty4z6n5wp.streamlit.app

## What it does
1. Pick a sector (Healthcare or Logistics) and a scenario: Base case, Budget cut by 50%, New regulation hits, or Data isn't ready.
2. Three Gemini agents debate 6 use cases and propose score changes with reasons.
3. The matrix updates after each agent speaks.
4. A final roadmap ranks the use cases and gives a kill criterion for each.

## How it works
- **data.py**: 12 use cases with value, deploy and trust scores (1 to 5), an evidence line and a source for each.
- **Scoring**: impact = value x 2, feasibility = deploy + trust.
- **ai_debate.py**: builds the prompt, calls Gemini for strict JSON, validates every score change (known use case, known factor, max +/-2), caches the answer, and falls back to a visible demo mode if the API fails.
- **app.py**: Streamlit interface, Plotly matrix, chat bubbles, final roadmap.
- **cache/**: saved debates for every sector and scenario, so the public app loads instantly and uses no API quota.

## Evidence
Facts come from Bain and HealthQuad (2026 India healthcare AI report), Deloitte (via Omnicuris) and NCAER and DPIIT logistics cost studies. The AI is told to use only this evidence and to say "no evidence provided" when a fact is missing.

## Limits
- Scores are judgement calls informed by sources, not measurements.
- Some logistics figures come from secondary summaries and are flagged for verification.
- No cost or payback model yet.

## Run it yourself
pip install -r requirements.txt
set GEMINI_API_KEY (free key from Google AI Studio)
streamlit run app.py

Built with Python, Streamlit, Plotly and the Gemini API.
