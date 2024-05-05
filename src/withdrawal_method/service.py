from uuid import UUID
from fastapi import HTTPException
from src.config.database import DbSession
from src.withdrawal_status.models import WithdrawalStatusModel


def get_or_raise(db_session: DbSession, withdrawal_status_id: int) -> WithdrawalStatusModel:
    """Get withdrawal method or raise exception"""

    withdrawal_status_model = db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.id == withdrawal_status_id).first()
    if not withdrawal_status_model:
        raise HTTPException(status_code=400, detail=f"Withdrawal status with id: '{withdrawal_status_id}' doesn't exist")
    return withdrawal_status_model 


def get_by_name_or_raise(db_session: DbSession, withdrawal_status_name: str) -> WithdrawalStatusModel:
    """Get withdrawal method or raise exception"""

    withdrawal_status_model = db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == withdrawal_status_name).first()
    if not withdrawal_status_model:
        raise HTTPException(status_code=400, detail=f"Withdrawal status with name: '{withdrawal_status_name}' doesn't exist")
    return withdrawal_status_model 


def get_crypto_method(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'crypto' withdrawal method"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "CRYPTO").first()


def get_fiat_method(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'fiat' withdrawal method"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "FIAT").first()
