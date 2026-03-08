""" 
    Always test Behaviour, not the implementation

    Way to sturcture a test
    AAA (Arrange, Act, Assertion)

    Arrange:
        - Make DB connection etc.
    Act:
        - Perform the Behaviour
    Assert
        - Check the Behaviour
    
Run specific Test:
- pytest store/tests
- pytest store/tests/test_collections.py
- pytest store/tests/test_collections.py::TestCreateCollection
- pytest store/tests/test_collections.py::TestCreateCollection::test_if_user_is_anonymous_returns_401
- pytest -f anonymous # Test include anonymous name
        

Run Conitnous Testing via Pytest-Watcher
- ptw
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
import pytest

# Always start name with Test, otherwise pytest will recognize it.
@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip # Skip test
    def test_if_user_is_anonymous_returns_401(self):

        # Act
        client = APIClient()
        response = client.post('/store/collections/', {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self):

        # Act
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/store/collections/', {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    
    def test_if_data_is_invalid_returns_400(self):

        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': ''})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('title', None) is not None

    def test_if_data_is_valid_returns_400(self):

        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collections/', {'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('id', 0) > 0