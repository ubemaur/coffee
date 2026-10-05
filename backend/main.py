from decimal import Decimal

from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

PRICE_PER_ICED_COFFEE = Decimal("5.00")
total_bank = Decimal("0.00")

@app.get("/")
def root():
    return {"message": "Coffee Piggy Bank"}

@app.post("/coffee-price")
def set_iced_coffee_price(new_price: Decimal = Query(gt=0)):
    global PRICE_PER_ICED_COFFEE
    PRICE_PER_ICED_COFFEE = new_price
    return {"message": "Price updated!"}

@app.post("/deposit-money")
def deposit_money_into_bank(deposited_money: Decimal = Query(gt=0)):
    global total_bank
    total_bank += deposited_money
    return {"message": f"${deposited_money} deposited!"}

@app.post("/withdraw-money")
def withdraw_money_from_bank(withdraw_money: Decimal = Query(gt=0)):
    global total_bank
    if withdraw_money > total_bank:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    total_bank -= withdraw_money
    return {"message": f"${withdraw_money} withdrew!"}

@app.post("/buy-coffee")
def buy_coffee(number_of_coffees: int = Query(default=1, gt=0)):
    global total_bank
    cost = PRICE_PER_ICED_COFFEE*number_of_coffees
    if cost > total_bank:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    total_bank -= cost
    return {"message": f"Bought {number_of_coffees} coffee(s) for ${cost}"}

@app.get("/piggy-bank")
def calculate_coffees():
    total = total_bank
    coffees = total // PRICE_PER_ICED_COFFEE
    leftover = total % PRICE_PER_ICED_COFFEE

    return {
        "purchasable_coffees": int(coffees),
        "deposited": float(total),
        "price_per_iced_coffee": float(PRICE_PER_ICED_COFFEE),
        "money_left": float(leftover),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)