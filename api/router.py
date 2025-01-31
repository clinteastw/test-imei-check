from fastapi import APIRouter, Depends, HTTPException

from api.auth.auth import current_user
from api.models.tokens import APIToken
from api.models.users import APIUser as User
from bot.models.users_tg import TgUser
from bot.utils import is_valid_imei

from .imei_check.schemas import IMEICheckRequest
from .imei_check.utils import get_imei_info

api_router = APIRouter()

@api_router.get("/api/get-token")
async def get_token(user: User = Depends(current_user)):
    token = await APIToken.get_or_create_token(user.id)
    return {"message": f"Here is your token {token}"}

@api_router.post("/api/add-user-to-whitelist")
async def add_user_to_white_list(tg_id: str, token: str):
    token = await APIToken.get_by_token_value(token)
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    tg_user = await TgUser.get_user_from_whitelist(tg_id)
    if tg_user:
        return {"message": "User already in whitelist"}
    new_tg_user = await TgUser.add_user_to_whitelist(tg_id)
    return {"message": f"User {tg_id} now in whitelist"}

@api_router.post("/api/check-imei")
async def check_imei(request: IMEICheckRequest):
    token = await APIToken.get_by_token_value(request.token)
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not is_valid_imei(request.imei):
        raise HTTPException(status_code=400, detail="Invalid IMEI")
    
    result = await get_imei_info(request.imei)
    return {"imei": request.imei, "info": result}