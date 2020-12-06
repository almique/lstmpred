from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Optional
from datetime import datetime
from typing import List, Optional
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_closing_price_app():
    response = client.post("/get_closing_price_app",
        json={"Year": 2015 , "Month": 7 , "Day": 20, "stockname": "ASIANPAINT"}
    )
    assert response.status_code == 422

def test_get_closing_price_app_week():
    response = client.post("/get_closing_price_app_week",
            json = {"Year": 2015 , "Month": 7 , "Day": 20, "stockname": "ASIANPAINT"}
    )
    assert response.status_code == 422

def test_best_time():
    response = client.post("/best_time",
            json = {"Year": "2020", "stockname": "ASIANPAINT"}
    )
    assert response.status_code == 422

def test_best_Stock():
    response = client.post("/best_Stock",
            json = {"Year": "2020", "stockname": ["ASIANPAINT", "ADANIPORTS", "AXISBANK", "BAJFINANCE", "BHARTIARTL", "BAJAJ-AUTO"]}
    )
    assert response.status_code == 422
