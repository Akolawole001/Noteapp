#!/usr/bin/env python3
"""
Comprehensive test script for Note Taking & To-Do List App.
Tests all API endpoints to verify full functionality.
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8003"
API_URL = f"{BASE_URL}/api"

# Test data
TEST_EMAIL = f"test_{datetime.now().timestamp()}@example.com"
TEST_PASSWORD = "TestPass123"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(name, status, details=""):
    """Print formatted test result."""
    symbol = "✓" if status else "✗"
    color = GREEN if status else RED
    print(f"{color}{symbol}{RESET} {name}")
    if details:
        print(f"  {YELLOW}{details}{RESET}")

def test_health_check():
    """Test 1: Health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        success = response.status_code == 200
        data = response.json()
        print_test(
            "Health Check",
            success,
            f"Status: {data.get('status')}, App: {data.get('app')}"
        )
        return success
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_register():
    """Test 2: User registration."""
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=5
        )
        success = response.status_code == 201
        if success:
            data = response.json()
            print_test(
                "User Registration",
                True,
                f"User ID: {data.get('id')}, Email: {data.get('email')}"
            )
        else:
            print_test("User Registration", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("User Registration", False, str(e))
        return False

def test_login():
    """Test 3: User login."""
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=5
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            token = data.get('access_token')
            print_test(
                "User Login",
                True,
                f"Token type: {data.get('token_type')}"
            )
            return token
        else:
            print_test("User Login", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("User Login", False, str(e))
        return None

def test_get_user_info(token):
    """Test 4: Get current user info."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/auth/me", headers=headers, timeout=5)
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Get User Info",
                True,
                f"Email: {data.get('email')}"
            )
        else:
            print_test("Get User Info", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Get User Info", False, str(e))
        return False

def test_create_note(token):
    """Test 5: Create a note."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        note_data = {
            "title": "Test Note",
            "content": "This is a test note created by the automated test script."
        }
        response = requests.post(
            f"{API_URL}/notes/",
            headers=headers,
            json=note_data,
            timeout=5
        )
        success = response.status_code == 201
        if success:
            data = response.json()
            print_test(
                "Create Note",
                True,
                f"Note ID: {data.get('id')}, Title: {data.get('title')}"
            )
            return data.get('id')
        else:
            print_test("Create Note", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Create Note", False, str(e))
        return None

def test_get_notes(token):
    """Test 6: Get all notes."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/notes/", headers=headers, timeout=5)
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Get Notes",
                True,
                f"Total notes: {len(data)}"
            )
        else:
            print_test("Get Notes", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Get Notes", False, str(e))
        return False

def test_update_note(token, note_id):
    """Test 7: Update a note."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {"title": "Updated Test Note"}
        response = requests.put(
            f"{API_URL}/notes/{note_id}",
            headers=headers,
            json=update_data,
            timeout=5
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Update Note",
                True,
                f"Updated title: {data.get('title')}"
            )
        else:
            print_test("Update Note", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Update Note", False, str(e))
        return False

def test_create_task(token):
    """Test 8: Create a task."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "todo"
        }
        response = requests.post(
            f"{API_URL}/tasks/",
            headers=headers,
            json=task_data,
            timeout=5
        )
        success = response.status_code == 201
        if success:
            data = response.json()
            print_test(
                "Create Task",
                True,
                f"Task ID: {data.get('id')}, Status: {data.get('status')}"
            )
            return data.get('id')
        else:
            print_test("Create Task", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Create Task", False, str(e))
        return None

def test_get_tasks(token):
    """Test 9: Get all tasks."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_URL}/tasks/", headers=headers, timeout=5)
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Get Tasks",
                True,
                f"Total tasks: {len(data)}"
            )
        else:
            print_test("Get Tasks", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Get Tasks", False, str(e))
        return False

def test_update_task(token, task_id):
    """Test 10: Update task status."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {"status": "in_progress"}
        response = requests.put(
            f"{API_URL}/tasks/{task_id}",
            headers=headers,
            json=update_data,
            timeout=5
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Update Task",
                True,
                f"New status: {data.get('status')}"
            )
        else:
            print_test("Update Task", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Update Task", False, str(e))
        return False

def test_create_event(token, task_id):
    """Test 11: Create a calendar event."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        start_time = datetime.now() + timedelta(hours=2)
        end_time = start_time + timedelta(hours=1)
        event_data = {
            "title": "Test Meeting",
            "description": "This is a test calendar event",
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "linked_task_id": task_id
        }
        response = requests.post(
            f"{API_URL}/calendar/events",
            headers=headers,
            json=event_data,
            timeout=5
        )
        success = response.status_code == 201
        if success:
            data = response.json()
            print_test(
                "Create Calendar Event",
                True,
                f"Event ID: {data.get('id')}, Linked Task: {data.get('linked_task_id')}"
            )
            return data.get('id')
        else:
            print_test("Create Calendar Event", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Create Calendar Event", False, str(e))
        return None

def test_get_events(token):
    """Test 12: Get calendar events."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/calendar/events",
            headers=headers,
            timeout=5
        )
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test(
                "Get Calendar Events",
                True,
                f"Total events: {len(data)}"
            )
        else:
            print_test("Get Calendar Events", False, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test("Get Calendar Events", False, str(e))
        return False

def test_delete_note(token, note_id):
    """Test 13: Delete a note."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(
            f"{API_URL}/notes/{note_id}",
            headers=headers,
            timeout=5
        )
        success = response.status_code == 204
        print_test(
            "Delete Note",
            success,
            "Note deleted successfully" if success else f"Status: {response.status_code}"
        )
        return success
    except Exception as e:
        print_test("Delete Note", False, str(e))
        return False

def main():
    """Run all tests."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Note Taking & To-Do List App - Functionality Test{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    print(f"{YELLOW}Testing server at: {BASE_URL}{RESET}\n")
    
    results = []
    
    # Test 1: Health check
    results.append(test_health_check())
    
    # Test 2: Registration
    results.append(test_register())
    
    # Test 3: Login
    token = test_login()
    results.append(token is not None)
    
    if not token:
        print(f"\n{RED}Login failed. Cannot continue with authenticated tests.{RESET}\n")
        return
    
    # Test 4: Get user info
    results.append(test_get_user_info(token))
    
    # Test 5-7: Note operations
    note_id = test_create_note(token)
    results.append(note_id is not None)
    results.append(test_get_notes(token))
    if note_id:
        results.append(test_update_note(token, note_id))
    
    # Test 8-10: Task operations
    task_id = test_create_task(token)
    results.append(task_id is not None)
    results.append(test_get_tasks(token))
    if task_id:
        results.append(test_update_task(token, task_id))
    
    # Test 11-12: Calendar operations
    event_id = test_create_event(token, task_id)
    results.append(event_id is not None)
    results.append(test_get_events(token))
    
    # Test 13: Delete operation
    if note_id:
        results.append(test_delete_note(token, note_id))
    
    # Summary
    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Total Tests:  {total_tests}")
    print(f"{GREEN}Passed:       {passed_tests}{RESET}")
    if failed_tests > 0:
        print(f"{RED}Failed:       {failed_tests}{RESET}")
    else:
        print(f"{GREEN}Failed:       {failed_tests}{RESET}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n{GREEN}✓ All tests passed! Your app is fully functional! 🎉{RESET}\n")
    elif success_rate >= 80:
        print(f"\n{YELLOW}⚠ Most tests passed. Check failed tests above.{RESET}\n")
    else:
        print(f"\n{RED}✗ Multiple tests failed. Please review the errors above.{RESET}\n")

if __name__ == "__main__":
    main()
