import asyncio
from fotmob import FotMob

import json

async def main():
    async with FotMob() as fotmob:
        # Search for players
        players = await fotmob.search_player("saka")
        print(json.dumps(players, indent = 4))
        
        # Get today's matches
        matches = await fotmob.live_games()
        print(json.dumps(matches, indent = 4))
        
        # Get Premier League standings
        standings = await fotmob.standings(47)
        print(json.dumps(standings, indent = 4))
asyncio.run(main())