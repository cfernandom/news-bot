import asyncio
from dotenv import load_dotenv

load_dotenv()

from services.orchestrator.src.main import run_pipeline

async def main():
    await run_pipeline()

asyncio.run(main())