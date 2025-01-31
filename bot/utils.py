import aiohttp

from config import BOT_API_URL


async def send_api_check_imei_request(imei: str, token: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            BOT_API_URL, 
            json={"imei": imei, "token": token}
        ) as response:
            if response.status != 200:
                return {"error": f"Ошибка: {response.status}"}
            return await response.json()


def is_valid_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False
    digits = [int(d) for d in imei]
    checksum = 0
    for i, digit in enumerate(digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0