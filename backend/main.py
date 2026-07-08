
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models import *

from storage import (
    group_counter,
    expense_counter,
    settlement_counter
)

import storage
import services

app = FastAPI(
    title="Expense Sharing API",
    version="1.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error"
        }
    )



# GROUPS

@app.post(
    "/groups",
    response_model=GroupResponse,
    status_code=201
)
def create_group(request: CreateGroupRequest):

    group = {
        "groupId": storage.group_counter,
        "name": request.name,
        "members": [101, 102, 103]
    }

    storage.group_counter += 1

    services.add_group(group)

    return {
        "groupId": group["groupId"],
        "name": group["name"]
    }


@app.get(
    "/groups/{groupId}",
    response_model=GroupResponse
)
def get_group(groupId: int):

    group = services.find_group(groupId)

    return {
        "groupId": group["groupId"],
        "name": group["name"]
    }


# EXPENSES

@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=201
)
def add_expense(request: AddExpenseRequest):

    expense = {
        "expenseId": storage.expense_counter,
        "groupId": request.groupId,
        "amount": request.amount,
        "paidBy": request.paidBy
    }

    storage.expense_counter += 1

    services.add_expense(expense)

    return {
        "expenseId": expense["expenseId"],
        "status": "CREATED"
    }


@app.get("/expenses")
def get_expenses():

    return services.get_all_expenses()



# BALANCES

@app.get(
    "/balances/{userId}",
    response_model=BalanceResponse
)
def get_balance(userId: int):

    return services.get_balance(userId)



# SETTLEMENTS

@app.post(
    "/settlements",
    response_model=SettlementResponse,
    status_code=201
)
def create_settlement(request: SettlementRequest):

    settlement = {
        "settlementId": storage.settlement_counter,
        "fromUser": request.fromUser,
        "toUser": request.toUser,
        "amount": request.amount
    }

    storage.settlement_counter += 1

    services.create_settlement(settlement)

    return {
        "settlementId": settlement["settlementId"],
        "status": "SUCCESS"
    }

