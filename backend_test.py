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
        
    def test_get_cards_endpoint(self):
        """Test GET /api/cards - should return 22 Major Arcana cards"""
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/cards", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result("GET /api/cards", False, f"Status code: {response.status_code}", response_time)
                return
                
            cards = response.json()
            
            # Verify exactly 22 cards
            if len(cards) != 22:
                self.log_result("GET /api/cards", False, f"Expected 22 cards, got {len(cards)}", response_time)
                return
                
            # Verify card structure
            required_fields = ['id', 'name', 'image_url', 'keywords', 'meaning_upright', 'meaning_reversed', 'description', 'symbolism', 'yes_no_meaning']
            for i, card in enumerate(cards):
                for field in required_fields:
                    if field not in card:
                        self.log_result("GET /api/cards", False, f"Card {i} missing field: {field}", response_time)
                        return
                        
            # Verify IDs are 0-21
            card_ids = [card['id'] for card in cards]
            expected_ids = list(range(22))
            if sorted(card_ids) != expected_ids:
                self.log_result("GET /api/cards", False, f"Card IDs not 0-21: {sorted(card_ids)}", response_time)
                return
                
            # Verify no image_base64 in list (should be None)
            for card in cards:
                if card.get('image_base64') is not None:
                    self.log_result("GET /api/cards", False, "image_base64 should be None in card list", response_time)
                    return
                    
            self.log_result("GET /api/cards", True, f"22 cards with proper structure, IDs 0-21", response_time)
            
        except Exception as e:
            self.log_result("GET /api/cards", False, f"Exception: {str(e)}")
            
    def test_get_card_by_id(self, card_id: int, expected_name: str):
        """Test GET /api/cards/{id} - specific card retrieval"""
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/cards/{card_id}", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result(f"GET /api/cards/{card_id}", False, f"Status code: {response.status_code}", response_time)
                return
                
            card = response.json()
            
            # Verify card structure
            required_fields = ['id', 'name', 'image_url', 'keywords', 'meaning_upright', 'meaning_reversed', 'description', 'symbolism', 'yes_no_meaning']
            for field in required_fields:
                if field not in card:
                    self.log_result(f"GET /api/cards/{card_id}", False, f"Missing field: {field}", response_time)
                    return
                    
            # Verify correct ID and name
            if card['id'] != card_id:
                self.log_result(f"GET /api/cards/{card_id}", False, f"Wrong ID: expected {card_id}, got {card['id']}", response_time)
                return
                
            if card['name'] != expected_name:
                self.log_result(f"GET /api/cards/{card_id}", False, f"Wrong name: expected {expected_name}, got {card['name']}", response_time)
                return
                
            # Verify image_base64 is present for individual card
            if not card.get('image_base64'):
                self.log_result(f"GET /api/cards/{card_id}", False, "image_base64 missing for individual card", response_time)
                return
                
            self.log_result(f"GET /api/cards/{card_id}", True, f"Correct card: {card['name']}, has image_base64", response_time)
            
        except Exception as e:
            self.log_result(f"GET /api/cards/{card_id}", False, f"Exception: {str(e)}")
            
    def test_turkish_card_of_day(self):
        """Test POST /api/reading/card_of_day?language=tr - Turkish language support"""
        try:
            start_time = time.time()
            response = requests.post(f"{API_BASE}/reading/card_of_day?language=tr", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result("POST /api/reading/card_of_day (Turkish)", False, f"Status code: {response.status_code}", response_time)
                return
                
            reading = response.json()
            
            # Verify reading structure
            required_fields = ['id', 'reading_type', 'cards', 'interpretation', 'mode', 'timestamp']
            for field in required_fields:
                if field not in reading:
                    self.log_result("POST /api/reading/card_of_day (Turkish)", False, f"Missing field: {field}", response_time)
                    return
                    
            # Verify exactly 1 card
            if len(reading['cards']) != 1:
                self.log_result("POST /api/reading/card_of_day (Turkish)", False, f"Expected 1 card, got {len(reading['cards'])}", response_time)
                return
                
            # Verify card structure
            card_data = reading['cards'][0]
            if 'card' not in card_data or 'position' not in card_data or 'reversed' not in card_data:
                self.log_result("POST /api/reading/card_of_day (Turkish)", False, "Invalid card structure", response_time)
                return
                
            # Verify interpretation exists
            if not reading['interpretation'] or len(reading['interpretation']) < 10:
                self.log_result("POST /api/reading/card_of_day (Turkish)", False, "No interpretation generated", response_time)
                return
                
            # Check response time requirement (<2s)
            if response_time >= 2.0:
                self.log_result("POST /api/reading/card_of_day (Turkish)", False, f"Response time too slow: {response_time:.3f}s", response_time)
                return
                
            self.log_result("POST /api/reading/card_of_day (Turkish)", True, f"Turkish reading generated, mode: {reading['mode']}", response_time)
            
        except Exception as e:
            self.log_result("POST /api/reading/card_of_day (Turkish)", False, f"Exception: {str(e)}")
            
    def test_english_classic_tarot(self):
        """Test POST /api/reading/classic_tarot?language=en - English with AI interpretation"""
        try:
            start_time = time.time()
            response = requests.post(f"{API_BASE}/reading/classic_tarot?language=en", timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result("POST /api/reading/classic_tarot (English)", False, f"Status code: {response.status_code}", response_time)
                return
                
            reading = response.json()
            
            # Verify reading structure
            required_fields = ['id', 'reading_type', 'cards', 'interpretation', 'mode', 'timestamp']
            for field in required_fields:
                if field not in reading:
                    self.log_result("POST /api/reading/classic_tarot (English)", False, f"Missing field: {field}", response_time)
                    return
                    
            # Verify exactly 3 cards
            if len(reading['cards']) != 3:
                self.log_result("POST /api/reading/classic_tarot (English)", False, f"Expected 3 cards, got {len(reading['cards'])}", response_time)
                return
                
            # Verify positions
            expected_positions = ["Past", "Present", "Future"]
            actual_positions = [card['position'] for card in reading['cards']]
            if actual_positions != expected_positions:
                self.log_result("POST /api/reading/classic_tarot (English)", False, f"Wrong positions: {actual_positions}", response_time)
                return
                
            # Verify interpretation exists
            if not reading['interpretation'] or len(reading['interpretation']) < 10:
                self.log_result("POST /api/reading/classic_tarot (English)", False, "No interpretation generated", response_time)
                return
                
            # Check response time requirement (<2s for fallback, <15s for AI)
            if response_time >= 15.0:
                self.log_result("POST /api/reading/classic_tarot (English)", False, f"Response time too slow: {response_time:.3f}s", response_time)
                return
                
            self.log_result("POST /api/reading/classic_tarot (English)", True, f"3-card reading generated, mode: {reading['mode']}", response_time)
            
        except Exception as e:
            self.log_result("POST /api/reading/classic_tarot (English)", False, f"Exception: {str(e)}")
            
    def test_all_reading_types_health_check(self):
        """Basic health check of all 5 reading types"""
        reading_types = [
            ("card_of_day", 1),
            ("classic_tarot", 3),
            ("path_of_day", 4),
            ("couples_tarot", 5),
            ("yes_no", 1)
        ]
        
        for reading_type, expected_cards in reading_types:
            try:
                start_time = time.time()
                url = f"{API_BASE}/reading/{reading_type}"
                if reading_type == "yes_no":
                    url += "?question=Will I be successful?"
                    
                response = requests.post(url, timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code != 200:
                    self.log_result(f"Health check: {reading_type}", False, f"Status code: {response.status_code}", response_time)
                    continue
                    
                reading = response.json()
                
                # Basic structure check
                if 'cards' not in reading or 'interpretation' not in reading:
                    self.log_result(f"Health check: {reading_type}", False, "Missing cards or interpretation", response_time)
                    continue
                    
                # Card count check
                if len(reading['cards']) != expected_cards:
                    self.log_result(f"Health check: {reading_type}", False, f"Expected {expected_cards} cards, got {len(reading['cards'])}", response_time)
                    continue
                    
                # Response time check
                if response_time >= 10.0:
                    self.log_result(f"Health check: {reading_type}", False, f"Response time too slow: {response_time:.3f}s", response_time)
                    continue
                    
                self.log_result(f"Health check: {reading_type}", True, f"{expected_cards} cards, interpretation generated", response_time)
                
            except Exception as e:
                self.log_result(f"Health check: {reading_type}", False, f"Exception: {str(e)}")
                
    def test_reading_types_endpoint(self):
        """Test GET /api/reading-types endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/reading-types", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result("GET /api/reading-types", False, f"Status code: {response.status_code}", response_time)
                return
                
            reading_types = response.json()
            
            # Verify exactly 5 reading types
            if len(reading_types) != 5:
                self.log_result("GET /api/reading-types", False, f"Expected 5 reading types, got {len(reading_types)}", response_time)
                return
                
            # Verify structure
            required_fields = ['id', 'name', 'description', 'card_count', 'positions']
            for rt in reading_types:
                for field in required_fields:
                    if field not in rt:
                        self.log_result("GET /api/reading-types", False, f"Missing field: {field}", response_time)
                        return
                        
            self.log_result("GET /api/reading-types", True, "5 reading types with proper structure", response_time)
            
        except Exception as e:
            self.log_result("GET /api/reading-types", False, f"Exception: {str(e)}")
            
    def test_readings_endpoint(self):
        """Test GET /api/readings endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{API_BASE}/readings", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                self.log_result("GET /api/readings", False, f"Status code: {response.status_code}", response_time)
                return
                
            readings = response.json()
            
            # Should return a list (may be empty)
            if not isinstance(readings, list):
                self.log_result("GET /api/readings", False, "Response is not a list", response_time)
                return
                
            self.log_result("GET /api/readings", True, f"Retrieved {len(readings)} readings", response_time)
            
        except Exception as e:
            self.log_result("GET /api/readings", False, f"Exception: {str(e)}")
            
    def run_all_tests(self):
        """Run all regression tests"""
        print("=" * 80)
        print("TAROT API REGRESSION TEST SUITE - SHIP-READY VERIFICATION")
        print("=" * 80)
        print()
        
        # Priority Tests (Critical for Production)
        print("🔥 PRIORITY TESTS (Critical for Production)")
        print("-" * 50)
        
        # 1. GET /api/cards
        self.test_get_cards_endpoint()
        
        # 2. GET /api/cards/{id} - test with specific IDs
        self.test_get_card_by_id(0, "The Fool")
        self.test_get_card_by_id(20, "Judgement")
        
        # 3. POST /api/reading/card_of_day?language=tr
        self.test_turkish_card_of_day()
        
        # 4. POST /api/reading/classic_tarot?language=en
        self.test_english_classic_tarot()
        
        print()
        print("🏥 HEALTH CHECK TESTS")
        print("-" * 50)
        
        # 5. Basic health check of all 5 reading types
        self.test_all_reading_types_health_check()
        
        # Additional endpoints
        self.test_reading_types_endpoint()
        self.test_readings_endpoint()
        
        print()
        print("=" * 80)
        print("TEST RESULTS SUMMARY")
        print("=" * 80)
        
        for result in self.results:
            print(f"{result['status']} - {result['test']} ({result['response_time']})")
            if not result['passed'] and result['details']:
                print(f"    └─ {result['details']}")
                
        print()
        print(f"TOTAL: {self.passed_tests}/{self.total_tests} tests passed")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED - BACKEND IS SHIP-READY!")
            return True
        else:
            print(f"❌ {self.total_tests - self.passed_tests} TESTS FAILED - NEEDS ATTENTION")
            return False

def main():
    """Main test execution"""
    tester = TarotAPITester()
    success = tester.run_all_tests()
    
    # Save detailed results to file
    with open("/app/test_results_detailed.json", "w") as f:
        json.dump(tester.results, f, indent=2)
    
    print(f"\nDetailed results saved to: /app/test_results_detailed.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())