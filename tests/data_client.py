import os
import requests
from typing import List, Dict, Optional


class DataServiceClient:
    """Client for fetching test data from the data service"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('DATA_SERVICE_URL', 'http://localhost:5000')

    def get_users(self, filter: Optional[Dict] = None) -> List[Dict]:
        """Fetch users, optionally filtered by labels.
        e.g. filter={"labels": ["ES", "male"]}
        """
        if filter:
            response = requests.post(f'{self.base_url}/users', json=filter)
        else:
            response = requests.get(f'{self.base_url}/users')
        response.raise_for_status()
        return response.json()
