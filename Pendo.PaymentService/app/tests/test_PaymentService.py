# 
# Python testing implentation for Pendo.PaymentService using Pytest
# Author: Alexander McCall
# Created: 12/02/2025
#

import pytest
from src.PaymentService import some_testing_function

def test_testing_function():
    # Arrange
    param = True

    # Act
    result = some_testing_function(param)

    # Assert
    assert result == param