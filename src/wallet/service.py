from typing import List
from uuid import UUID
from fastapi import HTTPException
from src.config.database import DbSession
from src.wallet.schema import WalletCreate, WalletUpdate
from src.wallet.models import WalletModel


def create(db_session: DbSession, wallet_input: WalletCreate) -> WalletModel:
    """Creates a wallet"""

    wallet_model = WalletModel(
        owner_email=wallet_input.owner_email,
    )

    db_session.add(wallet_model)
    db_session.commit()
    db_session.refresh(wallet_model)

    return wallet_model 


def update(db_session: DbSession, wallet_id: UUID, wallet_input: WalletUpdate) -> WalletModel:

    wallet_model = get_or_raise(db_session=db_session, wallet_id=wallet_id)
    
    wallet_data = wallet_model.to_dict()
    update_data = wallet_input.model_dump()

    for field in update_data:
        if field in wallet_data:
            setattr(wallet_model, field, update_data[field])
    
    db_session.commit()
    db_session.refresh(wallet_model)

    return wallet_model


def get_all(
        db_session: DbSession,
        limit: int,
        offset: int,
        owner_email: str | None
) -> List[WalletModel]:
    """Get all wallets"""

    query = db_session.query(WalletModel)
    if owner_email:
        query = query.filter(WalletModel.owner_email == owner_email)
    
    return query.limit(limit).offset(offset).all()


def get_or_raise(db_session: DbSession, wallet_id: UUID) -> WalletModel:
    """Get wallet or raise exception"""

    wallet_model = db_session.query(WalletModel).filter(WalletModel.id == wallet_id).first()
    if not wallet_model:
        raise HTTPException(status_code=400, detail=f"Wallet with id: '{wallet_id}' doesn't exist")
    return wallet_model 


def increase_balance(db_session: DbSession, wallet_id: UUID, amount: float, should_commit=False) -> WalletModel:
    """Increase wallet balance"""

    wallet_model = get_or_raise(db_session=db_session, wallet_id=wallet_id)
    wallet_model.balance = WalletModel.balance + amount # type: ignore

    db_session.flush()

    if should_commit:
        db_session.commit()
        db_session.refresh(wallet_model)

    return wallet_model


def decrease_balance(db_session: DbSession, wallet_id: UUID, amount: float, should_commit=False) -> WalletModel:
    """Decrease wallet balance"""

    wallet_model = get_or_raise(db_session=db_session, wallet_id=wallet_id)

    if wallet_model.balance < amount: # type: ignore
        raise HTTPException(status_code=400, detail=f"Can't decrease to negative balance")
    
    wallet_model.balance = WalletModel.balance - amount # type: ignore

    db_session.flush()

    if should_commit:
        db_session.commit()
        db_session.refresh(wallet_model)

    return wallet_model


def delete(db_session: DbSession, wallet_id: UUID) -> UUID:
    """Deletes an employee"""

    wallet_model = get_or_raise(db_session=db_session, wallet_id=wallet_id)

    db_session.delete(wallet_model)
    db_session.commit()

    return wallet_model
