import asyncio
import json
from aiohttp import ClientSession

from private import API_KEY

async def collectData(url, session, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def getDataAPI(session, api_key):
    url = "https://moviesdatabase.p.rapidapi.com/actors/random"
    headers = {
        "X-RapidAPI-Key": f"{api_key}",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }
    return await collectData(url, session, headers=headers)

async def getData(session):
    url = "https://api.thecatapi.com/v1/images/search?limit=10"
    return await collectData(url, session, None)

async def main():
    async with ClientSession() as session:
        tasks = [
            getDataAPI(session, API_KEY),
            getData(session)
        ]
        data1, data2 = await asyncio.gather(*tasks)

        dataJson1 = json.loads(data1)
        dataJson2 = json.loads(data2)

        print("Dane z API 2:", dataJson1)
        print("Dane:", dataJson2)

if __name__ == "__main__":
    asyncio.run(main())
