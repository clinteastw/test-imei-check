import json

import aiohttp

from config import IMEI_CHECK_API_URL, IMEI_CHECK_SANDBOX_TOKEN


async def get_imei_info(imei: str) -> dict:
    headers = {"Authorization": "Bearer " + IMEI_CHECK_SANDBOX_TOKEN,
               "Content-Type": "application/json",}
    body = json.dumps({
        "deviceId": imei,
        "serviceId": 12,
    })
    async with aiohttp.ClientSession() as session:
        async with session.post(IMEI_CHECK_API_URL, headers=headers, data=body) as response:
            if response.status == 201:
                params = await response.json()
                properties = params.get("properties", {})
                if not properties:
                    return "No device data"

                return {
                    "status": "ok",
                    "detail": {
                                "deviceName": properties.get("deviceName"),
                                "modelCode": properties.get("modelCode"),
                                "imei1": properties.get("imei"),
                                "imei2": properties.get("imei2"),
                                "serial": properties.get("serial"),
                                "unlockNumber": properties.get("unlockNumber"),
                                "miActivationLock": properties.get("miActivationLock"),
                                "skuNumber": properties.get("skuNumber"),
                                "purchaseCountry": properties.get("purchaseCountry"),
                                "warrantyStatus": properties.get("warrantyStatus")
                            }
            }
            return {"error": f"Failed to fetch IMEI information. Status: {response.status}"}