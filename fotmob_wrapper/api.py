import aiohttp

BASE_URL = "https://www.fotmob.com/api"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Cookie": "NEXT_LOCALE=en-GB; u:location=%7B%22countryCode%22%3A%22GB%22%2C%22regionId%22%3A%22ENG%22%2C%22ip%22%3A%22127.0.0.1%22%2C%22ccode3%22%3A%22GBR%22%2C%22ccode3NoRegion%22%3A%22GBR%22%2C%22timezone%22%3A%22Europe%2FLondon%22%7D",
}

class FotmobApi:
    default_headers = HEADERS
    
    def __init__(self, headers: dict = None):
        self.session = None
        self.headers = self.default_headers 

    async def _get(self, endpoint):
        print(f"{BASE_URL}{endpoint}")
        if self.session is None:
            self.session = aiohttp.ClientSession(headers = self.headers)
        async with self.session.get(f"{BASE_URL}{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to fetch {endpoint}: {response.status}")
            
    async def _raw_get(self, endpoint):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers = self.headers)
        async with self.session.get(endpoint) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to fetch {endpoint}: {response.status}")

    async def close(self):
        if self.session:
            await self.session.close()
