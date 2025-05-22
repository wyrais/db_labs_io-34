import requests
import json
from datetime import date

# Базовый URL API
BASE_URL = "http://localhost:8000"

def test_health():
    """Тест health check эндпоинта"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_users():
    """Тест получения списка пользователей"""
    print("\n=== Testing GET /users ===")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Users found: {len(response.json())}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_user_by_id(user_id=1):
    """Тест получения пользователя по ID"""
    print(f"\n=== Testing GET /users/{user_id} ===")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_user():
    """Тест создания нового пользователя"""
    print("\n=== Testing POST /users ===")
    new_user = {
        "username": "test_user",
        "email": "test@example.com",
        "password_hash": "$2a$10$testhashedpassword"
    }
    try:
        response = requests.post(f"{BASE_URL}/users", json=new_user)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_projects():
    """Тест получения списка проектов"""
    print("\n=== Testing GET /projects ===")
    try:
        response = requests.get(f"{BASE_URL}/projects")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Projects found: {len(response.json())}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_project():
    """Тест создания нового проекта"""
    print("\n=== Testing POST /projects ===")
    new_project = {
        "title": "Test Project",
        "description": "This is a test project",
        "start_date": str(date.today()),
        "end_date": None,
        "status": "planned"
    }
    try:
        response = requests.post(f"{BASE_URL}/projects", json=new_project)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_docs():
    """Проверка доступности документации API"""
    print("\n=== Testing API Documentation ===")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"Swagger UI available: {response.status_code == 200}")
        
        response = requests.get(f"{BASE_URL}/redoc")
        print(f"ReDoc available: {response.status_code == 200}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests():
    """Запуск всех тестов"""
    print("Starting API Tests...")
    print(f"Testing API at: {BASE_URL}")
    
    tests = [
        test_health,
        test_get_users,
        test_get_user_by_id,
        test_get_projects,
        test_create_user,
        test_create_project,
        test_api_docs
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"Test {test.__name__} failed with error: {e}")
            results.append((test.__name__, False))
    
    print("\n=== Test Summary ===")
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    print(f"\nTotal: {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    run_all_tests()