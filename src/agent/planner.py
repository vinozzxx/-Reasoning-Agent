# # # src/agent/planner.py
# # # from langchain import LLMChain, PromptTemplate

# # from langchain_core.prompts import PromptTemplate
# # from langchain_core.output_parsers import JsonOutputParser
# # from langchain_core.runnables import RunnableSequence


# # from langchain_openai import ChatOpenAI
# # import json

# # from src.prompts import planner_prompt

# # def create_planner(llm):
# #     template = PromptTemplate(
# #         template=planner_prompt,
# #         input_variables=["question"]
# #     )
# #     return template | llm


# # async def plan_question(chain, question: str):
# #     resp = await chain.ainvoke({"question": question})
# #     text = resp.content.strip()

# #     # Expect JSON output
# #     try:
# #         return json.loads(text)["plan"]
# #     except:
# #         raise ValueError(f"Planner JSON parse failed: {text}")

# from langchain_core.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# import json
# from src.prompts import planner_prompt

# def create_planner(llm):
#     template = PromptTemplate(
#         template=planner_prompt,
#         input_variables=["question"]
#     )
#     return template | llm

# async def plan_question(chain, question: str):
#     resp = await chain.ainvoke({"question": question})
#     text = resp.content.strip()
#     # return json.loads(text)["plan"]

# def safe_json(text):
#     import json, re

#     # Extract JSON between first and last curly brace
#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     if not match:
#         raise ValueError(f"LLM did not return JSON:\n{text}")

#     cleaned = match.group()
#     try:
#         return json.loads(cleaned)
#     except Exception as e:
#         raise ValueError(f"Invalid JSON:\n{cleaned}\n\nOriginal:\n{text}") from e

import json
import re
from langchain_core.prompts import PromptTemplate
from src.prompts import planner_prompt


def safe_json(text: str):
    """
    Extract valid JSON from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Planner did not return JSON:\n{text}")

    json_text = match.group()

    try:
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Planner JSON invalid:\n{json_text}\n\nOriginal:\n{text}") from e


def create_planner(llm):
    """
    Returns a chain: Prompt → LLM
    """
    template = PromptTemplate(
        template=planner_prompt,
        input_variables=["question"]
    )
    return template | llm


async def plan_question(chain, question: str):
    """
    Runs the planner and extracts plan[] from output.
    """
    resp = await chain.ainvoke({"question": question})
    text = resp.content.strip()
    data = safe_json(text)
    return data["plan"]
