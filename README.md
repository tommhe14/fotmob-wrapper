## FotMob API Wrapper

A comprehensive Python wrapper for the FotMob API with built-in proxy support for bypassing restrictions.

[![PyPI Downloads](https://static.pepy.tech/badge/fotmob-wrapper)](https://pepy.tech/projects/fotmob-wrapper)

## Installation

```py
pip install fotmob-wrapper
```

## Quick Start

```py
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
```

## Features
- ✅ Automatic proxy token handling and caching

- ✅ Full coverage of FotMob API endpoints

- ✅ Async/await support

- ✅ Type hints throughout

- ✅ Error handling and fallback mechanisms

- ✅ Image URL generators for teams, players, and leagues

## API Methods

# Search Methods

```py
await fotmob.search("query")  # General search
await fotmob.search_player("player name")
await fotmob.search_team("team name")
await fotmob.search_league("league name")
```

# League Methods

```py
await fotmob.get_league(47)  # League details (47 = Premier League)
await fotmob.get_league_current_season(47)  # League current season
await fotmob.standings(47)  # League table
await fotmob.get_league_news(47)  # League news
await fotmob.get_league_fixtures(47, "2024/2025")  # Season fixtures
await fotmob.totw_rounds(47, "2024/2025")  # TOTW rounds
await fotmob.totw(47, "2024/2025", 1)  # Team of the Week
await fotmob.get_league_next_fixture(47)
```

# Team Methods

```py
await fotmob.get_team(9825)  # Team details (9825 = Arsenal)
await fotmob.get_team_news(9825)  # Team news
await fotmob.get_team_fixtures(9825)  # Team fixtures
await fotmob.get_team_stats(9825, 27110)  # Team tournament stats
await fotmob.get_team_next_fixture(9825)
await fotmob.get_team_last_fixture(9825)
await fotmob.get_team_next_fixtures(9825)
await fotmob.get_team_last_fixtures(9825)
```

# Player Methods

```py
await fotmob.get_player(664500)  # Player details
await fotmob.player_stats(664500)  # Player statistics
```

# Match Methods

```py
await fotmob.get_matches_by_date("20241225")  # Matches by date
await fotmob.get_notable_matches()  # Notable matches
await fotmob.get_match(4813416)  # Match details
await fotmob.get_match_odds(4813416)  # Match odds
await fotmob.get_tv_listings(4813416, "GB")  # TV listings
```

# Utility Methods

```py
await fotmob.todays_games()  # Today's matches (convenience method)
await fotmob.live_games()  # Live matches (convenience method)
await fotmob.get_fixture_difficulty(47)  # Fixture difficulty
await fotmob.get_historical_table(9825)  # Historical table

# Image URLs (no API call needed)
fotmob.get_team_logo(9825)  # Team logo URL
fotmob.get_league_logo(47)  # League logo URL
fotmob.get_player_image(664500)  # Player image URL
fotmob.get_nation_logo("ENG")  # Nation logo URL
```

# Debugging

```py
import logging
logging.basicConfig(level=logging.DEBUG)

async with FotMob() as fotmob:
    # Debug information will be logged
    await fotmob.todays_games()
```
