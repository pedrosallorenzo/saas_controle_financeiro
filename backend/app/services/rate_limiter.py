from datetime import date
from app.config import settings
import httpx

LIMITS = {
    "parse": 50,
    "ask": 20,
}


async def check_rate_limit(user_id: str, action: str) -> bool:
    today = date.today().isoformat()
    key = f"rate:{user_id}:{action}:{today}"
    limit = LIMITS.get(action, 10)

    headers = {
        "Authorization": f"Bearer {settings.upstash_redis_token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        incr_resp = await client.post(
            f"{settings.upstash_redis_url}/incr/{key}",
            headers=headers,
        )
        count = incr_resp.json().get("result", 0)

        if count == 1:
            await client.post(
                f"{settings.upstash_redis_url}/expire/{key}/86400",
                headers=headers,
            )

    return count <= limit
