#!/usr/bin/env python3
"""
SussyBaka - A fun application that combines 'sus' and 'baka' culture
"""

import random
import sys


class SussyBaka:
    """Main SussyBaka class for detecting sus behavior"""
    
    def __init__(self):
        self.sus_level = 0
        self.baka_level = 0
    
    def check_sussiness(self, action):
        """Check how sus an action is"""
        sus_keywords = ['vent', 'emergency', 'imposter', 'kill', 'sabotage']
        sus_count = sum(1 for keyword in sus_keywords if keyword in action.lower())
        self.sus_level += sus_count * 20
        return sus_count > 0
    
    def check_baka_level(self, intelligence_score):
        """Check the baka (foolishness) level"""
        if intelligence_score < 50:
            self.baka_level = 100 - intelligence_score
            return "Very baka!"
        elif intelligence_score < 75:
            self.baka_level = 75 - intelligence_score // 2
            return "A bit baka"
        else:
            self.baka_level = 0
            return "Not baka at all"
    
    def get_verdict(self):
        """Get the final sussybaka verdict"""
        if self.sus_level > 50 and self.baka_level > 50:
            return "🚨 ULTIMATE SUSSYBAKA DETECTED! 🚨"
        elif self.sus_level > 50:
            return "⚠️ Very sus detected!"
        elif self.baka_level > 50:
            return "🤦 Such a baka!"
        else:
            return "✅ All good, not sussybaka"


def main():
    """Main function to run the sussybaka checker"""
    print("=" * 50)
    print("🎮 Welcome to SussyBaka Detector! 🎮")
    print("=" * 50)
    
    checker = SussyBaka()
    
    # Interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        print("\nInteractive mode enabled!")
        action = input("\nDescribe an action to check for sussiness: ")
        checker.check_sussiness(action)
        
        try:
            intelligence = int(input("Rate your intelligence (0-100): "))
            checker.check_baka_level(intelligence)
        except ValueError:
            print("Invalid input! That's pretty baka...")
            checker.baka_level = 80
    else:
        # Demo mode
        test_action = "I saw someone vent in electrical"
        print(f"\nTesting action: '{test_action}'")
        is_sus = checker.check_sussiness(test_action)
        print(f"Sus detected: {is_sus}")
        print(f"Sus level: {checker.sus_level}%")
        
        test_intelligence = random.randint(0, 100)
        print(f"\nTesting intelligence score: {test_intelligence}")
        baka_result = checker.check_baka_level(test_intelligence)
        print(f"Baka verdict: {baka_result}")
        print(f"Baka level: {checker.baka_level}%")
    
    # Final verdict
    print(f"\n{'=' * 50}")
    print(f"Final Verdict: {checker.get_verdict()}")
    print(f"{'=' * 50}")
    print(f"\nSus Level: {checker.sus_level}%")
    print(f"Baka Level: {checker.baka_level}%")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
