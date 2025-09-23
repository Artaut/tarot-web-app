#!/usr/bin/env python3
"""
Backend API Testing for Tarot App - Turkish Language Support Focus
Tests the updated endpoints with Turkish language support as requested
"""

import requests
import json
import sys
from typing import Dict, List, Any

# Use the production backend URL from frontend/.env
BACKEND_URL = "https://divinereader.preview.emergentagent.com/api"

def test_get_cards_turkish():
    """Test GET /api/cards?language=tr - should return exactly 22 cards with Turkish names, no image_base64"""
    print("🧪 Testing GET /api/cards?language=tr...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/cards?language=tr", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
        cards = response.json()
        print(f"   Cards returned: {len(cards)}")
        
        # Check exactly 22 cards
        if len(cards) != 22:
            print(f"   ❌ FAILED: Expected exactly 22 cards, got {len(cards)}")
            return False
            
        # Check unique IDs 0-21
        card_ids = [card['id'] for card in cards]
        expected_ids = list(range(22))
        if sorted(card_ids) != expected_ids:
            print(f"   ❌ FAILED: Expected IDs 0-21, got {sorted(card_ids)}")
            return False
            
        # Check no image_base64 in list items
        for card in cards:
            if 'image_base64' in card and card['image_base64'] is not None:
                print(f"   ❌ FAILED: Found image_base64 in list item (card {card['id']})")
                return False
                
        # Check Turkish names are present
        turkish_names_found = 0
        for card in cards:
            if 'name' in card and any(char in card['name'] for char in 'çğıöşüÇĞIÖŞÜ'):
                turkish_names_found += 1
                
        print(f"   Turkish names found: {turkish_names_found}")
        print(f"   Sample card names: {[cards[i]['name'] for i in [0, 9, 20]]}")
        
        print("   ✅ PASSED: GET /api/cards?language=tr")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def test_get_card_detail_turkish():
    """Test GET /api/cards/20?language=tr - should include image_base64 and Turkish name 'Yargı'"""
    print("🧪 Testing GET /api/cards/20?language=tr...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/cards/20?language=tr", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
        card = response.json()
        print(f"   Card ID: {card.get('id')}")
        print(f"   Card Name: {card.get('name')}")
        
        # Check card ID is 20
        if card.get('id') != 20:
            print(f"   ❌ FAILED: Expected card ID 20, got {card.get('id')}")
            return False
            
        # Check Turkish name is 'Yargı'
        if card.get('name') != 'Yargı':
            print(f"   ❌ FAILED: Expected name 'Yargı', got '{card.get('name')}'")
            return False
            
        # Check image_base64 is present and non-empty
        image_base64 = card.get('image_base64')
        if not image_base64:
            print(f"   ❌ FAILED: image_base64 is missing or empty")
            return False
            
        if not image_base64.startswith('data:'):
            print(f"   ❌ FAILED: image_base64 is not a valid data URI")
            return False
            
        print(f"   Image base64 length: {len(image_base64)}")
        print(f"   Image base64 prefix: {image_base64[:50]}...")
        
        # Check TarotCard model structure
        required_fields = ['id', 'name', 'image_url', 'keywords', 'meaning_upright', 
                          'meaning_reversed', 'description', 'symbolism', 'yes_no_meaning']
        for field in required_fields:
            if field not in card:
                print(f"   ❌ FAILED: Missing required field '{field}'")
                return False
                
        print("   ✅ PASSED: GET /api/cards/20?language=tr")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def test_get_card_hermit_turkish():
    """Test GET /api/cards/9?language=tr - should include image_base64 and correct Turkish name 'Ermiş'"""
    print("🧪 Testing GET /api/cards/9?language=tr...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/cards/9?language=tr", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
        card = response.json()
        print(f"   Card ID: {card.get('id')}")
        print(f"   Card Name: {card.get('name')}")
        
        # Check card ID is 9
        if card.get('id') != 9:
            print(f"   ❌ FAILED: Expected card ID 9, got {card.get('id')}")
            return False
            
        # Check Turkish name is 'Ermiş'
        if card.get('name') != 'Ermiş':
            print(f"   ❌ FAILED: Expected name 'Ermiş', got '{card.get('name')}'")
            return False
            
        # Check image_base64 is present and non-empty
        image_base64 = card.get('image_base64')
        if not image_base64:
            print(f"   ❌ FAILED: image_base64 is missing or empty")
            return False
            
        if not image_base64.startswith('data:'):
            print(f"   ❌ FAILED: image_base64 is not a valid data URI")
            return False
            
        print(f"   Image base64 length: {len(image_base64)}")
        
        print("   ✅ PASSED: GET /api/cards/9?language=tr")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def test_card_of_day_turkish():
    """Test POST /api/reading/card_of_day?language=tr - should work with Turkish fields"""
    print("🧪 Testing POST /api/reading/card_of_day?language=tr...")
    
    try:
        response = requests.post(f"{BACKEND_URL}/reading/card_of_day?language=tr", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
        reading = response.json()
        print(f"   Reading Type: {reading.get('reading_type')}")
        print(f"   Cards Count: {len(reading.get('cards', []))}")
        
        # Check reading type
        if reading.get('reading_type') != 'card_of_day':
            print(f"   ❌ FAILED: Expected reading_type 'card_of_day', got '{reading.get('reading_type')}'")
            return False
            
        # Check exactly 1 card
        cards = reading.get('cards', [])
        if len(cards) != 1:
            print(f"   ❌ FAILED: Expected 1 card, got {len(cards)}")
            return False
            
        # Check card has Turkish fields
        card_info = cards[0].get('card', {})
        card_name = card_info.get('name', '')
        print(f"   Card Name: {card_name}")
        
        # Check if interpretation contains Turkish text
        interpretation = reading.get('interpretation', '')
        has_turkish = any(word in interpretation.lower() for word in ['bugün', 'kart', 'günün', 'öner'])
        print(f"   Has Turkish interpretation: {has_turkish}")
        print(f"   Interpretation preview: {interpretation[:100]}...")
        
        # Check required reading structure
        required_fields = ['id', 'reading_type', 'cards', 'interpretation', 'timestamp']
        for field in required_fields:
            if field not in reading:
                print(f"   ❌ FAILED: Missing required field '{field}'")
                return False
                
        print("   ✅ PASSED: POST /api/reading/card_of_day?language=tr")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def test_reading_types():
    """Test GET /api/reading-types - smoke test"""
    print("🧪 Testing GET /api/reading-types...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/reading-types", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            return False
            
        reading_types = response.json()
        print(f"   Reading types count: {len(reading_types)}")
        
        if len(reading_types) != 5:
            print(f"   ❌ FAILED: Expected 5 reading types, got {len(reading_types)}")
            return False
            
        print("   ✅ PASSED: GET /api/reading-types")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def test_get_readings():
    """Test GET /api/readings - smoke test after creating readings"""
    print("🧪 Testing GET /api/readings...")
    
    try:
        # First create 2 readings
        print("   Creating 2 readings first...")
        requests.post(f"{BACKEND_URL}/reading/card_of_day", timeout=10)
        requests.post(f"{BACKEND_URL}/reading/classic_tarot", timeout=10)
        
        # Now get readings
        response = requests.get(f"{BACKEND_URL}/readings?limit=2", timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ FAILED: Expected 200, got {response.status_code}")
            return False
            
        readings = response.json()
        print(f"   Readings returned: {len(readings)}")
        
        if len(readings) == 0:
            print(f"   ❌ FAILED: No readings returned")
            return False
            
        print("   ✅ PASSED: GET /api/readings")
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: Exception occurred: {str(e)}")
        return False

def main():
    """Run all backend tests"""
    print("🚀 Starting Backend API Tests for Tarot App - Turkish Language Focus")
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 60)
    
    tests = [
        test_get_cards_turkish,
        test_get_card_detail_turkish,
        test_get_card_hermit_turkish,
        test_card_of_day_turkish,
        test_reading_types,
        test_get_readings
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ FAILED: Unexpected error in {test.__name__}: {str(e)}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("❌ Some tests failed!")
        return False
    else:
        print("✅ All tests passed!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)