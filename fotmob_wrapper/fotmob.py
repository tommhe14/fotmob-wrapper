from .api import FotmobApi
import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import urllib.parse

class FotMob:

    def __init__(self, api: FotmobApi = None):
        self.api = api or FotmobApi()
        self.enums = self.ENUMS

    @classmethod
    async def search(cls, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """
        Searches FotMob for teams, players, leagues, and more based on a search term.

        Args:
            term (str): The search query (e.g., team or player name).
            hits (int, optional): Maximum number of results to return. Defaults to 50.

        Returns:
            List[Dict[str, Any]]: A list of suggestion dictionaries containing search results.
        """
        api = FotmobApi()
        data = await api._get(f"/search/suggest?hits={hits}&lang=en&term={term.replace(' ', '+')}")
        await api.close()

        if data and isinstance(data, list):
            return data[0].get("suggestions", [])
        return []
    
    @classmethod
    async def search_team(cls, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """
        Searches FotMob for teams based on a search term.

        Args:
            term (str): The search query (e.g., team name).
            hits (int, optional): Maximum number of results to return. Defaults to 50.

        Returns:
            List[Dict[str, Any]]: A filtered list of team suggestions.
        """
        api = FotmobApi()
        data = await api._get(f"/search/suggest?hits={hits}&lang=en&term={term.replace(' ', '+')}")
        await api.close()

        if data and isinstance(data, list):
            suggestions = data[0].get("suggestions", [])
            return [item for item in suggestions if item.get("type") == "team"]
        return []
    
    @classmethod
    async def search_league(cls, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """
        Searches FotMob for leagues based on a search term.

        Args:
            term (str): The search query (e.g., league name).
            hits (int, optional): Maximum number of results to return. Defaults to 50.

        Returns:
            List[Dict[str, Any]]: A filtered list of league suggestions.
        """
        api = FotmobApi()
        data = await api._get(f"/search/suggest?hits={hits}&lang=en&term={term.replace(' ', '+')}")
        await api.close()

        if data and isinstance(data, list):
            suggestions = data[0].get("suggestions", [])
            return [item for item in suggestions if item.get("type") == "league"]
        return []
    
    @classmethod
    async def search_player(cls, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """
        Searches FotMob for players based on a search term.

        Args:
            term (str): The search query (e.g., player name).
            hits (int, optional): Maximum number of results to return. Defaults to 50.

        Returns:
            List[Dict[str, Any]]: A filtered list of player suggestions.
        """
        api = FotmobApi()
        data = await api._get(f"/search/suggest?hits={hits}&lang=en&term={term.replace(' ', '+')}")
        await api.close()

        if data and isinstance(data, list):
            suggestions = data[0].get("suggestions", [])
            return [item for item in suggestions if item.get("type") == "player"]
        return []
    
    @classmethod
    async def all_leagues(cls) -> Dict[str, Any]:
        """
        Retrieves all leagues available on FotMob.

        Returns:
            Dict[str, Any]: A dictionary containing all league information.
        """
        api = FotmobApi()
        data = await api._get("/allLeagues")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def today_games(cls) -> Dict[str, Any]:
        """
        Retrieves all matches scheduled for today.

        Returns:
            Dict[str, Any]: A dictionary containing today's match information.
        """
        today = datetime.datetime.now().date()
        passed_date = today.strftime("%Y%m%d")

        api = FotmobApi()
        try:
            data = await api._get(f"/matches?date={passed_date}")
        finally:
            await api.close()

        if data and isinstance(data, dict):
            return data
        return {}

    @classmethod
    async def live_games(cls) -> List[Dict[str, Any]]:
        """
        Retrieves all matches scheduled for today that have finished.

        Returns:
            List[Dict[str, Any]]: A list of match dictionaries where the match is finished.
        """
        today = datetime.datetime.now().date()
        passed_date = today.strftime("%Y%m%d")

        api = FotmobApi()
        try:
            data = await api._get(f"/matches?date={passed_date}")
        finally:
            await api.close()

        if not data or not isinstance(data, dict):
            return []

        live_games = [
            match
            for league in data.get("leagues", [])
            for match in league.get("matches", [])
            if match.get("status", {}).get("reason", {}).get("longKey") != "finished"
        ]

        return live_games
    
    @classmethod
    async def standings(cls, LeagueId: int) -> Dict[str, Any]:
        """
        Retrieves current standings table for a given league

        Returns:
            Dict[str, Any]: A dictionary containing all league information.
        """
        api = FotmobApi()
        data = await api._get(f"/tltable?leagueId={LeagueId}")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_league(cls, LeagueId: int) -> Dict[str, Any]:
        """
        Retrieves league data including stats, games, transfers etc.

        Returns:
            Dict[str, Any]: A dictionary containing all league information.
        """
        api = FotmobApi()
        data = await api._get(f"/leagues?id={LeagueId}&ccode3=GBR")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_league_current_season(cls, LeagueId: int) -> Dict[str, Any]:
        """
        Retrieves league data including stats, games, transfers etc.

        Args:
            LeagueId (int): The ID of the league.

        Returns:
            Dict[str, Any]: A dictionary containing the current season or an empty dictionary.
        """
        api = FotmobApi()
        data = await api._get(f"/leagues?id={LeagueId}&ccode3=GBR")
        await api.close()

        if data and isinstance(data, dict):
            seasons = data.get("allAvailableSeasons", [])
            if seasons:
                return seasons[0]

        return {}
    
    @classmethod
    async def get_league_news(cls, LeagueId: int) -> Dict[str, Any]:
        """
        Retrieves league news.

        Args:
            LeagueId (int): The ID of the league.

        Returns:
            Dict[str, Any]: A dictionary containing all league news.
        """
        api = FotmobApi()
        data = await api._get(f"/tlnews?id={LeagueId}&type=league&language=en-GB&startIndex=0")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_league_fixtures(cls, LeagueId: int, Season: str) -> Dict[str, Any]:
        """
        Retrieves seasonal fixtures for the given league.

        Args:
            LeagueId (int): The ID of the league.
            Season (str): Provide season in a standard format, e.g. '2024/2025'.

        Returns:
            Dict[str, Any]: A dictionary containing all league fixture information.
        """
        encoded_season = urllib.parse.quote(Season, safe="")  # <-- fix here

        api = FotmobApi()
        data = await api._get(f"/fixtures?id={LeagueId}&season={encoded_season}")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {}
    
    @classmethod
    async def totw_rounds(cls, LeagueId: int, Season: str) -> Dict[str, Any]:
        """
        Retrieves the Team of the Week (TOTW) rounds for a given league and season.

        Args:
            LeagueId (int): The ID of the league.
            Season (str): Provide season in a standard format, e.g. '2024/2025'.

        Returns:
            Dict[str, Any]: A dictionary containing TOTW round information.
        """
        encoded_season = urllib.parse.quote(Season)

        api = FotmobApi()
        data = await api._get(f"/team-of-the-week/rounds?leagueid={LeagueId}&season={encoded_season}")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def totw(cls, LeagueId: int, Season: str, Round: int, totw_image: bool = None) -> Dict[str, Any]:
        """
        Retrieves the Team of the Week (TOTW) rounds for a given league and season.

        Args:
            LeagueId (int): The ID of the league.
            Season (str): Provide season in a standard format, e.g. '2024/2025'.
            totw_image (bool): Return the requested totw in an image format

        Returns:
            Dict[str, Any]: A dictionary containing TOTW round information.
        """

        api = FotmobApi()
        data = await api._get(f"/team-of-the-week/team?leagueid={LeagueId}&roundId={Round}&season={Season}")
        await api.close()

        if data and isinstance(data, dict):
            return data if not totw_image else f"https://www.fotmob.com/api/league/totw?leagueId={LeagueId}&season={Season}&roundId={Round}&lang=en-GB,en-US,en"
        return {} 
    
    @classmethod
    async def get_team_news(cls, TeamId: int) -> Dict[str, Any]:
        """
        Retrieves Team news.

        Args:
            TeamId (int): The ID of the Team.

        Returns:
            Dict[str, Any]: A dictionary containing the team news.
        """
        api = FotmobApi()
        data = await api._get(f"/tlnews?id={TeamId}&type=team&language=en-GB&startIndex=0")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_team(cls, TeamId: int) -> Dict[str, Any]:
        """
        Retrieves Team data

        Args:
            TeamId (int): The ID of the Team

        Returns:
            Dict[str, Any]: A dictionary containing the team data
        """
        api = FotmobApi()
        data = await api._get(f"/teams?id={TeamId}&ccode3=GBR")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_player(cls, PlayerId: int) -> Dict[str, Any]:
        """
        Retrieves Player data

        Args:
            PlayerId (int): The ID of the Player

        Returns:
            Dict[str, Any]: A dictionary containing the Player data
        """
        api = FotmobApi()
        data = await api._get(f"/playerData?id={PlayerId}")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def player_stats(cls, PlayerId: int) -> Dict[str, Any]:
        """
        Retrieves Player Stats

        Args:
            PlayerId (int): The ID of the Player

        Returns:
            Dict[str, Any]: A dictionary containing the Player data
        """
        api = FotmobApi()
        data = await api._get(f"/playerStats?id={PlayerId}&seasonId=0-1&isFirstSeason=false")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_match(cls, Matchid: int) -> Dict[str, Any]:
        """
        Retrieves Match Data

        Args:
            MatchId (int): The ID of the Player

        Returns:
            Dict[str, Any]: A dictionary containing the Match data
        """
        api = FotmobApi()
        data = await api._get(f"/matchDetails?matchId={Matchid}")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {}
    
    @classmethod
    async def get_tv_listings(cls, Matchid: int, CountryCode: str = "GB") -> Dict[str, Any]:
        """
        Retrieves Match Data

        Args:
            MatchId (int): The ID of the Player

        Returns:
            Dict[str, Any]: A dictionary containing the Match data
        """
        api = FotmobApi()
        data = await api._get(f"/tvlisting?matchId={Matchid}&countryCode={CountryCode.upper()}&ids=")
        await api.close()

        if data and isinstance(data, dict):
            return data
        return {} 
    
    @classmethod
    async def get_team_logo(cls, TeamId: int) -> str:
        """
        Retrieves Team Logo

        Args:
            TeamId (int): The ID of the Team
        """
        return f"https://images.fotmob.com/image_resources/logo/teamlogo/{TeamId}.png"
    
    @classmethod
    async def get_league_logo(cls, LeagueId: int) -> str:
        """
        Retrieves League Logo

        Args:
            League (int): The ID of the League
        """
        return f"https://images.fotmob.com/image_resources/logo/leaguelogo/dark/{LeagueId}.png"
    
    @classmethod
    async def get_nation_logo(cls, NationCode: int) -> str:
        """
        Retrieves Nation logo

        Args:
            NationCode (STR): The code of the nation
        """
        return f"https://images.fotmob.com/image_resources/logo/teamlogo/{NationCode.lower()}.png"
    
    @classmethod
    async def get_player_logo(cls, PlayerId: int) -> str:
        """
        Retrieves Player logo

        Args:
            PLayerId (int): The Id of the player
        """
        return f"https://images.fotmob.com/image_resources/logo/playerimages/{PlayerId}.png"
    
    

    

    

    
    



    

    


