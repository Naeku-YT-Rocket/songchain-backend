from uuid import UUID
from fastapi import HTTPException
from src.config.database import DbSession
from src.withdrawal_status.models import WithdrawalStatusModel


def get_or_raise(db_session: DbSession, withdrawal_status_id: int) -> WithdrawalStatusModel:
    """Get withdrawal status or raise exception"""

    withdrawal_status_model = db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.id == withdrawal_status_id).first()
    if not withdrawal_status_model:
        raise HTTPException(status_code=400, detail=f"Withdrawal status with id: '{withdrawal_status_id}' doesn't exist")
    return withdrawal_status_model 


def get_requested_status(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'offered' listing status"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "REQUESTED").first()


def get_paid_status(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'paid' listing status"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "PURCHASED").first()


def get_rejected_status(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'rejected' listing status"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "REJECTED").first()


def get_cancelled_status(db_session: DbSession) -> WithdrawalStatusModel:
    """Get 'cancelled' listing status"""

    return db_session.query(WithdrawalStatusModel).filter(WithdrawalStatusModel.name == "CANCELLED").first()
