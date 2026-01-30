#!/bin/bash
# Comprehensive End-to-End Test Suite for NoteApp
# Tests all features including security

BASE_URL="http://127.0.0.1:8003"
TEST_EMAIL="e2etest$(date +%s)@example.com"
TEST_PASSWORD="SecureTest123!"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0

echo "=========================================="
echo "🧪 NoteApp End-to-End Test Suite"
echo "=========================================="
echo ""
echo "📍 Testing: $BASE_URL"
echo "👤 Test User: $TEST_EMAIL"
echo ""

# Helper function
test_result() {
    local name="$1"
    local status="$2"
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        ((PASS++))
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        ((FAIL++))
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏥 STEP 1: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HEALTH_RESPONSE=$(curl -s $BASE_URL/health)
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    test_result "Health endpoint responds" "pass"
else
    test_result "Health endpoint responds" "fail"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 STEP 2: User Registration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
echo "Response: $REGISTER_RESPONSE"

if echo "$REGISTER_RESPONSE" | grep -q "email"; then
    test_result "User registration successful" "pass"
    USER_ID=$(echo "$REGISTER_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    echo "  📝 User ID: $USER_ID"
else
    test_result "User registration successful" "fail"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 STEP 3: User Login & JWT Token"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_EMAIL&password=$TEST_PASSWORD")
echo "Response: ${LOGIN_RESPONSE:0:100}..."

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -n "$ACCESS_TOKEN" ]; then
    test_result "User login successful" "pass"
    test_result "JWT token generated" "pass"
    echo "  🔑 Token: ${ACCESS_TOKEN:0:30}..."
else
    test_result "User login successful" "fail"
    test_result "JWT token generated" "fail"
    echo "⚠️  Cannot continue without access token"
    exit 1
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛡️  STEP 4: Security Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 4.1: Access without token
echo "Test 4.1: Unauthorized access prevention"
UNAUTH_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/notes)
HTTP_CODE=$(echo "$UNAUTH_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    test_result "Blocks access without token (HTTP $HTTP_CODE)" "pass"
else
    test_result "Blocks access without token (HTTP $HTTP_CODE)" "fail"
fi

# Test 4.2: Invalid token
echo "Test 4.2: Invalid token rejection"
INVALID_TOKEN_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET $BASE_URL/api/notes \
  -H "Authorization: Bearer invalid_token_12345")
HTTP_CODE=$(echo "$INVALID_TOKEN_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    test_result "Rejects invalid token (HTTP $HTTP_CODE)" "pass"
else
    test_result "Rejects invalid token (HTTP $HTTP_CODE)" "fail"
fi

# Test 4.3: CORS headers
echo "Test 4.3: CORS headers present"
CORS_RESPONSE=$(curl -s -I $BASE_URL/health)
if echo "$CORS_RESPONSE" | grep -qi "access-control"; then
    test_result "CORS headers configured" "pass"
else
    test_result "CORS headers configured" "fail"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 STEP 5: Notes CRUD Operations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 5.1: Create Note
echo "Test 5.1: Create note"
NOTE_RESPONSE=$(curl -s -X POST $BASE_URL/api/notes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Note","content":"This is a test note content"}')
NOTE_ID=$(echo "$NOTE_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$NOTE_ID" ]; then
    test_result "Create note (ID: $NOTE_ID)" "pass"
else
    test_result "Create note" "fail"
fi

# Test 5.2: Get all notes
echo "Test 5.2: Retrieve all notes"
NOTES_LIST=$(curl -s -X GET $BASE_URL/api/notes \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$NOTES_LIST" | grep -q "Test Note"; then
    test_result "Get all notes" "pass"
    NOTE_COUNT=$(echo "$NOTES_LIST" | grep -o '"id":' | wc -l)
    echo "  📊 Total notes: $NOTE_COUNT"
else
    test_result "Get all notes" "fail"
fi

# Test 5.3: Get specific note
if [ -n "$NOTE_ID" ]; then
    echo "Test 5.3: Get specific note"
    SPECIFIC_NOTE=$(curl -s -X GET $BASE_URL/api/notes/$NOTE_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    
    if echo "$SPECIFIC_NOTE" | grep -q "Test Note"; then
        test_result "Get note by ID" "pass"
    else
        test_result "Get note by ID" "fail"
    fi
fi

# Test 5.4: Update note
if [ -n "$NOTE_ID" ]; then
    echo "Test 5.4: Update note"
    UPDATE_NOTE=$(curl -s -X PUT $BASE_URL/api/notes/$NOTE_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title":"Updated Test Note","content":"Updated content"}')
    
    if echo "$UPDATE_NOTE" | grep -q "Updated Test Note"; then
        test_result "Update note" "pass"
    else
        test_result "Update note" "fail"
    fi
fi

# Test 5.5: Delete note
if [ -n "$NOTE_ID" ]; then
    echo "Test 5.5: Delete note"
    DELETE_NOTE=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/api/notes/$NOTE_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    HTTP_CODE=$(echo "$DELETE_NOTE" | tail -n1)
    
    if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
        test_result "Delete note (HTTP $HTTP_CODE)" "pass"
    else
        test_result "Delete note (HTTP $HTTP_CODE)" "fail"
    fi
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ STEP 6: Tasks CRUD Operations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 6.1: Create Task
echo "Test 6.1: Create task"
TASK_RESPONSE=$(curl -s -X POST $BASE_URL/api/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test task description","status":"pending","due_date":"2026-02-15T10:00:00"}')
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$TASK_ID" ]; then
    test_result "Create task (ID: $TASK_ID)" "pass"
else
    test_result "Create task" "fail"
fi

# Test 6.2: Get all tasks
echo "Test 6.2: Retrieve all tasks"
TASKS_LIST=$(curl -s -X GET $BASE_URL/api/tasks \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$TASKS_LIST" | grep -q "Test Task"; then
    test_result "Get all tasks" "pass"
    TASK_COUNT=$(echo "$TASKS_LIST" | grep -o '"id":' | wc -l)
    echo "  📊 Total tasks: $TASK_COUNT"
else
    test_result "Get all tasks" "fail"
fi

# Test 6.3: Update task status
if [ -n "$TASK_ID" ]; then
    echo "Test 6.3: Update task status"
    UPDATE_TASK=$(curl -s -X PUT $BASE_URL/api/tasks/$TASK_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title":"Test Task","description":"Updated description","status":"completed","due_date":"2026-02-15T10:00:00"}')
    
    if echo "$UPDATE_TASK" | grep -q "completed"; then
        test_result "Update task status to completed" "pass"
    else
        test_result "Update task status to completed" "fail"
    fi
fi

# Test 6.4: Delete task
if [ -n "$TASK_ID" ]; then
    echo "Test 6.4: Delete task"
    DELETE_TASK=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/api/tasks/$TASK_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    HTTP_CODE=$(echo "$DELETE_TASK" | tail -n1)
    
    if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
        test_result "Delete task (HTTP $HTTP_CODE)" "pass"
    else
        test_result "Delete task (HTTP $HTTP_CODE)" "fail"
    fi
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📅 STEP 7: Calendar Events CRUD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 7.1: Create Event
echo "Test 7.1: Create calendar event"
EVENT_RESPONSE=$(curl -s -X POST $BASE_URL/api/calendar \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Event","description":"Test event description","start_time":"2026-02-15T10:00:00","end_time":"2026-02-15T11:00:00"}')
EVENT_ID=$(echo "$EVENT_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -n "$EVENT_ID" ]; then
    test_result "Create calendar event (ID: $EVENT_ID)" "pass"
else
    test_result "Create calendar event" "fail"
fi

# Test 7.2: Get all events
echo "Test 7.2: Retrieve all events"
EVENTS_LIST=$(curl -s -X GET $BASE_URL/api/calendar \
  -H "Authorization: Bearer $ACCESS_TOKEN")

if echo "$EVENTS_LIST" | grep -q "Test Event"; then
    test_result "Get all calendar events" "pass"
    EVENT_COUNT=$(echo "$EVENTS_LIST" | grep -o '"id":' | wc -l)
    echo "  📊 Total events: $EVENT_COUNT"
else
    test_result "Get all calendar events" "fail"
fi

# Test 7.3: Update event
if [ -n "$EVENT_ID" ]; then
    echo "Test 7.3: Update event"
    UPDATE_EVENT=$(curl -s -X PUT $BASE_URL/api/calendar/$EVENT_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title":"Updated Event","description":"Updated event description","start_time":"2026-02-15T14:00:00","end_time":"2026-02-15T15:00:00"}')
    
    if echo "$UPDATE_EVENT" | grep -q "Updated Event"; then
        test_result "Update calendar event" "pass"
    else
        test_result "Update calendar event" "fail"
    fi
fi

# Test 7.4: Delete event
if [ -n "$EVENT_ID" ]; then
    echo "Test 7.4: Delete event"
    DELETE_EVENT=$(curl -s -w "\n%{http_code}" -X DELETE $BASE_URL/api/calendar/$EVENT_ID \
      -H "Authorization: Bearer $ACCESS_TOKEN")
    HTTP_CODE=$(echo "$DELETE_EVENT" | tail -n1)
    
    if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
        test_result "Delete calendar event (HTTP $HTTP_CODE)" "pass"
    else
        test_result "Delete calendar event (HTTP $HTTP_CODE)" "fail"
    fi
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔒 STEP 8: Data Isolation Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create second user
echo "Test 8.1: Create second user"
USER2_EMAIL="e2etest2_$(date +%s)@example.com"
REGISTER2=$(curl -s -X POST $BASE_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$USER2_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

if echo "$REGISTER2" | grep -q "email"; then
    test_result "Create second user" "pass"
    
    # Login second user
    LOGIN2=$(curl -s -X POST $BASE_URL/api/auth/login \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=$USER2_EMAIL&password=$TEST_PASSWORD")
    TOKEN2=$(echo "$LOGIN2" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    
    if [ -n "$TOKEN2" ]; then
        # Create note as user 1
        NOTE1=$(curl -s -X POST $BASE_URL/api/notes \
          -H "Authorization: Bearer $ACCESS_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{"title":"User 1 Note","content":"Private content"}')
        
        # Try to access user 1's notes as user 2
        echo "Test 8.2: Data isolation between users"
        NOTES2=$(curl -s -X GET $BASE_URL/api/notes \
          -H "Authorization: Bearer $TOKEN2")
        
        if echo "$NOTES2" | grep -q "User 1 Note"; then
            test_result "Data isolation (should not see other user's data)" "fail"
        else
            test_result "Data isolation (correctly isolated)" "pass"
        fi
    fi
else
    test_result "Create second user" "fail"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 STEP 9: Frontend Integration Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 9.1: Frontend loads
echo "Test 9.1: Frontend page loads"
FRONTEND=$(curl -s $BASE_URL/)
if echo "$FRONTEND" | grep -q "NoteApp"; then
    test_result "Frontend HTML loads" "pass"
else
    test_result "Frontend HTML loads" "fail"
fi

# Test 9.2: CSS loads
echo "Test 9.2: CSS file accessible"
CSS_RESPONSE=$(curl -s -w "\n%{http_code}" $BASE_URL/css/styles.css)
HTTP_CODE=$(echo "$CSS_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    test_result "CSS file loads (HTTP 200)" "pass"
else
    test_result "CSS file loads (HTTP $HTTP_CODE)" "fail"
fi

# Test 9.3: JavaScript loads
echo "Test 9.3: JavaScript file accessible"
JS_RESPONSE=$(curl -s -w "\n%{http_code}" $BASE_URL/js/app.js)
HTTP_CODE=$(echo "$JS_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    test_result "JavaScript file loads (HTTP 200)" "pass"
else
    test_result "JavaScript file loads (HTTP $HTTP_CODE)" "fail"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 STEP 10: API Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 10.1: Swagger UI
echo "Test 10.1: Swagger UI accessible"
SWAGGER=$(curl -s -w "\n%{http_code}" $BASE_URL/api/docs)
HTTP_CODE=$(echo "$SWAGGER" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    test_result "Swagger UI accessible (HTTP 200)" "pass"
else
    test_result "Swagger UI accessible (HTTP $HTTP_CODE)" "fail"
fi

# Test 10.2: OpenAPI schema
echo "Test 10.2: OpenAPI schema available"
OPENAPI=$(curl -s $BASE_URL/openapi.json)
if echo "$OPENAPI" | grep -q "openapi"; then
    test_result "OpenAPI schema available" "pass"
else
    test_result "OpenAPI schema available" "fail"
fi
echo ""

echo "=========================================="
echo "📈 TEST RESULTS SUMMARY"
echo "=========================================="
TOTAL=$((PASS + FAIL))
if [ $TOTAL -gt 0 ]; then
    PERCENTAGE=$((PASS * 100 / TOTAL))
else
    PERCENTAGE=0
fi

echo ""
echo "Total Tests:     $TOTAL"
echo -e "${GREEN}Passed:          $PASS${NC}"
echo -e "${RED}Failed:          $FAIL${NC}"
echo "Success Rate:    $PERCENTAGE%"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}✅ Application is fully functional${NC}"
    echo -e "${GREEN}✅ All features working correctly${NC}"
    echo -e "${GREEN}✅ Security measures in place${NC}"
    echo -e "${GREEN}✅ Ready for deployment${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo -e "${YELLOW}Please review the errors above${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi
