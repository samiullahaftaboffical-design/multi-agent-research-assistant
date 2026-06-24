import time
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env only if it exists (local dev). In production, env vars are set directly.
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
Model="gemini-2.5-flash-lite"

def call_agents(role,task_description,input_text=None):
    model=genai.GenerativeModel(Model)

    if input_text:
        prompt=f"""
You are a {role}.
{task_description}

Here is the information to work with:
---
{input_text}
---

Provide your output now. Be thorough and professional.
"""
    else:
        prompt = f"""
You are a {role}.
{task_description}

Provide your output now. Be thorough and professional.
"""
    time.sleep(2)
    response=model.generate_content(prompt)
    return response.text

def run_research(topic):
    print(f"\n{'='*60}")
    print(f"RESEARCH TOPIC: {topic}")
    print(f"{'='*60}\n")

    print("Agent 1 : Researcher is working")
    R_output=call_agents(role="Senior Research Specialist",
                         task_description=f"""
                         Research the topic: "{topic}".
Find and compile the most important information, key data points, trends, 
expert opinions, and credible facts. Be comprehensive. This research will 
be passed to an analyst who will extract the most critical insights.
""",
input_text=None
)
    print(" Researcher complete.\n")
    print("Agent 2 : Analyst is working ")
    A_output=call_agents(role="Senior Data Analyst",
                         task_description=f"""
Analyze the research findings. Extract the 5-7 most important insights.
Identify patterns, key statistics, important trends, and any contradictions.
Organize findings by importance. Be concise but thorough.
This will be passed to a writer who will create the final report.
""",
input_text=R_output
)
    print(" Analyst complete.\n")
    print("Agent 3 : Writer is working")
    W_output=call_agents(role="Professional Technical Writer",
                         task_description=f"""
Using the analyzed findings, write a complete research report.
Structure it with these sections:
1. Executive Summary (2-3 sentences)
2. Key Findings (numbered list with explanations)
3. Detailed Analysis (organized by theme)
4. Current Trends
5. Future Outlook
6. Conclusion

Use professional language. Include data points and statistics where available.
This draft will be reviewed by a critic for quality.
""",
input_text=A_output
)
    print(" Writer complete.\n")
    print("Agent 4 : Critic is working ")
    C_output=call_agents(role="Senior Editor and Quality Reviewer",
                         task_description=f"""
Review this research report critically. Check for:
- Missing important information or perspectives
- Weak or unsupported claims
- Unclear or poorly structured sections
- Lack of data or examples
- Any contradictions

Provide specific, actionable feedback. List what needs to be fixed or added.
This feedback will be used by an editor to improve the report.
""",
input_text=W_output
)
    print(" Critic complete.\n")
    print("Agent 5 : Editor is working")
    E_output=call_agents(role="Executive Editor",
                        task_description=f"""
Take the original draft report and the critic's feedback.
Produce a final, polished, professional research report.
Address all the critic's concerns. Fix any issues.
Add any missing information requested.
Ensure the report is publication-ready.

The final output must be the complete report. No notes, no comments about edits.
Just the final report.
""",
input_text=C_output
)
    print("Editor complete.\n")
    return E_output

if __name__ == "__main__":
    topic = "How is AI being used in cybersecurity in 2025?"
    report = run_research(topic)
    
    print(f"\n{'='*60}")
    print("FINAL RESEARCH REPORT")
    print(f"{'='*60}\n")
    print(report)
