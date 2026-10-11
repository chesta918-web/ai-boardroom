import copy
import json
import os
from pathlib import Path

from google import genai
from google.genai import types

from data import SECTORS

MODEL = "gemini-3.8-flash"  # check the current free model name in AI Studio
SCENARIOS = {
    "Base case": "Normal conditions. No surprises.",
    "Budget cut by 50%": "The AI budget was just cut by 50%. Expensive projects are at risk.",
    "New regulation hits": "A new data protection rule just hit this sector. Compliance work is needed.",
    "Data isn't ready": "The company's data turns out to be messy and scattered.",
}


def build_prompt(sector, scenario):
    items = []
    for i, uc in enumerate(SECTORS[sector], start=1):
        items.append({
            "id": i,
            "name": uc["name"],
            "value": uc["value"],
            "deploy": uc["deploy"],
            "trust": uc["trust"],
            "evidence": uc["why"],
            "source": uc["source"],
        })
    return f"""You are running a boardroom simulation about AI use cases in the {sector} sector in India.

Scenario: {scenario}

Use cases. Scores are 1 to 5. The "evidence" and "source" fields are the ONLY facts you may use:
{json.dumps(items, indent=2)}

Three speakers talk once each, in this order:
1. Optimist: argues for the most promising use cases.
2. Skeptic: raises risks, using the evidence.
3. CFO: challenges cost and payback.

Rules:
- Use ONLY the evidence given. If a point needs a fact you were not given, say "no evidence provided".
- Each message is 60 words or fewer.
- An adjustment changes one score. factor must be "value", "deploy" or "trust". delta is a whole number from -2 to 2. Give a short reason that cites the evidence.
- The verdict has a 2 sentence summary and one kill criteria line for EVERY use case, written like "Drop this if ...".

Return ONLY JSON in exactly this shape:
{{
  "turns": [
    {{"agent": "Optimist", "message": "...", "adjustments": [{{"id": 1, "factor": "deploy", "delta": -1, "reason": "..."}}]}},
    {{"agent": "Skeptic", "message": "...", "adjustments": []}},
    {{"agent": "CFO", "message": "...", "adjustments": []}}
  ],
  "verdict": {{"summary": "...", "kill_criteria": [{{"id": 1, "line": "Drop this if ..."}}]}}
}}"""


def call_gemini(prompt):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    return response.text


def validate(result, sector):
    n = len(SECTORS[sector])
    assert len(result["turns"]) == 3, "expected 3 turns"
    for turn in result["turns"]:
        clean = []
        for a in turn.get("adjustments", []):
            if a.get("id") in range(1, n + 1) and a.get("factor") in ("value", "deploy", "trust"):
                a["delta"] = max(-2, min(2, int(a.get("delta", 0))))
                clean.append(a)
        turn["adjustments"] = clean
    assert "summary" in result["verdict"], "no verdict summary"
    return result


CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)


def cache_file(sector, scenario_name):
    safe = (sector + "_" + scenario_name).lower()
    for ch in " '%":
        safe = safe.replace(ch, "_")
    return CACHE_DIR / (safe + ".json")


def demo_debate(sector):
    ucs = SECTORS[sector]
    best = max(range(len(ucs)), key=lambda i: ucs[i]["value"]) + 1
    hardest = min(range(len(ucs)), key=lambda i: ucs[i]["deploy"]) + 1
    return {
        "turns": [
            {"agent": "Optimist", "message": "Use case " + str(best) + " has the biggest payoff. Back it first.",
             "adjustments": [{"id": best, "factor": "value", "delta": 1, "reason": "demo"}]},
            {"agent": "Skeptic", "message": "Use case " + str(hardest) + " depends on data we may not have.",
             "adjustments": [{"id": hardest, "factor": "deploy", "delta": -1, "reason": "demo"}]},
            {"agent": "CFO", "message": "Show me the payback before we commit.", "adjustments": []},
        ],
        "verdict": {"summary": "DEMO MODE text. Set GEMINI_API_KEY to see the real debate.",
                    "kill_criteria": []},
    }


def run_debate(sector, scenario_name):
    """Returns (result, source, error). source is cache, live or demo."""
    path = cache_file(sector, scenario_name)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")), "cache", None
    if not os.environ.get("GEMINI_API_KEY"):
        return demo_debate(sector), "demo", "No GEMINI_API_KEY set in this terminal"
    try:
        prompt = build_prompt(sector, SCENARIOS[scenario_name])
        result = validate(json.loads(call_gemini(prompt)), sector)
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result, "live", None
    except Exception as e:
        return demo_debate(sector), "demo", str(e)


def apply_adjustments(sector, result, upto):
    """Copy of the use cases with the first `upto` turns of score changes applied."""
    ucs = copy.deepcopy(SECTORS[sector])
    for turn in result["turns"][:upto]:
        for a in turn["adjustments"]:
            uc = ucs[a["id"] - 1]
            uc[a["factor"]] = max(1, min(5, uc[a["factor"]] + a["delta"]))
    return ucs


if __name__ == "__main__":
    sector = "Healthcare"
    prompt = build_prompt(sector, SCENARIOS["Base case"])
    raw = call_gemini(prompt)
    try:
        result = validate(json.loads(raw), sector)
    except Exception as e:
        print("Bad answer from the AI:", e)
        print(raw)
    else:
        for turn in result["turns"]:
            print(turn["agent"] + ":", turn["message"])
            for a in turn["adjustments"]:
                print("    change:", a)
        print("Verdict:", result["verdict"]["summary"])
    for k in result["verdict"].get("kill_criteria", []):
        print("    kill", k["id"], k["line"])