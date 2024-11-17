import requests
import logging
import os

class Config:
    # Load the API URL from environment variables or use a default value
    api_url = os.getenv('API_URL', "https://v3.football.api-sports.io")
    
    # Load the API key from environment variables; provide a default key for development
    api_key = os.getenv('API_KEY', 'your_test_api_key')

class APIClient:
    def __init__(self):
        """
        Initializes the APIClient with API details from Config.
        """
        # Get API URL and key from config
        self.base_url = Config.api_url
        self.api_key = Config.api_key
        self.timezone = "Europe/Istanbul"  # Set timezone as a constant

        # Validate API Key
        if not self.api_key:
            logging.error("API Key not found. Please provide a valid API key.")
            raise ValueError("API Key not found.")
        else:
            logging.info(f"API Key successfully retrieved: {self.api_key[:4]}****")

        # Set headers
        self.headers = {
            "x-apisports-key": self.api_key
        }

    def test_connection(self):
        """
        Tests the API connection.
        """
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raises exception on error
            logging.info("API connection successful!")  # Log success
            return True
        except requests.exceptions.RequestException as req_err:
            logging.error(f"API connection failed! Error: {req_err}")
            return False

    def send_request(self, endpoint, **kwargs):
        """
        Makes a general API request.
        :param endpoint: API endpoint to hit.
        :param kwargs: Optional parameters to send in the request.
        """
        # Construct full URL for the endpoint
        url = f"{self.base_url}/{endpoint}"

        try:
            # Send GET request with query parameters
            response = requests.get(url, headers=self.headers, params=kwargs, timeout=10)
            response.raise_for_status()  # Check for HTTP errors

            # Log the full URL with query parameters
            logging.info(f"Full URL with params: {response.url}")
            logging.info("API request successful!")

            return response.json()  # Return the response in JSON format
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred during the API request: {req_err}")

        return {"error": "API request failed."}