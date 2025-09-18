import aiohttp
from typing import Dict, Any, Optional
import time
import base64

from .utils.ls_x import ls_x

class FotmobApi:
    def __init__(self, proxy_url: Optional[str] = None):
        self.base_url = "https://www.fotmob.com/api"
        if proxy_url:
            self.proxy_url = proxy_url
        else:
            self.proxy_url = base64.b64decode(ls_x).decode('utf-8')

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.fotmob.com/",
        }
        self.session = None
        self.x_mas_token = None
        self.token_expiry = 0
        self.token_ttl = 3600  

    async def _ensure_session(self):
        """Ensure we have an active session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.headers)

    async def _get_x_mas_token(self):
        """Get and cache the x-mas token from the proxy"""
        current_time = time.time()
        if self.x_mas_token and current_time < self.token_expiry:
            return self.x_mas_token
        
        try:
            await self._ensure_session()
            async with self.session.get(self.proxy_url) as response:
                response.raise_for_status()
                auth_data = await response.json()
                self.x_mas_token = auth_data.get("x-mas")
                if self.x_mas_token:
                    self.token_expiry = current_time + self.token_ttl
                    return self.x_mas_token
        except Exception as e:
            print(f"Failed to get x-mas token from {self.proxy_url}: {e}")
        
        return None

    async def _get(self, endpoint: str = None, raw_url: str = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Base request method with x-mas token handling"""
        await self._ensure_session()
        
        x_mas_token = await self._get_x_mas_token()
        
        headers = self.headers.copy()
        if x_mas_token:
            headers["x-mas"] = x_mas_token
        
        url = f"{self.base_url}{endpoint}" if not raw_url else raw_url
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            if x_mas_token:
                try:
                    headers_without_token = self.headers.copy()
                    async with self.session.get(url, params=params, headers=headers_without_token) as response:
                        response.raise_for_status()
                        return await response.json()
                except aiohttp.ClientError:
                    pass
            raise Exception(f"API request to {url} failed: {str(e)}")

    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()