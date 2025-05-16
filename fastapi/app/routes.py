from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from services.leonardo import LeonardoService
from fastapi import HTTPException
from app.background import track_transaction
from app.storage import load_data, save_data
from app.ip_limit import check_and_update_ip_limit


router = APIRouter()
leonardo_service = LeonardoService()

class MemeRequest(BaseModel):
    animal: str
    object: str

class WalletRequest(BaseModel):
    walletAddress: str

class UnlockRequest(BaseModel):
    walletAddress: str
    txid: str

class GenerationResponse(BaseModel):
    canGenerate: bool
    usedGenerations: int
    limit: int

class UnlockResponse(BaseModel):
    success: bool
    message: str
    newLimit: int

@router.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    image_url = leonardo_service.generate_image(request.animal, request.object)
    if not image_url:
        raise HTTPException(status_code=500, detail="Failed to generate image.")
    return {"image_url": image_url}

@router.post("/can-generate", response_model=GenerationResponse)
def can_generate(request: WalletRequest):
    data = load_data()
    user = data.get(request.walletAddress)
    if not user:
        user = {"canGenerate": True, "usedGenerations": 0, "limit": 2}
        data[request.walletAddress] = user
        save_data(data)
    return GenerationResponse(**user)

@router.post("/use-generation", response_model=GenerationResponse)
def use_generation(request: WalletRequest, req: Request):
    data = load_data()
    user = data.get(request.walletAddress)
    if not user:
        raise HTTPException(status_code=404, detail="User not initialized.")
    if not user["canGenerate"] or user["usedGenerations"] >= user["limit"]:
        raise HTTPException(status_code=403, detail="Generation limit reached or access denied.")
    # Check IP Limit
    # check_and_update_ip_limit(req, user["limit"])
    user["usedGenerations"] += 1
    if user["usedGenerations"] >= user["limit"]:
        user["canGenerate"] = False
    data[request.walletAddress] = user
    save_data(data)
    return GenerationResponse(**user)

@router.post("/unlock", response_model=UnlockResponse)
def unlock_generation_access(req: UnlockRequest):
    wallet = req.walletAddress
    txid = req.txid

    # Загружаем базу, чтобы не потерять новых юзеров
    data = load_data()
    if wallet not in data:
        data[wallet] = {
            "canGenerate": False,
            "usedGenerations": 0,
            "limit": 2
        }
        save_data(data)

    # Добавляем в очередь фона
    track_transaction(txid, wallet)

    new_limit = data[wallet]['limit'] + 10
    return UnlockResponse(
        success=True,
        message="Transaction received and being verified. Please wait ~15 sec.",
        newLimit=new_limit
    )

