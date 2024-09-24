"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import pytest

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

@pytest.fixture()
def client():
  return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndPoints:
    """Test cases for Counter-related endpoints"""

    def test_create_a_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_a_counter(self, client):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_201_CREATED
        result = client.post('/counters/bar')
        assert result.status_code == status.HTTP_409_CONFLICT

    def test_update_a_counter(self, client):
        """It should update a counter"""
        # Step 1: Make a call to Create a counter.
        result = client.post('/counters/boo')
        assert result.status_code == status.HTTP_201_CREATED
        # Step 2: Ensure that it returned a successful return code.
        data = result.get_json()
        assert data['boo'] == 0
        # Step 3: Check the counter value as a baseline.
        baseline = data['boo']
        # Step 4: Update the counter
        result = client.put('/counters/boo')
        assert result.status_code == status.HTTP_200_OK
        # Step 5: Ensure that it returned a successful return code.
        data = result.get_json()
        # Step 6: Check that the counter value is one more than the baseline you measured in step 3.
        assert data['boo'] == baseline + 1

    def test_update_non_existent_counter(self, client):
        """It should return 404 for updating a non-existent counter"""
        result = client.put('/counters/nonexistent')
        assert result.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_counter(self, client):
        """It should delete a counter"""
        # Create a counter first
        result = client.post('/counters/test')
        assert result.status_code == status.HTTP_201_CREATED
        # Delete the counter
        response = client.delete('/counters/test')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Verify the counter is deleted
        result = client.get('/counters/test')
        assert result.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_non_existent_counter(self, client):
        """It should return 404 for deleting a non-existent counter"""
        response = client.delete('/counters/nonexistent')
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_a_counter(client):
    """It should read a counter"""
    result = client.post('/counters/boo2')
    assert result.status_code == status.HTTP_201_CREATED
    data = result.get_json()
    assert data['boo2'] == 0
    result = client.get('/counters/boo2')
    assert result.status_code == status.HTTP_200_OK
    data = result.get_json()
    assert data['boo2'] == 0
        
def test_read_nonexistent_counter(client):
    """It should return 404 for reading a nonexistent counter"""
    result = client.get('/counters/nonexistent')
    assert result.status_code == status.HTTP_404_NOT_FOUND