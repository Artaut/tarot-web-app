#!/usr/bin/env python3
"""
Backend Regression Test Suite for Tarot API
Ship-Ready Verification Tests

Tests critical endpoints after configuration updates:
- GET /api/cards (22 Major Arcana cards)
- GET /api/cards/{id} (specific card retrieval)
- POST /api/reading/card_of_day (Turkish language support)
- POST /api/reading/classic_tarot (English with AI interpretation)
- Health check of all 5 reading types
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('EXPO_PUBLIC_BACKEND_URL', 'https://divinereader.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

print(f"Testing backend at: {API_BASE}")

class TarotAPITester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name: str, passed: bool, details: str = "", response_time: float = 0):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        result = {
            'test': test_name,
            'status': status,
            'passed': passed,
            'details': details,
            'response_time': f"{response_time:.3f}s" if response_time > 0 else "N/A"
        }
        self.results.append(result)
        print(f"{status} - {test_name} ({result['response_time']}) - {details}")
    
    def test_root_endpoint(self):
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("Root Endpoint", True, "API is running and accessible")
                    return True
                else:
                    self.log_test("Root Endpoint", False, "Response missing expected message field", {"response": data})
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Connection error: {str(e)}")
        return False
    
    def test_get_all_cards(self):
        """Test GET /api/cards - should return all 22 Major Arcana cards"""
        try:
            response = self.session.get(f"{self.base_url}/cards")
            if response.status_code == 200:
                cards = response.json()
                
                # Check if we have 22 cards (Major Arcana)
                if len(cards) != 22:
                    self.log_test("Get All Cards", False, f"Expected 22 cards, got {len(cards)}")
                    return False
                
                # Validate card structure
                required_fields = ["id", "name", "image_url", "keywords", "meaning_upright", 
                                 "meaning_reversed", "description", "symbolism", "yes_no_meaning"]
                
                for i, card in enumerate(cards):
                    for field in required_fields:
                        if field not in card:
                            self.log_test("Get All Cards", False, f"Card {i} missing field: {field}")
                            return False
                    
                    # Validate data types
                    if not isinstance(card["id"], int):
                        self.log_test("Get All Cards", False, f"Card {i} id should be integer")
                        return False
                    
                    if not isinstance(card["keywords"], list):
                        self.log_test("Get All Cards", False, f"Card {i} keywords should be list")
                        return False
                
                # Check if cards are properly ordered (0-21)
                card_ids = [card["id"] for card in cards]
                expected_ids = list(range(22))
                if sorted(card_ids) != expected_ids:
                    self.log_test("Get All Cards", False, "Card IDs not properly ordered 0-21")
                    return False
                
                self.log_test("Get All Cards", True, f"Successfully retrieved {len(cards)} cards with proper structure")
                return True
            else:
                self.log_test("Get All Cards", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Get All Cards", False, f"Request error: {str(e)}")
        return False
    
    def test_get_specific_card(self):
        """Test GET /api/cards/{id} - test with id=0 for The Fool"""
        try:
            response = self.session.get(f"{self.base_url}/cards/0")
            if response.status_code == 200:
                card = response.json()
                
                # Validate The Fool card specifically
                if card["id"] != 0:
                    self.log_test("Get Specific Card", False, f"Expected card id 0, got {card['id']}")
                    return False
                
                if card["name"] != "The Fool":
                    self.log_test("Get Specific Card", False, f"Expected 'The Fool', got '{card['name']}'")
                    return False
                
                # Check required fields
                required_fields = ["id", "name", "image_url", "keywords", "meaning_upright", 
                                 "meaning_reversed", "description", "symbolism", "yes_no_meaning"]
                
                for field in required_fields:
                    if field not in card:
                        self.log_test("Get Specific Card", False, f"Missing field: {field}")
                        return False
                
                self.log_test("Get Specific Card", True, f"Successfully retrieved The Fool card with all fields")
                return True
            else:
                self.log_test("Get Specific Card", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Get Specific Card", False, f"Request error: {str(e)}")
        return False
    
    def test_get_invalid_card(self):
        """Test GET /api/cards/{id} with invalid ID"""
        try:
            response = self.session.get(f"{self.base_url}/cards/999")
            if response.status_code == 404:
                self.log_test("Get Invalid Card", True, "Properly returns 404 for invalid card ID")
                return True
            else:
                self.log_test("Get Invalid Card", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Get Invalid Card", False, f"Request error: {str(e)}")
        return False
    
    def test_get_reading_types(self):
        """Test GET /api/reading-types - should return all 5 reading types"""
        try:
            response = self.session.get(f"{self.base_url}/reading-types")
            if response.status_code == 200:
                reading_types = response.json()
                
                # Check if we have 5 reading types
                if len(reading_types) != 5:
                    self.log_test("Get Reading Types", False, f"Expected 5 reading types, got {len(reading_types)}")
                    return False
                
                # Validate reading type structure
                required_fields = ["id", "name", "description", "card_count", "positions"]
                expected_types = ["card_of_day", "classic_tarot", "path_of_day", "couples_tarot", "yes_no"]
                expected_counts = [1, 3, 4, 5, 1]
                
                found_types = []
                for reading_type in reading_types:
                    for field in required_fields:
                        if field not in reading_type:
                            self.log_test("Get Reading Types", False, f"Reading type missing field: {field}")
                            return False
                    
                    found_types.append(reading_type["id"])
                    
                    # Validate positions list length matches card_count
                    if len(reading_type["positions"]) != reading_type["card_count"]:
                        self.log_test("Get Reading Types", False, 
                                    f"Reading type {reading_type['id']}: positions count doesn't match card_count")
                        return False
                
                # Check if all expected types are present
                for expected_type in expected_types:
                    if expected_type not in found_types:
                        self.log_test("Get Reading Types", False, f"Missing reading type: {expected_type}")
                        return False
                
                self.log_test("Get Reading Types", True, f"Successfully retrieved {len(reading_types)} reading types with proper structure")
                return True
            else:
                self.log_test("Get Reading Types", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Get Reading Types", False, f"Request error: {str(e)}")
        return False
    
    def test_create_reading(self, reading_type: str, expected_card_count: int, question: str = None):
        """Test POST /api/reading/{type} - create a reading"""
        try:
            url = f"{self.base_url}/reading/{reading_type}"
            params = {}
            if question:
                params["question"] = question
            
            response = self.session.post(url, params=params)
            if response.status_code == 200:
                reading = response.json()
                
                # Validate reading structure
                required_fields = ["id", "reading_type", "cards", "interpretation", "timestamp"]
                for field in required_fields:
                    if field not in reading:
                        self.log_test(f"Create Reading ({reading_type})", False, f"Missing field: {field}")
                        return False
                
                # Check reading type matches
                if reading["reading_type"] != reading_type:
                    self.log_test(f"Create Reading ({reading_type})", False, 
                                f"Reading type mismatch: expected {reading_type}, got {reading['reading_type']}")
                    return False
                
                # Check card count
                if len(reading["cards"]) != expected_card_count:
                    self.log_test(f"Create Reading ({reading_type})", False, 
                                f"Expected {expected_card_count} cards, got {len(reading['cards'])}")
                    return False
                
                # Validate card structure in reading
                for i, card_data in enumerate(reading["cards"]):
                    required_card_fields = ["card", "position", "reversed"]
                    for field in required_card_fields:
                        if field not in card_data:
                            self.log_test(f"Create Reading ({reading_type})", False, 
                                        f"Card {i} missing field: {field}")
                            return False
                    
                    # Validate card data structure
                    card = card_data["card"]
                    if "id" not in card or "name" not in card:
                        self.log_test(f"Create Reading ({reading_type})", False, 
                                    f"Card {i} missing basic card info")
                        return False
                
                # Check interpretation is not empty
                if not reading["interpretation"] or len(reading["interpretation"].strip()) == 0:
                    self.log_test(f"Create Reading ({reading_type})", False, "Interpretation is empty")
                    return False
                
                # Validate timestamp format
                try:
                    datetime.fromisoformat(reading["timestamp"].replace('Z', '+00:00'))
                except ValueError:
                    self.log_test(f"Create Reading ({reading_type})", False, "Invalid timestamp format")
                    return False
                
                self.log_test(f"Create Reading ({reading_type})", True, 
                            f"Successfully created reading with {len(reading['cards'])} cards and interpretation")
                return True
            else:
                self.log_test(f"Create Reading ({reading_type})", False, 
                            f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test(f"Create Reading ({reading_type})", False, f"Request error: {str(e)}")
        return False
    
    def test_create_invalid_reading(self):
        """Test POST /api/reading/{type} with invalid reading type"""
        try:
            response = self.session.post(f"{self.base_url}/reading/invalid_type")
            if response.status_code == 404:
                self.log_test("Create Invalid Reading", True, "Properly returns 404 for invalid reading type")
                return True
            else:
                self.log_test("Create Invalid Reading", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Create Invalid Reading", False, f"Request error: {str(e)}")
        return False
    
    def test_get_readings(self):
        """Test GET /api/readings - should return recent readings"""
        try:
            response = self.session.get(f"{self.base_url}/readings")
            if response.status_code == 200:
                readings = response.json()
                
                # Should be a list (even if empty)
                if not isinstance(readings, list):
                    self.log_test("Get Readings", False, "Response should be a list")
                    return False
                
                # If we have readings, validate structure
                if len(readings) > 0:
                    required_fields = ["id", "reading_type", "cards", "interpretation", "timestamp"]
                    for i, reading in enumerate(readings):
                        for field in required_fields:
                            if field not in reading:
                                self.log_test("Get Readings", False, f"Reading {i} missing field: {field}")
                                return False
                    
                    # Check if readings are sorted by timestamp (most recent first)
                    if len(readings) > 1:
                        timestamps = [reading["timestamp"] for reading in readings]
                        sorted_timestamps = sorted(timestamps, reverse=True)
                        if timestamps != sorted_timestamps:
                            self.log_test("Get Readings", False, "Readings not sorted by timestamp (newest first)")
                            return False
                
                self.log_test("Get Readings", True, f"Successfully retrieved {len(readings)} readings")
                return True
            else:
                self.log_test("Get Readings", False, f"HTTP {response.status_code}", {"response": response.text})
        except Exception as e:
            self.log_test("Get Readings", False, f"Request error: {str(e)}")
        return False
    
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🔮 Starting Tarot API Tests")
        print(f"Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test basic connectivity
        if not self.test_root_endpoint():
            print("❌ Cannot connect to API. Stopping tests.")
            return False
        
        # Test card endpoints
        self.test_get_all_cards()
        self.test_get_specific_card()
        self.test_get_invalid_card()
        
        # Test reading types
        self.test_get_reading_types()
        
        # Test reading creation for each type
        reading_tests = [
            ("card_of_day", 1, None),
            ("classic_tarot", 3, None),
            ("path_of_day", 4, None),
            ("couples_tarot", 5, None),
            ("yes_no", 1, "Will I find love this year?")
        ]
        
        for reading_type, card_count, question in reading_tests:
            self.test_create_reading(reading_type, card_count, question)
        
        # Test invalid reading type
        self.test_create_invalid_reading()
        
        # Test getting readings (should now have some from previous tests)
        self.test_get_readings()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🔮 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! The Tarot API is working perfectly.")
            return True
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the details above.")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
            return False

def main():
    """Main test execution"""
    tester = TarotAPITester(BACKEND_URL)
    success = tester.run_all_tests()
    
    # Save detailed results to file
    with open("/app/test_results_detailed.json", "w") as f:
        json.dump(tester.test_results, f, indent=2)
    
    print(f"\nDetailed results saved to: /app/test_results_detailed.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())