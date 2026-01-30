#!/usr/bin/env python3
"""
Comprehensive End-to-End Test Suite for NoteApp
Tests all features including security
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Optional

# Configuration
BASE_URL = "http://127.0.0.1:8003"
TEST_EMAIL = f"e2etest{int(time.time())}@example.com"
TEST_PASSWORD = "SecureTest123!"

# Colors for terminal output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
BOLD = '\033[1m'
NC = '\033[0m'  # No Color

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.tests.append({
            "name": name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
            print(f"{GREEN}✅ PASS{NC}: {name}")
        else:
            self.failed += 1
            print(f"{RED}❌ FAIL{NC}: {name}")
        if message:
            print(f"  ℹ️  {message}")
    
    def print_summary(self):
        total = self.passed + self.failed
        percentage = (self.passed * 100 // total) if total > 0 else 0
        
        print("\n" + "=" * 50)
        print(f"{BOLD}📈 TEST RESULTS SUMMARY{NC}")
        print("=" * 50)
        print(f"\nTotal Tests:     {total}")
        print(f"{GREEN}Passed:          {self.passed}{NC}")
        print(f"{RED}Failed:          {self.failed}{NC}")
        print(f"Success Rate:    {percentage}%\n")
        
        if self.failed == 0:
            print(f"{GREEN}{'=' * 50}{NC}")
            print(f"{GREEN}🎉 ALL TESTS PASSED!{NC}")
            print(f"{GREEN}✅ Application is fully functional{NC}")
            print(f"{GREEN}✅ All features working correctly{NC}")
            print(f"{GREEN}✅ Security measures in place{NC}")
            print(f"{GREEN}✅ Ready for deployment{NC}")
            print(f"{GREEN}{'=' * 50}{NC}")
        else:
            print(f"{RED}{'=' * 50}{NC}")
            print(f"{RED}⚠️  SOME TESTS FAILED{NC}")
            print(f"{YELLOW}Please review the errors above{NC}")
            print(f"{RED}{'=' * 50}{NC}")

results = TestResults()

def print_header(title: str):
    print(f"\n{'━' * 50}")
    print(f"{BLUE}{BOLD}{title}{NC}")
    print('━' * 50)

def main():
    print("=" * 50)
    print("🧪 NoteApp End-to-End Test Suite")
    print("=" * 50)
    print(f"\n📍 Testing: {BASE_URL}")
    print(f"👤 Test User: {TEST_EMAIL}\n")
    
    # Store tokens and IDs
    access_token: Optional[str] = None
    user_id: Optional[int] = None
    note_id: Optional[int] = None
    task_id: Optional[int] = None
    event_id: Optional[int] = None
    
    # ========================================
    # STEP 1: Health Check
    # ========================================
    print_header("🏥 STEP 1: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200 and "healthy" in response.text:
            results.add_test("Health endpoint responds", True, f"Status: {response.status_code}")
        else:
            results.add_test("Health endpoint responds", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Health endpoint responds", False, str(e))
    
    # ========================================
    # STEP 2: User Registration
    # ========================================
    print_header("🔐 STEP 2: User Registration")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=5
        )
        if response.status_code in [200, 201]:
            data = response.json()
            user_id = data.get("id")
            results.add_test("User registration successful", True, f"User ID: {user_id}")
        else:
            results.add_test("User registration successful", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        results.add_test("User registration successful", False, str(e))
    
    # ========================================
    # STEP 3: User Login & JWT Token
    # ========================================
    print_header("🔑 STEP 3: User Login & JWT Token")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            if access_token:
                results.add_test("User login successful", True)
                results.add_test("JWT token generated", True, f"Token: {access_token[:30]}...")
            else:
                results.add_test("User login successful", False, "No access token in response")
        else:
            results.add_test("User login successful", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("User login successful", False, str(e))
    
    if not access_token:
        print(f"\n{RED}⚠️  Cannot continue without access token{NC}")
        results.print_summary()
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # ========================================
    # STEP 4: Security Tests
    # ========================================
    print_header("🛡️  STEP 4: Security Tests")
    
    # Test 4.1: Unauthorized access
    try:
        response = requests.get(f"{BASE_URL}/api/notes", timeout=5)
        if response.status_code in [401, 403]:
            results.add_test("Blocks access without token", True, f"HTTP {response.status_code}")
        else:
            results.add_test("Blocks access without token", False, f"HTTP {response.status_code}")
    except Exception as e:
        results.add_test("Blocks access without token", False, str(e))
    
    # Test 4.2: Invalid token
    try:
        response = requests.get(
            f"{BASE_URL}/api/notes",
            headers={"Authorization": "Bearer invalid_token_12345"},
            timeout=5
        )
        if response.status_code in [401, 403]:
            results.add_test("Rejects invalid token", True, f"HTTP {response.status_code}")
        else:
            results.add_test("Rejects invalid token", False, f"HTTP {response.status_code}")
    except Exception as e:
        results.add_test("Rejects invalid token", False, str(e))
    
    # Test 4.3: CORS headers
    try:
        response = requests.options(f"{BASE_URL}/health", timeout=5)
        cors_header = response.headers.get("Access-Control-Allow-Origin")
        if cors_header:
            results.add_test("CORS headers configured", True, f"Origin: {cors_header}")
        else:
            results.add_test("CORS headers configured", False, "No CORS headers found")
    except Exception as e:
        results.add_test("CORS headers configured", False, str(e))
    
    # ========================================
    # STEP 5: Notes CRUD Operations
    # ========================================
    print_header("📝 STEP 5: Notes CRUD Operations")
    
    # Test 5.1: Create Note
    try:
        response = requests.post(
            f"{BASE_URL}/api/notes",
            headers=headers,
            json={"title": "Test Note", "content": "This is a test note content"},
            timeout=5
        )
        if response.status_code in [200, 201]:
            data = response.json()
            note_id = data.get("id")
            results.add_test("Create note", True, f"Note ID: {note_id}")
        else:
            results.add_test("Create note", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        results.add_test("Create note", False, str(e))
    
    # Test 5.2: Get all notes
    try:
        response = requests.get(f"{BASE_URL}/api/notes", headers=headers, timeout=5)
        if response.status_code == 200:
            notes = response.json()
            note_count = len(notes) if isinstance(notes, list) else 0
            results.add_test("Get all notes", True, f"Total notes: {note_count}")
        else:
            results.add_test("Get all notes", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Get all notes", False, str(e))
    
    # Test 5.3: Get specific note
    if note_id:
        try:
            response = requests.get(f"{BASE_URL}/api/notes/{note_id}", headers=headers, timeout=5)
            if response.status_code == 200:
                results.add_test("Get note by ID", True)
            else:
                results.add_test("Get note by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Get note by ID", False, str(e))
    
    # Test 5.4: Update note
    if note_id:
        try:
            response = requests.put(
                f"{BASE_URL}/api/notes/{note_id}",
                headers=headers,
                json={"title": "Updated Test Note", "content": "Updated content"},
                timeout=5
            )
            if response.status_code == 200:
                results.add_test("Update note", True)
            else:
                results.add_test("Update note", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Update note", False, str(e))
    
    # Test 5.5: Delete note
    if note_id:
        try:
            response = requests.delete(f"{BASE_URL}/api/notes/{note_id}", headers=headers, timeout=5)
            if response.status_code in [200, 204]:
                results.add_test("Delete note", True, f"HTTP {response.status_code}")
            else:
                results.add_test("Delete note", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Delete note", False, str(e))
    
    # ========================================
    # STEP 6: Tasks CRUD Operations
    # ========================================
    print_header("✅ STEP 6: Tasks CRUD Operations")
    
    # Test 6.1: Create Task
    try:
        response = requests.post(
            f"{BASE_URL}/api/tasks",
            headers=headers,
            json={
                "title": "Test Task",
                "description": "Test task description",
                "status": "pending",
                "due_date": "2026-02-15T10:00:00"
            },
            timeout=5
        )
        if response.status_code in [200, 201]:
            data = response.json()
            task_id = data.get("id")
            results.add_test("Create task", True, f"Task ID: {task_id}")
        else:
            results.add_test("Create task", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        results.add_test("Create task", False, str(e))
    
    # Test 6.2: Get all tasks
    try:
        response = requests.get(f"{BASE_URL}/api/tasks", headers=headers, timeout=5)
        if response.status_code == 200:
            tasks = response.json()
            task_count = len(tasks) if isinstance(tasks, list) else 0
            results.add_test("Get all tasks", True, f"Total tasks: {task_count}")
        else:
            results.add_test("Get all tasks", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Get all tasks", False, str(e))
    
    # Test 6.3: Update task status
    if task_id:
        try:
            response = requests.put(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers=headers,
                json={
                    "title": "Test Task",
                    "description": "Updated description",
                    "status": "completed",
                    "due_date": "2026-02-15T10:00:00"
                },
                timeout=5
            )
            if response.status_code == 200:
                results.add_test("Update task status to completed", True)
            else:
                results.add_test("Update task status to completed", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Update task status to completed", False, str(e))
    
    # Test 6.4: Delete task
    if task_id:
        try:
            response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=headers, timeout=5)
            if response.status_code in [200, 204]:
                results.add_test("Delete task", True, f"HTTP {response.status_code}")
            else:
                results.add_test("Delete task", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Delete task", False, str(e))
    
    # ========================================
    # STEP 7: Calendar Events CRUD
    # ========================================
    print_header("📅 STEP 7: Calendar Events CRUD")
    
    # Test 7.1: Create Event
    try:
        response = requests.post(
            f"{BASE_URL}/api/calendar",
            headers=headers,
            json={
                "title": "Test Event",
                "description": "Test event description",
                "start_time": "2026-02-15T10:00:00",
                "end_time": "2026-02-15T11:00:00"
            },
            timeout=5
        )
        if response.status_code in [200, 201]:
            data = response.json()
            event_id = data.get("id")
            results.add_test("Create calendar event", True, f"Event ID: {event_id}")
        else:
            results.add_test("Create calendar event", False, f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        results.add_test("Create calendar event", False, str(e))
    
    # Test 7.2: Get all events
    try:
        response = requests.get(f"{BASE_URL}/api/calendar", headers=headers, timeout=5)
        if response.status_code == 200:
            events = response.json()
            event_count = len(events) if isinstance(events, list) else 0
            results.add_test("Get all calendar events", True, f"Total events: {event_count}")
        else:
            results.add_test("Get all calendar events", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Get all calendar events", False, str(e))
    
    # Test 7.3: Update event
    if event_id:
        try:
            response = requests.put(
                f"{BASE_URL}/api/calendar/{event_id}",
                headers=headers,
                json={
                    "title": "Updated Event",
                    "description": "Updated event description",
                    "start_time": "2026-02-15T14:00:00",
                    "end_time": "2026-02-15T15:00:00"
                },
                timeout=5
            )
            if response.status_code == 200:
                results.add_test("Update calendar event", True)
            else:
                results.add_test("Update calendar event", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Update calendar event", False, str(e))
    
    # Test 7.4: Delete event
    if event_id:
        try:
            response = requests.delete(f"{BASE_URL}/api/calendar/{event_id}", headers=headers, timeout=5)
            if response.status_code in [200, 204]:
                results.add_test("Delete calendar event", True, f"HTTP {response.status_code}")
            else:
                results.add_test("Delete calendar event", False, f"Status: {response.status_code}")
        except Exception as e:
            results.add_test("Delete calendar event", False, str(e))
    
    # ========================================
    # STEP 8: Data Isolation Test
    # ========================================
    print_header("🔒 STEP 8: Data Isolation Test")
    
    # Create second user
    user2_email = f"e2etest2_{int(time.time())}@example.com"
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={"email": user2_email, "password": TEST_PASSWORD},
            timeout=5
        )
        if response.status_code in [200, 201]:
            results.add_test("Create second user", True, f"Email: {user2_email}")
            
            # Login second user
            response = requests.post(
                f"{BASE_URL}/api/auth/login",
                data={"username": user2_email, "password": TEST_PASSWORD},
                timeout=5
            )
            if response.status_code == 200:
                token2 = response.json().get("access_token")
                headers2 = {"Authorization": f"Bearer {token2}"}
                
                # Create note as user 1
                requests.post(
                    f"{BASE_URL}/api/notes",
                    headers=headers,
                    json={"title": "User 1 Note", "content": "Private content"},
                    timeout=5
                )
                
                # Try to access user 1's notes as user 2
                response = requests.get(f"{BASE_URL}/api/notes", headers=headers2, timeout=5)
                if response.status_code == 200:
                    notes = response.json()
                    has_user1_note = any("User 1 Note" in str(note) for note in notes)
                    if not has_user1_note:
                        results.add_test("Data isolation (correctly isolated)", True)
                    else:
                        results.add_test("Data isolation (should not see other user's data)", False)
        else:
            results.add_test("Create second user", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Create second user", False, str(e))
    
    # ========================================
    # STEP 9: Frontend Integration Test
    # ========================================
    print_header("🌐 STEP 9: Frontend Integration Test")
    
    # Test 9.1: Frontend loads
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200 and "NoteApp" in response.text:
            results.add_test("Frontend HTML loads", True)
        else:
            results.add_test("Frontend HTML loads", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("Frontend HTML loads", False, str(e))
    
    # Test 9.2: CSS loads
    try:
        response = requests.get(f"{BASE_URL}/css/styles.css", timeout=5)
        if response.status_code == 200:
            results.add_test("CSS file loads", True, "HTTP 200")
        else:
            results.add_test("CSS file loads", False, f"HTTP {response.status_code}")
    except Exception as e:
        results.add_test("CSS file loads", False, str(e))
    
    # Test 9.3: JavaScript loads
    try:
        response = requests.get(f"{BASE_URL}/js/app.js", timeout=5)
        if response.status_code == 200:
            results.add_test("JavaScript file loads", True, "HTTP 200")
        else:
            results.add_test("JavaScript file loads", False, f"HTTP {response.status_code}")
    except Exception as e:
        results.add_test("JavaScript file loads", False, str(e))
    
    # ========================================
    # STEP 10: API Documentation
    # ========================================
    print_header("📊 STEP 10: API Documentation")
    
    # Test 10.1: Swagger UI
    try:
        response = requests.get(f"{BASE_URL}/api/docs", timeout=5)
        if response.status_code == 200:
            results.add_test("Swagger UI accessible", True, "HTTP 200")
        else:
            results.add_test("Swagger UI accessible", False, f"HTTP {response.status_code}")
    except Exception as e:
        results.add_test("Swagger UI accessible", False, str(e))
    
    # Test 10.2: OpenAPI schema
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200 and "openapi" in response.text:
            results.add_test("OpenAPI schema available", True)
        else:
            results.add_test("OpenAPI schema available", False, f"Status: {response.status_code}")
    except Exception as e:
        results.add_test("OpenAPI schema available", False, str(e))
    
    # Print summary
    results.print_summary()

if __name__ == "__main__":
    main()
