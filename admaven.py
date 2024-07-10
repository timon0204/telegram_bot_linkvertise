import httpx
import asyncio
import settings
from linkvertise import generate_rentry

async def generate_admaven_link(url) -> str:
    url = generate_rentry(url)
    api_url = settings.ADMAVEN_API_URL.format(
        api_token=settings.ADMAVEN_API_TOKEN, title=settings.ADMAVEN_TITLE,
        url=url, image_url=settings.IMAGE_URL
    )

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(api_url)
        response_json = response.json()
        
        # Extracting the full_short value
        full_short = response_json["message"][0]["full_short"]
        return full_short

if __name__ == "__main__":
    full_short_link = asyncio.run(generate_admaven_link("https://mega.nz"))
    print(full_short_link)
