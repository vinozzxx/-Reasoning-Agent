#  Multi-Step Reasoning Agent with Self‑Checking

This project implements a **multi‑step reasoning agent** that solves structured word problems using a **Planner → Executor → Verifier** architecture. The agent produces accurate answers while **hiding raw chain‑of‑thought**, exposing only short, user‑friendly reasoning and metadata for debugging.

This repository was built as part of a **Junior AI/ML / GenAI Engineer assignment**.

---

##  Key Features

*  Planner–Executor–Verifier agent loop
*  Dynamic retries when verification fails
*  Chain‑of‑thought hidden from end users
*  Modular prompt design (no hard‑coded prompts)
*  CLI / API‑ready architecture
*  Easy to swap LLM providers (Groq / OpenAI / etc.)

---

##  Problem Types Supported

* Time difference calculations
* Arithmetic & logical reasoning
* Constraint satisfaction problems
* Multi‑step word problems

**Example:**

> *“A meeting needs 60 minutes. Free slots are 09:00–09:30, 09:45–10:30, 11:00–12:00. Which slots fit?”*

---

##  Architecture Overview

The agent runs in **three internal phases**:

### 1️ Planner

* Reads the user question
* Breaks it into a concise step‑by‑step plan
* Example steps: parse → extract data → compute → validate → format

### 2️ Executor

* Executes the plan step by step
* Produces intermediate calculations
* Uses Python or LLM calls as needed

### 3️ Verifier

* Independently checks the solution
* Validates constraints and consistency
* Triggers retries if errors are detected

Only the **final answer + short explanation** are shown to the user.

---

##  Project Structure

```
.
├── .venv/                     # Virtual environment
├── prompts/                   # Prompt templates
│   ├── planner_prompt.txt     # Planner instructions
│   ├── executor_prompt.txt    # Executor instructions
│   └── verifier_prompt.txt    # Verifier instructions
│
├── src/
│   ├── agent/                 # Core agent logic
│   │   ├── __init__.py
│   │   ├── api.py             # API / interface layer
│   │   ├── planner.py         # Planner module
│   │   ├── executor.py        # Executor module
│   │   ├── verifier.py        # Verifier module
│   │
│   ├── prompts.py             # Prompt loader & manager
│   ├── tests.py               # Test cases & evaluation
│   └── __pycache__/
│
├── .env                       # Environment variables (API keys)
├── app.py                     # Entry point (CLI / API runner)
├── requirements.txt           # Dependencies
├── .gitignore
└── README.md
```

---

##  Where Prompts Live

All prompts are **separated from code** and stored under:

```
prompts/
├── planner_prompt.txt
├── executor_prompt.txt
└── verifier_prompt.txt
```

This makes the system:

* Easy to debug
* Easy to tune
* Easy to swap LLMs

---

##  How to Run

### 1️ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2️ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️ Add environment variables

Create a `.env` file:

```
LLM_API_KEY=your_api_key_here
```

### 4️ Run the agent

```bash
python app.py
```

---

##  Output Format (JSON)

```json
{
  "answer": "<final short answer>",
  "status": "success",
  "reasoning_visible_to_user": "<short explanation>",
  "metadata": {
    "plan": "<abbreviated internal plan>",
    "checks": [
      {
        "check_name": "Time consistency",
        "passed": true,
        "details": "Verified independently"
      }
    ],
    "retries": 0
  }
}
```

---

##  Testing & Evaluation

* Includes **easy + tricky test cases**
* Logs:

  * Question
  * Final output
  * Verification result
  * Retry count

Test file:

```
src/tests.py
```

---

##  Screenshots

> 📌 **Add screenshots here before submission**

Suggested screenshots:

* Project folder structure (VS Code)
* Sample input question
* JSON output result
* Verification pass/fail example

Example:

```md
![Project Structure](screenshots/project_structure.png)
```

---

##  Prompt Design Rationale

* Planner prompt focuses on **explicit step enumeration**
* Executor prompt enforces **step‑by‑step execution**
* Verifier prompt ensures **independent validation**

### What didn’t work well

* Single‑pass reasoning without verification
* Mixing planning + execution in one prompt

### Future Improvements

* Add confidence scoring
* Parallel verification strategies
* RAG for domain‑specific knowledge

---

##  Author

**Vinod Kumar**
Junior AI/ML Engineer Candidate

---

⭐ *If you find this project useful, feel free to star the repository.*
