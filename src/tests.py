# src/tests.py
import asyncio
import json

from src.agent.planner import create_planner, plan_question
from src.agent.executor import create_executor, execute
from src.agent.verifier import create_verifier, verify

# Use your LLM wrapper here
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="mixtral-8x7b-32768",   # or llama3-groq-70b
    temperature=0
)


async def run_single_test(question: str):
    planner = create_planner(llm)
    executor = create_executor(llm)
    verifier = create_verifier(llm)

    print(f"\n============================")
    print(f"TEST QUESTION: {question}")
    print(f"============================")

    # Step 1 — Plan
    plan = await plan_question(planner, question)
    print("PLAN:", plan)

    # Step 2 — Execute
    exec_out = await execute(executor, question, plan)
    print("EXECUTOR OUTPUT:", exec_out)

    # Step 3 — Verify
    verify_out = await verify(verifier, question, exec_out)
    print("VERIFIER:", verify_out)

    assert "final_answer" in exec_out, "Executor must return final_answer"
    assert verify_out["passed"] is True, "Verifier must approve"
    print("✅ PASSED")


async def run_all_tests():
    # Easy Tests
    easy_tests = [
        "A train leaves at 14:30 and arrives at 18:05. How long is the journey?",
        "Alice has 3 red apples and twice as many green apples. Total apples?",
        "Tom has 4 chocolates and gets 3 more. How many chocolates?",
        "Divide 100 rupees equally among 4 people. How much each?",
        "A meeting needs 60 minutes. Does 10:00–11:00 fit?",
    ]

    # Tricky Edge Tests
    tricky_tests = [
        "Train leaves at 23:30 and arrives next day at 01:15. Duration?",
        "A shop gives 30% discount on 500 rupees. What is the final price?",
        "If a meeting starts 09:00 and ends 09:30, does a 30-minute meeting fit exactly?",
        "Alice has 1 red apple and half as many green apples. How many total apples?",
        "A worker earns ₹500/day for 5 days and ₹750/day for 2 days. Total earnings?",
    ]

    print("\n### RUNNING EASY TESTS ###")
    for q in easy_tests:
        await run_single_test(q)

    print("\n### RUNNING TRICKY TESTS ###")
    for q in tricky_tests:
        await run_single_test(q)


# Allow: python src/tests.py
if __name__ == "__main__":
    asyncio.run(run_all_tests())
