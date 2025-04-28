import asyncio
import json
import datetime
from fotmob_wrapper.fotmob import FotMob

async def main():
    result = await FotMob.player_stats(PlayerId=961995)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
