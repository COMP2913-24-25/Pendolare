import requests
import sys
import time
import os

def check_kong():
    max_retries = 5
    retry_delay = 2
    kong_host = os.getenv('KONG_HOST', 'localhost')
    kong_url = f'http://{kong_host}:8000/status'

    for i in range(max_retries):
        try:
            print(f"Checking Kong at {kong_url}")
            response = requests.get(kong_url)
            if response.status_code == 200:
                print("Kong is accessible!")
                sys.exit(0)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1}/{max_retries}: Kong not ready yet: {str(e)}")
        time.sleep(retry_delay)
    
    print("Failed to connect to Kong")
    sys.exit(1)

if __name__ == "__main__":
    check_kong()
