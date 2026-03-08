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

Test Database:
- Pytest-django creates the test database once per session and uses transactional rollbacks 
- to provide a clean environment for each individual test.
    
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
import pytest
from store.models import Collection
from model_bakery import baker


@pytest.fixture
def create_collection(api_client):
    def create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return create_collection


@pytest.fixture
def get_collection(api_client):
    def get_collection(collection_id):
        return api_client.get(f'/store/collections/{collection_id}/')
    return get_collection

# Always start name with Test, otherwise pytest will recognize it.
@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip # Skip test
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):
        # Arrange
        authenticate(user={})
        
        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    
    def test_if_data_is_invalid_returns_400(self, authenticate, create_collection):
        # Arrange
        authenticate(user=User(is_staff=True))
        
        # Act
        response = create_collection({'title': ''})

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get('title', None) is not None

    def test_if_data_is_valid_returns_400(self, authenticate, create_collection):
        # Arrange
        authenticate(user=User(is_staff=True))
        
        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('id', 0) > 0


@pytest.mark.django_db
class TestReteriveCollection:
    def test_if_collection_exists_return_200(self, get_collection):
        """
        # response = create_collection({'title': 'a'})

        What is bad with this approach is that it also testing the POST endpoint.
        If POST endpoint fail, it will also fails this test, which is not related to
        each other.
        """
        
        # Collection.objects.create(title="a") # Make the test more noisy, if has mutiple fields to populate.

        collection = baker.make(Collection)

        response = get_collection(collection.id)

        assert response.status_code == status.HTTP_200_OK
        # assert response.data.get('id', 0) == collection.id
        # assert response.data.get('title', None) == collection.title

        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'product_count': 0
        }

    def test_if_collection_not_exists_return_404(self, get_collection):
        response = get_collection(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND