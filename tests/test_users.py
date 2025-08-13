import requests

def test_user_endpoint():
    # Define the URL
    url = "http://127.0.0.1:8000/users/"
    
    # Parameters to send with the request
    params = {'username': 'admin', 'password': 'qwerty'}
    
    # Send GET request
    response = requests.get(url, params=params)
    
    # Assert that the status code is 200
    assert response.status_code == 200

    # Optionally print response for debugging
    # print(response.text)  # Uncomment to see the empty response

def test_user_endpoint_unauthorized():
    # Define the URL
    url = "http://127.0.0.1:8000/users/"
    
    # Parameters to send with the request
    params = {'username': 'admin', 'password': 'admin'}
    
    # Send GET request
    response = requests.get(url, params=params)
    
    # Assert that the status code is 401 (Unauthorized)
    assert response.status_code == 401

    # Optionally print response for debugging (uncomment to view the response)
    # print(response.text)