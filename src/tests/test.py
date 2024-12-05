import requests
import json
from datetime import datetime

def test_attendance_api():
    """
    Test the attendance API endpoint
    """
    # API endpoint
    url = "http://192.168.2.120:6900/api/hpa/Paradise"
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "user": "admin",
        "pass": "1234",
        "name": "API_AttendanceList",
        "param": [
            "FromDate",
            "2021-02-01",
            "ToDate",
            "2025-02-24",
            "EmployeeID",
            "00001"
        ]
    }
    
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response JSON
        response_data = response.json()
        
        # Print response details
        print("Status Code:", response.status_code)
        print("\nResponse Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
        
        print("\nResponse Body:")
        print(json.dumps(response_data, indent=2))
        
        # Basic validation
        if response.status_code == 200:
            print("\nTest Result: SUCCESS ✓")
            print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
        else:
            print("\nTest Result: FAILURE ✗")
            print(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print("\nTest Result: ERROR ✗")
        print(f"Request failed: {str(e)}")
    except json.JSONDecodeError:
        print("\nTest Result: ERROR ✗")
        print("Failed to parse JSON response")
    except Exception as e:
        print("\nTest Result: ERROR ✗")
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    print("Starting API Test...")
    print("Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 50)
    test_attendance_api()