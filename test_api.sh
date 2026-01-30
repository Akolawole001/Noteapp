#!/bin/bash
# Comprehensive API Testing Script for Note App
# Tests all endpoints and security features

BASE_URL="http://127.0.0.1:8003"
TEST_EMAIL="testuser$(date +%s)@example.com"  # Unique email each run
TEST_PASSWORD="SecurePass123!"

echo "=================================="
echo "🧪 Note App API Testing Suite"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASS=0
FAIL=0

test_endpoint() {
    local name="$1"
    local response="$2"
    local expected_code="$3"
    
    if echo "$response" | grep -q "\""; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        ((PASS++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        ((FAIL++))
        return 1
    fi
}

echo "📊 Test 1: Health Check"
echo "-----------------------------------"
HEALTH=$(curl -s -w "\n%{http_code}" $BASE_URL/health)
HTTP_CODE=$(echo "$HEALTH" | tail -n1)
BODY=$(echo "$HEALTH" | head -n-1)
echo "Response: $BODY"
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Health check endpoint"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Health check endpoint (HTTP $HTTP_CODE)"
    ((FAIL++))
fi
echo ""

echo "📊 Test 2: User Registration"
echo "-----------------------------------"
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
echo "Email: $TEST_EMAIL"
echo "Response: $REGISTER_RESPONSE"
if echo "$REGISTER_RESPONSE" | grep -q "email"; then
    echo -e "${GREEN}✅ PASS${NC}: User registration"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: User registration"
    ((FAIL++))
fi
echo ""

echo "📊 Test 3: User Login"
echo "-----------------------------------"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
echo "Response: $LOGIN_RESPONSE"
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
if [ -n "$ACCESS_TOKEN" ]; then
    echo -e "${GREEN}✅ PASS${NC}: User login"
    echo "  🔑 Token: ${ACCESS_TOKEN:0:20}..."
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: User login - no access token"
    ((FAIL++))
    echo "⚠️  Cannot continue with authenticated tests without token"
    exit 1
fi
echo ""

echo "📊 Test 4: Create Note"
echo "-----------------------------------"
NOTE_RESPONSE=$(curl -s -X POST $BASE_URL/api/notes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"This is a test note content"}')
echo "Response: $NOTE_RESPONSE"
NOTE_ID=$(echo "$NOTE_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
if [ -n "$NOTE_ID" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Create note (ID: $NOTE_ID)"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Create note"
    ((FAIL++))
fi
echo ""

echo "📊 Test 5: Get All Notes"
echo "-----------------------------------"
NOTES_RESPONSE=$(curl -s -X GET $BASE_URL/api/notes \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Response: $NOTES_RESPONSE"
if echo "$NOTES_RESPONSE" | grep -q "Test Note"; then
    echo -e "${GREEN}✅ PASS${NC}: Get all notes"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Get all notes"
    ((FAIL++))
fi
echo ""

echo "📊 Test 6: Update Note"
echo "-----------------------------------"
if [ -n "$NOTE_ID" ]; then
    UPDATE_NOTE_RESPONSE=$(curl -s -X PUT $BASE_URL/api/notes/$NOTE_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title":"Updated Test Note","content":"Updated content"}')
    echo "Response: $UPDATE_NOTE_RESPONSE"
    if echo "$UPDATE_NOTE_RESPONSE" | grep -q "Updated Test Note"; then
        echo -e "${GREEN}✅ PASS${NC}: Update note"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: Update note"
        ((FAIL++))
    fi
else
    echo -e "${YELLOW}⏭️  SKIP${NC}: Update note (no note ID)"
fi
echo ""

echo "📊 Test 7: Create Task"
echo "-----------------------------------"
TASK_RESPONSE=$(curl -s -X POST $BASE_URL/api/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test task description","status":"pending","due_date":"2026-02-15T10:00:00"}')
echo "Response: $TASK_RESPONSE"
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
if [ -n "$TASK_ID" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Create task (ID: $TASK_ID)"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Create task"
    ((FAIL++))
fi
echo ""

echo "📊 Test 8: Get All Tasks"
echo "-----------------------------------"
TASKS_RESPONSE=$(curl -s -X GET $BASE_URL/api/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Response: $TASKS_RESPONSE"
if echo "$TASKS_RESPONSE" | grep -q "Test Task"; then
    echo -e "${GREEN}✅ PASS${NC}: Get all tasks"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Get all tasks"
    ((FAIL++))
fi
echo ""

echo "📊 Test 9: Create Calendar Event"
echo "-----------------------------------"
EVENT_RESPONSE=$(curl -s -X POST $BASE_URL/api/calendar \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Event","description":"Test event description","start_time":"2026-02-15T10:00:00","end_time":"2026-02-15T11:00:00"}')
echo "Response: $EVENT_RESPONSE"
EVENT_ID=$(echo "$EVENT_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
if [ -n "$EVENT_ID" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Create calendar event (ID: $EVENT_ID)"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Create calendar event"
    ((FAIL++))
fi
echo ""

echo "📊 Test 10: Get All Calendar Events"
echo "-----------------------------------"
EVENTS_RESPONSE=$(curl -s -X GET $BASE_URL/api/calendar \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Response: $EVENTS_RESPONSE"
if echo "$EVENTS_RESPONSE" | grep -q "Test Event"; then
    echo -e "${GREEN}✅ PASS${NC}: Get all calendar events"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Get all calendar events"
    ((FAIL++))
fi
echo ""

echo "📊 Test 11: Security - Access Without Token"
echo "-----------------------------------"
UNAUTHORIZED_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/notes)
HTTP_CODE=$(echo "$UNAUTHORIZED_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    echo -e "${GREEN}✅ PASS${NC}: Unauthorized access blocked (HTTP $HTTP_CODE)"
    ((PASS++))
else
    echo -e "${RED}❌ FAIL${NC}: Unauthorized access not blocked (HTTP $HTTP_CODE)"
    ((FAIL++))
fi
echo ""

echo "📊 Test 12: Delete Note"
echo "-----------------------------------"
if [ -n "$NOTE_ID" ]; then
    DELETE_RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/api/notes/$NOTE_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    HTTP_CODE=$(echo "$DELETE_RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC}: Delete note (HTTP $HTTP_CODE)"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: Delete note (HTTP $HTTP_CODE)"
        ((FAIL++))
    fi
else
    echo -e "${YELLOW}⏭️  SKIP${NC}: Delete note (no note ID)"
fi
echo ""

echo "=================================="
echo "📈 Test Results Summary"
echo "=================================="
TOTAL=$((PASS + FAIL))
PERCENTAGE=$((PASS * 100 / TOTAL))
echo -e "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo -e "Success Rate: $PERCENTAGE%"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Application is fully functional.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please review the errors above.${NC}"
    exit 1
fi
