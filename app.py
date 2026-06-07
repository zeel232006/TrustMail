from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import json
import re

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    email = data.get("email", "").strip()

    if not email:
        return jsonify({"error": "No email provided."}), 400

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$", email):
        return jsonify({"error": "Invalid email format."}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "API key not configured on server."}), 500

    prompt = f"""You are TrustMail, a strict email security analyst focused on protecting job seekers from scams.

Analyze this email address: "{email}"

STRICT RULES you must follow:
- Well-known corporate domains (tcs.com, infosys.com, wipro.com, accenture.com, google.com, microsoft.com, amazon.com, flipkart.com, edunetfoundation.org etc.) → score HIGH (75-100)
- Free email providers (gmail.com, yahoo.com, hotmail.com, outlook.com) used for recruitment → score LOW (20-40), always SUSPICIOUS
- Domains mimicking companies (gmail-jobs.com, tcs-hr.com, infosys-recruitment.net) → score VERY LOW (0-20), always DANGEROUS
- Unknown/unrecognizable domains with no clear company identity (like tallymet.com, quickhire.net, jobszone.in) → score LOW (15-35), mark SUSPICIOUS or DANGEROUS
- If the domain cannot be verified as a known legitimate organization, ALWAYS lean toward suspicious
- A real company recruiter uses their official company domain — unknown domains are a red flag

Return ONLY valid JSON, no markdown:
{{
  "trustScore": <number 0-100>,
  "verdict": "<safe|suspicious|dangerous>",
  "verdictSummary": "<one sentence summary>",
  "format": {{
    "status": "<pass|fail>",
    "result": "<brief result>",
    "detail": "<explanation>"
  }},
  "domain": {{
    "status": "<pass|warn|fail>",
    "result": "<brief result>",
    "detail": "<explanation about domain legitimacy>"
  }},
  "mx": {{
    "status": "<pass|warn|fail>",
    "result": "<brief result>",
    "detail": "<explanation about mail servers>"
  }},
  "spam": {{
    "status": "<pass|warn|fail>",
    "result": "<brief result>",
    "detail": "<explanation about spam risk>"
  }},
  "aiAnalysis": "<3-4 sentences. Be skeptical of unknown domains. Warn job seekers clearly if this looks untrustworthy.>",
  "flags": [
    {{ "label": "<signal text>", "type": "<red|yellow|green>" }}
  ]
}}

Provide 3-6 flags. Be strict — it is better to over-warn than under-warn when job seekers' safety is at risk."""
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        clean = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 502

if __name__ == "__main__":
    app.run(debug=True)