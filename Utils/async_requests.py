import aiohttp
from Utils.logger import logger

async def async_get(url: str, headers: dict = None, params: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            data: dict = await response.json()
            if not response.ok:
                raise HttpRequestException(f"Error while making GET request to {url}: {response.status} {response.reason}")
            return data

async def async_post(url: str, headers: dict = None, data: str = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            resp_data = await response.json()
            if not response.ok:
                raise HttpRequestException(f"Error while making POST request to {url}: {response.status}")
            return resp_data

async def async_ping(method: str, url: str, headers: dict = None, data: str = None) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url,  headers=headers, data=data) as response:
            return response.status



class HttpRequestException(Exception):
    pass