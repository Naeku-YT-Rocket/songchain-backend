from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.database import engine
from src.config.database import Base
from src.digital_asset.router import router as digital_asset_router
from src.wallet.router import router as wallet_router
from src.partition.router import router as partition_router
from src.withdrawal.router import router as withdrawal_router
from src.partition_event.router import router as partition_event_router
from src.royalty.router import router as royalty_router
from src.royalty_claim.router import router as royalty_claim_router


Base.metadata.create_all(bind=engine) # type: ignore

app = FastAPI(
    responses={
        "200": {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "ok"
                    }
                }
            }
        }
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
def health():
    return {
        "detail": "online"
    }

app.include_router(wallet_router)
app.include_router(withdrawal_router)
app.include_router(digital_asset_router)
app.include_router(partition_router)
app.include_router(partition_event_router)
app.include_router(royalty_router)
app.include_router(royalty_claim_router)
