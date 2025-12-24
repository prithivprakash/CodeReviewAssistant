from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from typing import Optional
from python_analyzer import analyzeCode

load_dotenv()



from llm_factory import get_llm

app = FastAPI(title="AI Code Review Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # allows OPTIONS, POST, etc.
    allow_headers=["*"],
)


ALLOWED_MODES = {"review", "explain", "generate", "sql"}


class askRequest(BaseModel):
    provider: Optional[str] = None
    api_key: Optional[str] = None
    mode: str
    language: str
    input: str



class askResponse(BaseModel):
    response : str


def build_prompt(mode: str, language: str, user_input: str, analysis : dict | None = None) -> str:
    mode = mode.lower()

    analysis_block = ""
    if analysis:
        analysis_block = f"""
### STATIC ANALYSIS (FACTUAL)
The following observations are derived from static code analysis and are guaranteed facts:
- Loop count: {analysis.get("loop_count")}
- Nested loops detected: {analysis.get("has_nested_loops")}
- Uses recursion: {analysis.get("uses_recursion")}
- Uses global variables: {analysis.get("uses_global")}
- Uses eval/exec: {analysis.get("uses_eval")}
- Maximum function length: {analysis.get("max_function_length")}
"""

    if mode == "review":
        return f"""
You are a senior software engineer performing a professional code review.

IMPORTANT RULES:
- Do NOT guess the algorithm name unless it is explicitly implemented.
- Do NOT invent bugs.
- Separate proven facts from interpretations.
- Do NOT label design tradeoffs as bugs.
- If the code is correct and reasonable for its purpose, explicitly say:
  "No critical issues found."

{analysis_block}

Return your response STRICTLY in the following format:

### INTENT
Describe what the code is trying to achieve in plain terms.

### FACTUAL OBSERVATIONS
List only things that can be proven directly from the code structure
(e.g., loops, recursion, global state, control flow).

### INTERPRETATION (LOW CONFIDENCE)
Reasoned observations that are NOT guaranteed.
Clearly state uncertainty using phrases like:
"may", "appears to", "cannot be determined with certainty".

### ISSUES
Classify findings into:
- Critical bug
- Potential improvement
- Design tradeoff
- Performance consideration

If none apply, state:
"No critical issues found."

### COMPLEXITY
Discuss time and space complexity.
Base claims on static analysis when available.
Avoid overclaiming.

### FIX
Provide improvements ONLY if issues exist.
If no fix is required, explicitly say so.

Code:
{user_input}
"""

    elif mode == "explain":
        return f"""
You are a senior software engineer explaining code to another engineer.

IMPORTANT RULES:
- Do NOT guess algorithm names unless explicit.
- Separate facts from interpretations.
- Do NOT over-report bugs.
- If the code is reasonable, say so.

{analysis_block}

Return your response STRICTLY in the following format:

### INTENT
Explain what the code is doing.

### FACTUAL OBSERVATIONS
Only structural facts derived from the code itself.

### INTERPRETATION (LOW CONFIDENCE)
Explain behavior or intent that cannot be proven with certainty.

### ISSUES
Classify as:
- Critical bug
- Potential improvement
- Design tradeoff
- Performance consideration

If none apply, say:
"No critical issues found."

### COMPLEXITY
Explain time and space complexity conservatively.

### NOTES
Any additional insights that may help understanding.

Code:
{user_input}
"""

    elif mode == "generate":
        return f"""
You are a senior {language} engineer.

Generate correct, readable, and production-quality {language} code
based on the requirement below.

IMPORTANT RULES:
- Do NOT assume missing details.
- If something is unclear, state assumptions explicitly.
- Prefer clarity over cleverness.
- Do NOT over-engineer.
- Ensure the solution is correct before optimizing.

Return your response STRICTLY in the following format:

### INTENT
Briefly restate what the code is supposed to do.

### ASSUMPTIONS
List any assumptions you made due to missing or ambiguous requirements.
If none, say "No assumptions made."

### DESIGN CHOICES
Explain the chosen approach and why it was selected over alternatives.

### EDGE CASES
List important edge cases and how the solution handles them.

### COMPLEXITY
State time and space complexity.

### CODE
Provide the full {language} implementation.

Requirement:
{user_input}
"""


    elif mode == "sql":
        return f"""
You are a senior SQL engineer.

IMPORTANT RULES:
- Do NOT assume schema details unless provided.
- If schema information is missing, explicitly state assumptions.
- Prefer correctness over clever optimizations.
- Avoid hallucinated columns or tables.

Return your response in the following format:

### QUERY
Provide the SQL query.

### EXPLANATION
Explain what the query does.

### ASSUMPTIONS
List any assumptions made about schema or data.

### OPTIMIZATION NOTES
Indexes or improvements, if applicable.
If none, say so explicitly.

Requirement:
{user_input}
"""

    else:
        raise ValueError("Invalid mode")




@app.post("/ask", response_model=askResponse)

def ask_ai(req: askRequest):
    analysis = None
    if req.language.lower() == "python" and req.mode in {"review", "explain"}:
        analysis = analyzeCode(req.input)
    try:
        provider = req.provider or os.getenv("PROVIDER")
        api_key = req.api_key or os.getenv("GROQ_API_KEY")

        if not provider or not api_key:
            raise HTTPException(
                status_code=400,
                detail="No API key provided and no default API key configured"
            )


        llm = get_llm(req.provider, req.api_key)

        prompt = build_prompt(
            mode=req.mode,
            language=req.language,
            user_input=req.input,
            analysis = analysis
        )


        messages = [
            SystemMessage(content="You are a helpful AI coding assistant."),
            HumanMessage(content=prompt)
        ]

        result = llm.invoke(messages)

        return askResponse(response=result.content.strip())

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


