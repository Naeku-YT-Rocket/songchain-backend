"""
    Withdrawal service

    Although _check_status_is_requested already implements shared logic, since 
    all functions are similar in nature, further logic sharing between functions
    may be applied. Still open to debate.

    _check_satus_is_requested function assumes request status is spelled 'REQUESTED'.
    Perhaps I should safely reference this status by making sure the name will always 
    correspond to the database name.
"""

from src.config.database import DbSession
from src.withdrawal.schema import WithdrawalCreate
from typing import List
from uuid import UUID
from fastapi import HTTPException
from src.config.database import DbSession
from src.wallet import service as wallet_service
from src.withdrawal.models import WithdrawalModel
from src.withdrawal_status import service as withdrawal_status_service
from src.withdrawal_method import service as withdrawal_method_service
from src.wallet.models import WalletModel


def _check_status_is_requested(withdrawal_model: WithdrawalModel):
    """Check withdrawal status is requested"""

    if withdrawal_model.withdrawal_status.name != "REQUESTED":
        raise HTTPException(400, "Withdrawal must be request in order to be cancelled")


def create(db_session: DbSession, withdrawal_input: WithdrawalCreate) -> WithdrawalModel:
    """Create withdrawal"""

    wallet_model = wallet_service.get_or_raise(db_session=db_session, wallet_id=withdrawal_input.wallet.id)

    if wallet_model.balance < withdrawal_input.amount: # type: ignore
        raise HTTPException(status_code=400, detail="Amount to withdraw can't be higher than balance in wallet")

    withdrawal_status_model = withdrawal_status_service.get_requested_status(db_session=db_session)
    withdrawal_method_model = withdrawal_method_service.get_by_name_or_raise(db_session=db_session, withdrawal_status_name=withdrawal_input.withdrawal_method.name)

    withdraw_model = WithdrawalModel(
        amount=withdrawal_input.amount,
        wallet=wallet_model,
        withdrawal_status=withdrawal_status_model,
        withdrawal_method=withdrawal_method_model
    )

    db_session.add(withdraw_model)
    db_session.flush()

    wallet_service.decrease_balance(
        db_session=db_session,
        wallet_id=withdrawal_input.wallet.id,
        amount=withdrawal_input.amount
    )

    db_session.commit()
    db_session.refresh(withdraw_model)

    return withdraw_model


def pay(db_session: DbSession, withdrawal_id: UUID) -> WithdrawalModel:
    """Pay a withdrawal"""

    withdrawal_model = get_or_raise(db_session=db_session, withdrawal_id=withdrawal_id)

    _check_status_is_requested(withdrawal_model=withdrawal_model)
    
    withdrawal_status_model = withdrawal_status_service.get_paid_status(db_session=db_session)

    withdrawal_model.withdrawal_status = withdrawal_status_model
    
    db_session.add(withdrawal_model)
    db_session.commit()
    db_session.refresh(withdrawal_model)

    return withdrawal_model


def reject(db_session: DbSession, withdrawal_id: UUID) -> WithdrawalModel:
    """Reject a withdrawal"""

    withdrawal_model = get_or_raise(db_session=db_session, withdrawal_id=withdrawal_id)

    _check_status_is_requested(withdrawal_model=withdrawal_model)
    
    withdrawal_status_model = withdrawal_status_service.get_rejected_status(db_session=db_session)

    withdrawal_model.withdrawal_status = withdrawal_status_model

    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=withdrawal_model.wallet_id, # type: ignore
        amount=withdrawal_model.amount # type: ignore
    )
    
    db_session.add(withdrawal_model)
    db_session.commit()
    db_session.refresh(withdrawal_model)

    return withdrawal_model


def cancel(db_session: DbSession, withdrawal_id: UUID) -> WithdrawalModel:
    """Cancel withdrawal"""

    withdrawal_model = get_or_raise(db_session=db_session, withdrawal_id=withdrawal_id)

    _check_status_is_requested(withdrawal_model=withdrawal_model)
    
    withdrawal_status_model = withdrawal_status_service.get_cancelled_status(db_session=db_session)

    withdrawal_model.withdrawal_status = withdrawal_status_model

    wallet_service.increase_balance(
        db_session=db_session,
        wallet_id=withdrawal_model.wallet_id, # type: ignore
        amount=withdrawal_model.amount # type: ignore
    )

    db_session.add(withdrawal_model)
    db_session.commit()
    db_session.refresh(withdrawal_model)

    return withdrawal_model


def get_all(
    db_session: DbSession,
    limit: int,
    offset: int,
    email: str | None,
    wallet_id: UUID | None
) -> List[WithdrawalModel]:
    """Get all withdrawals"""

    query = db_session.query(WithdrawalModel)
    if wallet_id:
        query = query.filter(WithdrawalModel.wallet_id == wallet_id)
    if email:
        query = query.join(WalletModel).filter(WalletModel.owner_email == email)

    return query.limit(limit).offset(offset).all()


def get_or_raise(db_session: DbSession, withdrawal_id: UUID) -> WithdrawalModel:
    """Get withdrawals or raise exception"""

    withdrawal_model = db_session.query(WithdrawalModel).filter(WithdrawalModel.id == withdrawal_id).first()
    if not withdrawal_model:
        raise HTTPException(status_code=400, detail=f"Withdrawal with id: '{withdrawal_id}' doesn't exist")
    return withdrawal_model 
