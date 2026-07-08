from fastapi import HTTPException

from storage import (
    groups,
    expenses,
    settlements,
    balances
)


def find_group(group_id: int):
    for group in groups:
        if group["groupId"] == group_id:
            return group

    raise HTTPException(
        status_code=404,
        detail="Group not found"
    )


def initialize_user(user_id: int):
    if user_id not in balances:
        balances[user_id] = {
            "owed": 0.0,
            "receivable": 0.0
        }


def add_group(group):
    groups.append(group)
    return group


def add_expense(expense):
    group = find_group(expense["groupId"])

    members = group["members"]

    if expense["paidBy"] not in members:
        raise HTTPException(
            status_code=404,
            detail="User not found in group"
        )

    share = expense["amount"] / len(members)

    initialize_user(expense["paidBy"])

    for member in members:
        initialize_user(member)

        if member == expense["paidBy"]:
            balances[member]["receivable"] += (
                expense["amount"] - share
            )
        else:
            balances[member]["owed"] += share

    expenses.append(expense)

    return expense


def get_all_expenses():
    return expenses


def get_balance(user_id: int):
    initialize_user(user_id)

    return {
        "userId": user_id,
        "totalOwed": round(
            balances[user_id]["owed"],
            2
        ),
        "totalReceivable": round(
            balances[user_id]["receivable"],
            2
        )
    }


def create_settlement(settlement):
    initialize_user(settlement["fromUser"])
    initialize_user(settlement["toUser"])

    amount = settlement["amount"]

    balances[settlement["fromUser"]]["owed"] = max(
        0,
        balances[settlement["fromUser"]]["owed"] - amount
    )

    balances[settlement["toUser"]]["receivable"] = max(
        0,
        balances[settlement["toUser"]]["receivable"] - amount
    )

    settlements.append(settlement)

    return settlement