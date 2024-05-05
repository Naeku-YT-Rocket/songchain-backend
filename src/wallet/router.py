from typing import List, Optional
from uuid import UUID
from src.wallet.service import create, get_all, delete, get_or_raise, update
from src.config.database import DbSession
from fastapi import APIRouter
from src.wallet.schema import WalletCreate, WalletRead, WalletUpdate


router = APIRouter(
    prefix="/wallet"
)


@router.post("/", tags=["wallet"], response_model=WalletRead)
def create_wallet(
    db_session: DbSession,
    wallet_input: WalletCreate
):

    return create(db_session=db_session, wallet_input=wallet_input)


@router.get("/", tags=["wallet"], response_model=List[WalletRead])
def get_wallets(
    db_session: DbSession,
    owner_email: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):

    return get_all(
        db_session=db_session,
        limit=limit,
        offset=offset,
        owner_email=owner_email
    )


@router.get("/{wallet_id}", tags=["wallet"], response_model=WalletRead)
def get_wallet(
    db_session: DbSession,
    wallet_id: UUID
):

    return get_or_raise(db_session=db_session, wallet_id=wallet_id)



@router.patch("/{wallet_id}", tags=["wallet"])
def update_wallet(
    db_session: DbSession,
    wallet_id: UUID,
    wallet_input: WalletUpdate
):
    
    return update(db_session=db_session, wallet_id=wallet_id, wallet_input=wallet_input)


@router.delete("/{wallet_id}", tags=["wallet"], response_model=UUID)
def delete_wallet(
    db_session: DbSession,
    wallet_id: UUID,
):

    return delete(db_session=db_session, wallet_id=wallet_id)

