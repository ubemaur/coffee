from decimal import Decimal

from fastapi import FastAPI, Query

app = FastAPI()

PRICE_PER_ICED_COFFEE = Decimal("5.00")
total_bank = Decimal("0.00")

@app.get("/")
def root():
    return {"message": "Coffee piggy bank"}

@app.post("/coffee-price")
def set_iced_coffee_price(new_price: float):
    global PRICE_PER_ICED_COFFEE
    PRICE_PER_ICED_COFFEE = Decimal(str(new_price))
    return {"message": "Price updated!"}

@app.post("/deposit-money")
def deposit_money_into_bank(deposited_money: float):
    global total_bank
    total_bank += Decimal(str(deposited_money))
    return {"message": f"${deposited_money} deposited!"}

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