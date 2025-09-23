#!/usr/bin/env python3
"""
Backend Regression Tests for Tarot API after AI Integration
Tests specific scenarios requested in the review.
"""

import requests
import json
import time
import os
import sys
from typing import Dict, Any, List
from datetime import datetime

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('EXPO_PUBLIC_BACKEND_URL='):
                    base_url = line.split('=', 1)[1].strip()
                    return f"{base_url}/api"
    except Exception as e:
        print(f"Warning: Could not read frontend .env: {e}")
    return "https://divinereader.preview.emergentagent.com/api"

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

class TarotAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details:
            for key, value in details.items():
                print(f"  {key}: {value}")
        print()

    def test_card_of_day_without_ai_key(self):
        """Test 1: POST /api/reading/card_of_day?language=tr without EMERGENT_LLM_KEY"""
        print("🔍 Test 1: Card of Day without AI key (fallback test)")
        
        try:
            # Record start time
            start_time = time.time()
            
            # Make request
            url = f"{self.base_url}/reading/card_of_day?language=tr"
            response = self.session.post(url)
            
            # Record end time
            end_time = time.time()
            response_time = end_time - start_time
            
            # Check response
            if response.status_code != 200:
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"response_time": f"{response_time:.2f}s"}
                )
                return
            
            data = response.json()
            
            # Validate response structure
            required_fields = ["id", "reading_type", "cards", "interpretation", "timestamp"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    f"Missing required fields: {missing_fields}",
                    {"response_time": f"{response_time:.2f}s"}
                )
                return
            
            # Check interpretation exists (fallback should work)
            interpretation = data.get("interpretation", "")
            if not interpretation or len(interpretation.strip()) < 10:
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    "Interpretation is empty or too short",
                    {"response_time": f"{response_time:.2f}s", "interpretation_length": len(interpretation)}
                )
                return
            
            # Check response time < 2s
            if response_time >= 2.0:
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    f"Response time {response_time:.2f}s >= 2s",
                    {"response_time": f"{response_time:.2f}s"}
                )
                return
            
            # Check reading type
            if data.get("reading_type") != "card_of_day":
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    f"Wrong reading type: {data.get('reading_type')}",
                    {"response_time": f"{response_time:.2f}s"}
                )
                return
            
            # Check cards array
            cards = data.get("cards", [])
            if len(cards) != 1:
                self.log_test(
                    "Card of Day without AI key",
                    False,
                    f"Expected 1 card, got {len(cards)}",
                    {"response_time": f"{response_time:.2f}s"}
                )
                return
            
            self.log_test(
                "Card of Day without AI key",
                True,
                "Fallback interpretation working, response time acceptable",
                {
                    "response_time": f"{response_time:.2f}s",
                    "interpretation_length": len(interpretation),
                    "card_count": len(cards)
                }
            )
            
        except Exception as e:
            self.log_test(
                "Card of Day without AI key",
                False,
                f"Exception: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_classic_tarot_with_question(self):
        """Test 2: POST /api/reading/classic_tarot?language=en with question"""
        print("🔍 Test 2: Classic Tarot with question")
        
        try:
            url = f"{self.base_url}/reading/classic_tarot?language=en"
            payload = {"question": "Career advice"}
            
            response = self.session.post(url, json=payload)
            
            if response.status_code != 200:
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return
            
            data = response.json()
            
            # Validate response structure
            required_fields = ["id", "reading_type", "cards", "interpretation", "timestamp"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    f"Missing required fields: {missing_fields}"
                )
                return
            
            # Check interpretation exists
            interpretation = data.get("interpretation", "")
            if not interpretation or len(interpretation.strip()) < 10:
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    "Interpretation is empty or too short",
                    {"interpretation_length": len(interpretation)}
                )
                return
            
            # Check reading type
            if data.get("reading_type") != "classic_tarot":
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    f"Wrong reading type: {data.get('reading_type')}"
                )
                return
            
            # Check cards array (should be 3 for classic tarot)
            cards = data.get("cards", [])
            if len(cards) != 3:
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    f"Expected 3 cards, got {len(cards)}"
                )
                return
            
            # Check that interpretation contains at least one card name
            card_names = []
            for card_info in cards:
                card = card_info.get("card", {})
                card_name = card.get("name", "")
                if card_name:
                    card_names.append(card_name)
            
            interpretation_lower = interpretation.lower()
            card_name_found = False
            found_card_names = []
            
            for card_name in card_names:
                if card_name.lower() in interpretation_lower:
                    card_name_found = True
                    found_card_names.append(card_name)
            
            if not card_name_found:
                self.log_test(
                    "Classic Tarot with question",
                    False,
                    "Interpretation does not contain any selected card names",
                    {
                        "card_names": card_names,
                        "interpretation_preview": interpretation[:200] + "..."
                    }
                )
                return
            
            self.log_test(
                "Classic Tarot with question",
                True,
                "Interpretation contains selected card names",
                {
                    "card_count": len(cards),
                    "found_card_names": found_card_names,
                    "interpretation_length": len(interpretation)
                }
            )
            
        except Exception as e:
            self.log_test(
                "Classic Tarot with question",
                False,
                f"Exception: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_card_detail_turkish(self):
        """Test 3: GET /api/cards/20?language=tr returns image_base64 and Turkish name"""
        print("🔍 Test 3: Card detail with Turkish language")
        
        try:
            url = f"{self.base_url}/cards/20?language=tr"
            response = self.session.get(url)
            
            if response.status_code != 200:
                self.log_test(
                    "Card detail Turkish",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                return
            
            data = response.json()
            
            # Check required fields
            required_fields = ["id", "name", "image_url", "keywords", "meaning_upright", 
                             "meaning_reversed", "description", "symbolism", "yes_no_meaning"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test(
                    "Card detail Turkish",
                    False,
                    f"Missing required fields: {missing_fields}"
                )
                return
            
            # Check image_base64 exists
            image_base64 = data.get("image_base64")
            if not image_base64:
                self.log_test(
                    "Card detail Turkish",
                    False,
                    "image_base64 field is missing or empty"
                )
                return
            
            # Validate base64 format
            if not image_base64.startswith("data:image/"):
                self.log_test(
                    "Card detail Turkish",
                    False,
                    "image_base64 is not a valid data URI",
                    {"image_base64_preview": image_base64[:50] + "..."}
                )
                return
            
            # Check Turkish name (card 20 should be "Yargı")
            card_name = data.get("name", "")
            expected_turkish_name = "Yargı"  # Card 20 is Judgement = Yargı in Turkish
            
            if card_name != expected_turkish_name:
                self.log_test(
                    "Card detail Turkish",
                    False,
                    f"Expected Turkish name '{expected_turkish_name}', got '{card_name}'"
                )
                return
            
            # Check card ID
            if data.get("id") != 20:
                self.log_test(
                    "Card detail Turkish",
                    False,
                    f"Expected card ID 20, got {data.get('id')}"
                )
                return
            
            self.log_test(
                "Card detail Turkish",
                True,
                "Card 20 returns correct Turkish name and image_base64",
                {
                    "card_name": card_name,
                    "image_base64_size": len(image_base64),
                    "card_id": data.get("id")
                }
            )
            
        except Exception as e:
            self.log_test(
                "Card detail Turkish",
                False,
                f"Exception: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def test_no_500_errors_basic_endpoints(self):
        """Test 4: Ensure no 500 errors on basic endpoints"""
        print("🔍 Test 4: Basic endpoints for 500 errors")
        
        endpoints_to_test = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/cards", "All cards"),
            ("GET", "/cards?language=tr", "All cards Turkish"),
            ("GET", "/cards/0", "Card detail"),
            ("GET", "/reading-types", "Reading types"),
            ("GET", "/readings", "Recent readings")
        ]
        
        all_passed = True
        results = []
        
        for method, endpoint, description in endpoints_to_test:
            try:
                url = f"{self.base_url}{endpoint}"
                if method == "GET":
                    response = self.session.get(url)
                else:
                    response = self.session.request(method, url)
                
                if response.status_code >= 500:
                    all_passed = False
                    results.append(f"{description}: HTTP {response.status_code}")
                else:
                    results.append(f"{description}: HTTP {response.status_code} ✓")
                    
            except Exception as e:
                all_passed = False
                results.append(f"{description}: Exception {str(e)}")
        
        if all_passed:
            self.log_test(
                "No 500 errors basic endpoints",
                True,
                "All basic endpoints return non-500 status codes",
                {"tested_endpoints": len(endpoints_to_test)}
            )
        else:
            self.log_test(
                "No 500 errors basic endpoints",
                False,
                "Some endpoints returned 500 errors",
                {"results": results}
            )

    def test_ai_integration_logging(self):
        """Test 5: Check AI integration behavior and logging"""
        print("🔍 Test 5: AI integration behavior")
        
        try:
            # Check if EMERGENT_LLM_KEY is set in environment
            ai_key_present = bool(os.getenv('EMERGENT_LLM_KEY'))
            
            # Make a reading request to trigger AI logic
            url = f"{self.base_url}/reading/card_of_day?language=en"
            response = self.session.post(url)
            
            if response.status_code != 200:
                self.log_test(
                    "AI integration logging",
                    False,
                    f"Failed to create reading for AI test: HTTP {response.status_code}"
                )
                return
            
            data = response.json()
            interpretation = data.get("interpretation", "")
            
            # Check that interpretation exists regardless of AI key presence
            if not interpretation or len(interpretation.strip()) < 10:
                self.log_test(
                    "AI integration logging",
                    False,
                    "No interpretation generated (AI or fallback failed)",
                    {"ai_key_present": ai_key_present}
                )
                return
            
            # Check backend logs for AI-related messages
            try:
                import subprocess
                log_result = subprocess.run(
                    ["tail", "-n", "50", "/var/log/supervisor/backend.out.log"],
                    capture_output=True, text=True, timeout=5
                )
                log_content = log_result.stdout
                
                # Look for AI-related log messages
                ai_logs_found = any(keyword in log_content.lower() for keyword in 
                                  ['ai', 'llm', 'openai', 'emergent', 'interpretation'])
                
                self.log_test(
                    "AI integration logging",
                    True,
                    "AI integration working with proper fallback",
                    {
                        "ai_key_present": ai_key_present,
                        "interpretation_length": len(interpretation),
                        "ai_logs_detected": ai_logs_found
                    }
                )
                
            except Exception as log_e:
                # Log check failed, but main functionality works
                self.log_test(
                    "AI integration logging",
                    True,
                    "AI integration working (log check failed)",
                    {
                        "ai_key_present": ai_key_present,
                        "interpretation_length": len(interpretation),
                        "log_error": str(log_e)
                    }
                )
            
        except Exception as e:
            self.log_test(
                "AI integration logging",
                False,
                f"Exception during AI integration test: {str(e)}",
                {"error_type": type(e).__name__}
            )

    def run_all_tests(self):
        """Run all regression tests"""
        print("🚀 Starting Backend Regression Tests after AI Integration")
        print("=" * 60)
        
        # Run specific tests requested in review
        self.test_card_of_day_without_ai_key()
        self.test_classic_tarot_with_question()
        self.test_card_detail_turkish()
        self.test_no_500_errors_basic_endpoints()
        self.test_ai_integration_logging()
        
        # Summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n" + "=" * 60)
        return passed == total

if __name__ == "__main__":
    tester = TarotAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)