"""
`conftest.py` is special file that pytest recognize.
- Functions that are define in this file will be use as a parameter in test function with same name as param.
- PyTest run these functions and return the value to the test function params.

    
-> confest.py

@pytest.fixture
def api_client()
    return ApiClient()

-> test_module.py
def test_first(api_client):
    # Here api_client is ApiClient instance
    pass
"""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()