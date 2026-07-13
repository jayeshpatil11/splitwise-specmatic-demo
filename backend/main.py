
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

# Actuator

from fastapi.routing import APIRoute

@app.get("/actuator/mappings", tags=["Actuator"], summary="List all registered API endpoints", operation_id="actuatorMappings")
def actuator_mappings():
    mappings = []

    for route in app.routes:
        if isinstance(route, APIRoute):
            mappings.append({
                "path": route.path,
                "methods": sorted(list(route.methods)),
                "name": route.name,
                "summary": route.summary if route.summary else None ,
                "operationId": route.operation_id or route.endpoint.__name__
            })

    mappings.sort(key=lambda x: x["path"])

    return {
        "application": "expense-sharing-api",
        "framework": "FastAPI",
        "totalEndpoints": len(mappings),
        "mappings": mappings
    }



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
    status_code=201,
    operation_id="createGroup",
    summary="Create Group"
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
    response_model=GroupResponse,
    operation_id="getGroup",
    summary="Get Group"
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
    status_code=201,
    operation_id="addExpense",
    summary="Add Expense"
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


@app.get(
    "/expenses",
    operation_id="getExpenses",
    summary="Get Expenses"
    )
def get_expenses():

    return services.get_all_expenses()



# BALANCES

@app.get(
    "/balances/{userId}",
    response_model=BalanceResponse,
    operation_id="getBalance",
    summary="View Balance"
)
def get_balance(userId: int):

    return services.get_balance(userId)



# SETTLEMENTS

@app.post(
    "/settlements",
    response_model=SettlementResponse,
    status_code=201,
    operation_id="createSettlement",
    summary="Create Settlement"
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

