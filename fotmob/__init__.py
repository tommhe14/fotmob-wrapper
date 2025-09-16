from .api import FotmobApi

import datetime
from typing import Dict, Any, List, Optional
import urllib.parse

class FotMob:
    """Main FotMob API wrapper interface"""
    
    def __init__(self, proxy_url: Optional[str] = None):
        self._api = FotmobApi(proxy_url=proxy_url)
    
    async def __aenter__(self):
        """Enter async context manager"""
        await self._api._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager"""
        await self._api.close()

    async def close(self):
        """Close context manager"""
        await self._api.close()

    async def search(self, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """Search for teams, players, leagues, and more"""
        data = await self._api._get(f"/data/search/suggest?hits={hits}&lang=en,de,pl,da&term={urllib.parse.quote(term)}")
        if data and isinstance(data, list):
            return data[0].get("suggestions", [])
        return []

    async def search_team(self, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """Search for teams"""
        suggestions = await self.search(term, hits)
        return [item for item in suggestions if item.get("type") == "team"]

    async def search_league(self, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """Search for leagues"""
        suggestions = await self.search(term, hits)
        return [item for item in suggestions if item.get("type") == "league"]

    async def search_player(self, term: str, hits: int = 50) -> List[Dict[str, Any]]:
        """Search for players"""
        suggestions = await self.search(term, hits)
        return [item for item in suggestions if item.get("type") == "player"]

    async def get_league(self, league_id: int, ccode3: str = "GBR") -> Dict[str, Any]:
        """Get league details"""
        return await self._api._get(f"/data/leagues?id={league_id}&ccode3={ccode3}")

    async def standings(self, league_id: int) -> Dict[str, Any]:
        """Get league standings/table"""
        return await self._api._get(f"/data/tltable?leagueId={league_id}")

    async def get_league_news(self, league_id: int, language: str = "en-GB", start_index: int = 0) -> Dict[str, Any]:
        """Get league news"""
        return await self._api._get(f"/data/tlnews?id={league_id}&type=league&language={language}&startIndex={start_index}")

    async def get_league_fixtures(self, league_id: int, season: str) -> Dict[str, Any]:
        """Get league fixtures for a season"""
        encoded_season = urllib.parse.quote(season)
        return await self._api._get(f"/data/fixtures?id={league_id}&season={encoded_season}")

    async def totw_rounds(self, league_id: int, season: str) -> Dict[str, Any]:
        """Get TOTW rounds"""
        encoded_season = urllib.parse.quote(season)
        return await self._api._get(f"/data/team-of-the-week/rounds?leagueId={league_id}&season={encoded_season}")

    async def totw(self, league_id: int, season: str, round_id: int, get_image_url: bool = False) -> Dict[str, Any]:
        """Get TOTW for a specific round"""
        encoded_season = urllib.parse.quote(season)
        data = await self._api._get(f"/data/team-of-the-week/team?leagueId={league_id}&roundId={round_id}&season={encoded_season}")
        
        if get_image_url and data:
            return f"https://images.fotmob.com/image_resources/logo/leaguelogo/{league_id}.png"
        return data

    async def get_team(self, team_id: int, ccode3: str = "GBR") -> Dict[str, Any]:
        """Get team details"""
        return await self._api._get(f"/data/teams?id={team_id}&ccode3={ccode3}")

    async def get_team_news(self, team_id: int, language: str = "en-GB", start_index: int = 0) -> Dict[str, Any]:
        """Get team news"""
        return await self._api._get(f"/data/tlnews?id={team_id}&type=team&language={language}&startIndex={start_index}")

    async def get_team_fixtures(self, team_id: int, before: Optional[int] = None) -> Dict[str, Any]:
        """Get team fixtures"""
        endpoint = f"/data/pageableFixtures?teamId={team_id}"
        if before:
            endpoint += f"&before={before}"
        return await self._api._get(endpoint)

    async def get_team_stats(self, team_id: int, tournament_id: int, is_team_sub_tab: bool = False) -> Dict[str, Any]:
        """Get team statistics for a tournament"""
        return await self._api._get(f"/data/teamseasonstats?teamId={team_id}&tournamentId={tournament_id}&isTeamSubTab={str(is_team_sub_tab).lower()}")

    async def get_player(self, player_id: int) -> Dict[str, Any]:
        """Get player details"""
        return await self._api._get(f"/data/playerData?id={player_id}")

    async def player_stats(self, player_id: int, season_id: str = "0-1", is_first_season: bool = False) -> Dict[str, Any]:
        """Get player statistics"""
        return await self._api._get(f"/data/playerStats?id={player_id}&seasonId={season_id}&isFirstSeason={str(is_first_season).lower()}")

    async def get_matches_by_date(self, date: Optional[str] = None, timezone: str = "Europe/London", ccode3: str = "GBR") -> Dict[str, Any]:
        """Get matches for a specific date"""
        if date is None:
            date = datetime.datetime.now().strftime("%Y%m%d")
        return await self._api._get(f"/data/matches?date={date}&timezone={timezone}&ccode3={ccode3}")

    async def get_notable_matches(self, lang: str = "en-GB", country: str = "GBR") -> Dict[str, Any]:
        """Get notable matches"""
        return await self._api._get(f"/data/notableMatches?lang={lang}&country={country}")

    async def get_match(self, match_id: int) -> Dict[str, Any]:
        """Get match details"""
        return await self._api._get(f"/data/match?id={match_id}")

    async def get_match_odds(self, match_id: int, ccode3: str = "GBR") -> Dict[str, Any]:
        """Get match odds"""
        return await self._api._get(f"/data/matchOdds?matchId={match_id}&ccode3={ccode3}")

    async def get_tv_listings(self, match_id: int, country_code: str = "GB") -> Dict[str, Any]:
        """Get TV listings for a match"""
        return await self._api._get(f"/data/tvlistings?countryCode={country_code}&ids={match_id}")

    async def get_fixture_difficulty(self, league_id: int) -> Dict[str, Any]:
        """Get fixture difficulty for a league"""
        return await self._api._get(f"/data/fixtureDifficulty?id={league_id}")

    async def get_historical_table(self, team_id: int, table_link: str) -> Dict[str, Any]:
        """Get historical table data"""
        return await self._api._get(f"/data/historicaltable?teamId={team_id}&tableLink={table_link}")

    def get_team_logo(self, team_id: int) -> str:
        """Get team logo URL"""
        return f"https://images.fotmob.com/image_resources/logo/teamlogo/{team_id}.png"

    def get_league_logo(self, league_id: int) -> str:
        """Get league logo URL"""
        return f"https://images.fotmob.com/image_resources/logo/leaguelogo/dark/{league_id}.png"

    def get_nation_logo(self, nation_code: str) -> str:
        """Get nation logo URL"""
        return f"https://images.fotmob.com/image_resources/logo/teamlogo/{nation_code.lower()}.png"

    def get_player_image(self, player_id: int) -> str:
        """Get player image URL"""
        return f"https://images.fotmob.com/image_resources/logo/playerimages/{player_id}.png"

    async def todays_games(self, timezone: str = "Europe/London", ccode3: str = "GBR") -> Dict[str, Any]:
        """Get today's matches"""
        today = datetime.datetime.now().strftime("%Y%m%d")
        return await self.get_matches_by_date(today, timezone, ccode3)

    async def live_games(self, timezone: str = "Europe/London", ccode3: str = "GBR") -> List[Dict[str, Any]]:
        """Get live matches (not finished)"""
        data = await self.todays_games(timezone, ccode3)
        if not data or not isinstance(data, dict):
            return []

        live_games = [
            match
            for league in data.get("leagues", [])
            for match in league.get("matches", [])
            if match.get("status", {}).get("reason", {}).get("longKey") != "finished"
        ]
        return live_games
