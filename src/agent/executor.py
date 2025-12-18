# # # src/agent/executor.py
# # # from langchain import LLMChain, PromptTemplate

# # from langchain_core.prompts import PromptTemplate
# # from langchain_core.output_parsers import JsonOutputParser
# # from langchain_core.runnables import RunnableSequence

# # from langchain_openai import ChatOpenAI
# # import json

# # from src.prompts import executor_prompt

# # def create_executor(llm):
# #     template = PromptTemplate(
# #         template=executor_prompt,
# #         input_variables=["question", "plan"]
# #     )
# #     return template | llm


# # async def execute(chain, question, plan):
# #     resp = await chain.ainvoke({"question": question, "plan": str(plan)})
# #     text = resp.content.strip()

# #     try:
# #         return json.loads(text)
# #     except:
# #         raise ValueError(f"Executor JSON parse failed: {text}")

# from langchain_core.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# import json
# from src.prompts import executor_prompt

# def create_executor(llm):
#     template = PromptTemplate(
#         template=executor_prompt,
#         input_variables=["question", "plan"]
#     )
#     return template | llm

# async def execute(chain, question, plan):
#     resp = await chain.ainvoke({"question": question, "plan": str(plan)})
#     return json.loads(resp.content)

import json
import re
from langchain_core.prompts import PromptTemplate
from src.prompts import executor_prompt


def safe_json(text: str):
    """
    Extract valid JSON from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Executor did not return JSON:\n{text}")

    json_text = match.group()

    try:
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Executor JSON invalid:\n{json_text}\n\nOriginal:\n{text}") from e


def create_executor(llm):
    template = PromptTemplate(
        template=executor_prompt,
        input_variables=["question", "plan"]
    )
    return template | llm


async def execute(chain, question, plan):
    resp = await chain.ainvoke({
        "question": question,
        "plan": str(plan)
    })

    text = resp.content.strip()
    return safe_json(text)
