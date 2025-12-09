"""Verification script for JSON Fixer Agent."""

import sys
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO

# Add parent directory to path so we can import modules
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.mobility.json_fixer import JsonFixerAgent

class TestJsonFixer(unittest.TestCase):
    
    def test_fix_missing_comma(self):
        """Test fixing a JSON with missing comma."""
        broken_json = '{"key1": "value1" "key2": "value2"}'
        error_msg = "Expecting ',' delimiter: line 1 column 18 (char 17)"
        
        # We need to mock the LLM response because we don't want to make real API calls in this unit test
        # However, for verification purposes in this task, I WANT to see if the real LLM can fix it.
        # So I will NOT mock it here, assuming I have access to the LLM via the config.
        # If I can't access real LLM, I will fail.
        
        print("\nTesting real LLM fix for missing comma...")
        fixer = JsonFixerAgent()
        result, error = fixer.fix_json(broken_json, error_msg, "Expected format: {key1: str, key2: str}")
        
        print(f"Result: {result}")
        print(f"Error: {error}")
        
        self.assertIsNone(error)
        self.assertEqual(result.get("key1"), "value1")
        self.assertEqual(result.get("key2"), "value2")

    def test_fix_unquoted_key(self):
        """Test fixing a JSON with unquoted keys."""
        broken_json = '{key1: "value1", key2: "value2"}'
        error_msg = "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
        
        print("\nTesting real LLM fix for unquoted keys...")
        fixer = JsonFixerAgent()
        result, error = fixer.fix_json(broken_json, error_msg, "Expected format: {key1: str, key2: str}")
        
        print(f"Result: {result}")
        print(f"Error: {error}")
        
        self.assertIsNone(error)
        self.assertEqual(result.get("key1"), "value1")
        
    def test_fix_trailing_comma(self):
        """Test fixing a JSON with trailing comma."""
        broken_json = '{"key1": "value1",}'
        error_msg = "Expecting property name enclosed in double quotes: line 1 column 18 (char 17)"
        
        print("\nTesting real LLM fix for trailing comma...")
        fixer = JsonFixerAgent()
        result, error = fixer.fix_json(broken_json, error_msg, "Expected format: {key1: str}")
        
        print(f"Result: {result}")
        print(f"Error: {error}")
        
        self.assertIsNone(error)
        self.assertEqual(result.get("key1"), "value1")

if __name__ == '__main__':
    unittest.main()
