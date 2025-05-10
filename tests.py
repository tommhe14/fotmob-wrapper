import asyncio
import json
import datetime
from fotmob_wrapper.fotmob import FotMob

async def main():
    result = await FotMob.live_games()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
