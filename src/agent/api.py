# src/agent/api.py (CLI part)
if __name__ == "__main__":
    import asyncio
    from src.agent.main import solve
    while True:
        q = input("Question> ")
        if q.strip() in ("exit","quit"): break
        result = asyncio.run(solve(q))
        print(result)


# src/agent/api.py (HTTP)
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/solve")
async def solve_endpoint(q: Query):
    from src.agent.main import solve
    return await solve(q.question)
