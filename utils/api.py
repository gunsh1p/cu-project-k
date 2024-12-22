import httpx

import config


async def get_weather(city: str) -> dict[str, float | int]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.API_HOST}/api/get-weather?city={city}")
        response.raise_for_status()
        return response.json()
