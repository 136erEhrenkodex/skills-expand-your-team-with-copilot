#!/usr/bin/env python3
"""
Unit tests for the SussyBaka detector
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import sussybaka
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sussybaka import SussyBaka


class TestSussyBaka(unittest.TestCase):
    """Test cases for SussyBaka class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checker = SussyBaka()
    
    def test_initialization(self):
        """Test that SussyBaka initializes with zero levels"""
        self.assertEqual(self.checker.sus_level, 0)
        self.assertEqual(self.checker.baka_level, 0)
    
    def test_sus_detection_with_keywords(self):
        """Test that sus keywords are detected"""
        result = self.checker.check_sussiness("I saw someone vent in electrical")
        self.assertTrue(result)
        self.assertGreater(self.checker.sus_level, 0)
    
    def test_sus_detection_without_keywords(self):
        """Test that normal actions are not flagged as sus"""
        result = self.checker.check_sussiness("I completed my tasks")
        self.assertFalse(result)
        self.assertEqual(self.checker.sus_level, 0)
    
    def test_baka_level_high(self):
        """Test baka level for low intelligence scores"""
        result = self.checker.check_baka_level(30)
        self.assertEqual(result, "Very baka!")
        self.assertGreater(self.checker.baka_level, 50)
    
    def test_baka_level_medium(self):
        """Test baka level for medium intelligence scores"""
        result = self.checker.check_baka_level(60)
        self.assertEqual(result, "A bit baka")
        self.assertLess(self.checker.baka_level, 50)
    
    def test_baka_level_low(self):
        """Test baka level for high intelligence scores"""
        result = self.checker.check_baka_level(90)
        self.assertEqual(result, "Not baka at all")
        self.assertEqual(self.checker.baka_level, 0)
    
    def test_ultimate_sussybaka_verdict(self):
        """Test ultimate sussybaka verdict"""
        self.checker.sus_level = 60
        self.checker.baka_level = 60
        verdict = self.checker.get_verdict()
        self.assertEqual(verdict, "🚨 ULTIMATE SUSSYBAKA DETECTED! 🚨")
    
    def test_sus_only_verdict(self):
        """Test sus-only verdict"""
        self.checker.sus_level = 60
        self.checker.baka_level = 30
        verdict = self.checker.get_verdict()
        self.assertEqual(verdict, "⚠️ Very sus detected!")
    
    def test_baka_only_verdict(self):
        """Test baka-only verdict"""
        self.checker.sus_level = 30
        self.checker.baka_level = 60
        verdict = self.checker.get_verdict()
        self.assertEqual(verdict, "🤦 Such a baka!")
    
    def test_all_good_verdict(self):
        """Test all-good verdict"""
        self.checker.sus_level = 30
        self.checker.baka_level = 30
        verdict = self.checker.get_verdict()
        self.assertEqual(verdict, "✅ All good, not sussybaka")
    
    def test_multiple_sus_keywords(self):
        """Test detection of multiple sus keywords"""
        result = self.checker.check_sussiness("The imposter will sabotage and kill everyone")
        self.assertTrue(result)
        self.assertEqual(self.checker.sus_level, 60)  # 3 keywords * 20


if __name__ == '__main__':
    unittest.main()
