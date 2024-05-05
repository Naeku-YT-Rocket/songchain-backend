from typing import List, Optional
from uuid import UUID
from src.withdrawal.schema import WithdrawalCreate, WithdrawalRead
from src.withdrawal.service import create, get_all, pay, reject, cancel
from src.config.database import DbSession
from fastapi import APIRouter


router = APIRouter(
    prefix="/withdrawal"
)

@router.get("/", tags=["withdrawal"], response_model=List[WithdrawalRead])
def get_withdrawals(
    db_session: DbSession,
    wallet_id: Optional[UUID] = None,
    email: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):

    withdrawals_model = get_all(
        db_session=db_session,
        limit=limit,
        offset=offset,
        email=email,
        wallet_id=wallet_id
    )

    return withdrawals_model


@router.post("/", tags=["withdrawal"], response_model=WithdrawalRead)
def create_withdrawal(
    db_session: DbSession,
    withdrawal_input: WithdrawalCreate
):

    withdrawal_model = create(
        db_session=db_session,
        withdrawal_input=withdrawal_input
    )

    return withdrawal_model


@router.post("/{withdrawal_id}/pay", tags=["withdrawal"], response_model=WithdrawalRead)
def pay_withdrawal(
    db_session: DbSession,
    withdrawal_id: UUID
):
    withdrawal_model = pay(
        db_session=db_session,
        withdrawal_id=withdrawal_id
    )

    return withdrawal_model


@router.post("/{withdrawal_id}/reject", tags=["withdrawal"], response_model=WithdrawalRead)
def reject_withdrawal(
    db_session: DbSession,
    withdrawal_id: UUID
):
    withdrawal_model = reject(
        db_session=db_session,
        withdrawal_id=withdrawal_id
    )

    return withdrawal_model


@router.post("/{withdrawal_id}/cancel", tags=["withdrawal"], response_model=WithdrawalRead)
def cancel_withdrawal(
    db_session: DbSession,
    withdrawal_id: UUID
):
    withdrawal_model = cancel(
        db_session=db_session,
        withdrawal_id=withdrawal_id
    )

    return withdrawal_model
