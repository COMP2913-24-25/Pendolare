# 
# Python testing implentation for Pendo.JourneyService using Pytest
# Author: Catherine Weightman
# Created: 12/02/2025
#

import pytest
from fastapi.testclient import TestClient
from src.journey_service import app, some_testing_function

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Journey"}

def test_view_endpoint():
    response = client.get("/view")
    assert response.status_code == 200
    assert response.json() == {"message": "View Journey"}

def test_create_endpoint():
    response = client.post("/create/")
    assert response.status_code == 200
    assert response.json() == "Create Journey"

def test_testing_function():
    # Arrange
    param = True

    # Act
    result = some_testing_function(param)

    # Assert
    assert result == param