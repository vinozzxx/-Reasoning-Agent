# # # src/agent/verifier.py
# # # from langchain import LLMChain, PromptTemplate

# # from langchain_core.prompts import PromptTemplate
# # from langchain_core.output_parsers import JsonOutputParser
# # from langchain_core.runnables import RunnableSequence


# # from langchain_openai import ChatOpenAI
# # import json

# # from src.prompts import verifier_prompt

# # def create_verifier(llm):
# #     template = PromptTemplate(
# #         template=verifier_prompt,
# #         input_variables=["question", "solution_json"]
# #     )
# #     return template | llm


# # async def verify(chain, question, solution_json):
# #     resp = await chain.ainvoke({
# #         "question": question,
# #         "solution_json": json.dumps(solution_json)
# #     })
# #     text = resp.content.strip()

# #     try:
# #         return json.loads(text)
# #     except:
# #         raise ValueError(f"Verifier JSON parse failed: {text}")

# from langchain_core.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# import json
# from src.prompts import verifier_prompt

# def create_verifier(llm):
#     template = PromptTemplate(
#         template=verifier_prompt,
#         input_variables=["question", "solution_json"]
#     )
#     return template | llm

# async def verify(chain, question, solution_json):
#     resp = await chain.ainvoke({
#         "question": question,
#         "solution_json": json.dumps(solution_json)
#     })
#     return json.loads(resp.content)

import json
import re
from langchain_core.prompts import PromptTemplate
from src.prompts import verifier_prompt


def safe_json(text: str):
    """
    Extract valid JSON from verifier output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Verifier did not return JSON:\n{text}")

    json_text = match.group()

    try:
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Verifier JSON invalid:\n{json_text}\n\nOriginal:\n{text}") from e


def create_verifier(llm):
    template = PromptTemplate(
        template=verifier_prompt,
        input_variables=["question", "solution_json"]
    )
    return template | llm


async def verify(chain, question, solution_json):
    resp = await chain.ainvoke({
        "question": question,
        "solution_json": json.dumps(solution_json)
    })

    text = resp.content.strip()
    return safe_json(text)
