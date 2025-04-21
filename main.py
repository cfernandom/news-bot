import asyncio
from services.decision_engine.src.main import main as decision_engine

async def main():
    await decision_engine()

asyncio.run(main())