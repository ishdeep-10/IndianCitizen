import requests

def get_data(url: str, headers: dict, data: dict):
    try:
        response = requests.post(url, headers=headers, json=data)
    
        # Check if request was successful
        response.raise_for_status()
    
        # Parse and print the response
        result = response.json()
        print("Success!")
        #print("Data:", result.get("data"))
        #print("Meta:", result.get("meta"))
        return result
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")