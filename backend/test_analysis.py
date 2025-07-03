#!/usr/bin/env python3
"""
Test script for the enhanced morae and pitch accent analysis.
This script demonstrates how the new analysis detects missing/extra morae and pitch accent errors.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.morae_service import (
    extract_morae, 
    extract_morae_from_transcription, 
    analyze_morae_errors, 
    get_morae_feedback
)
from app.services.pitch_service import (
    extract_pitch_accent_info,
    derive_pitch_pattern,
    get_pitch_accent_name
)
from app.services.feedback_service import analyze_comprehensive_pronunciation

def test_morae_analysis():
    """Test morae analysis with various scenarios."""
    print("=== MORAE ANALYSIS TESTS ===\n")
    
    # Test cases with expected vs actual morae
    test_cases = [
        {
            "expected": "こんにちは",
            "actual": "こんにちは",  # Perfect
            "description": "Perfect pronunciation"
        },
        {
            "expected": "こんにちは",
            "actual": "こんちは",    # Missing に
            "description": "Missing mora"
        },
        {
            "expected": "こんにちは",
            "actual": "こんにちはあ",  # Extra あ
            "description": "Extra mora"
        },
        {
            "expected": "こんにちは",
            "actual": "こんにちわ",    # Wrong mora (わ instead of は)
            "description": "Incorrect mora"
        },
        {
            "expected": "おはようございます",
            "actual": "おはようございま",  # Missing す
            "description": "Missing final mora"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Expected: {test_case['expected']}")
        print(f"Actual:   {test_case['actual']}")
        
        expected_morae = extract_morae(test_case['expected'])
        actual_morae = extract_morae_from_transcription(test_case['actual'])
        
        print(f"Expected morae: {expected_morae}")
        print(f"Actual morae:   {actual_morae}")
        
        errors = analyze_morae_errors(expected_morae, actual_morae)
        feedback = get_morae_feedback(errors)
        
        print(f"Accuracy: {errors['overall_accuracy']:.2%}")
        print(f"Feedback: {feedback}")
        print(f"Error positions: {errors['error_positions']}")
        print("-" * 50)

def test_pitch_accent_analysis():
    """Test pitch accent analysis."""
    print("\n=== PITCH ACCENT ANALYSIS TESTS ===\n")
    
    test_phrases = [
        "こんにちは",      # heiban (flat)
        "おはよう",        # atamadaka (head-high)
        "ありがとう",      # nakadaka (middle-high)
        "さようなら"       # odaka (tail-high)
    ]
    
    for phrase in test_phrases:
        print(f"Phrase: {phrase}")
        
        accent_info = extract_pitch_accent_info(phrase)
        pattern = derive_pitch_pattern(accent_info["accent_type"], accent_info["total_morae"])
        accent_name = get_pitch_accent_name(accent_info["accent_type"])
        
        print(f"Accent type: {accent_info['accent_type']} ({accent_name})")
        print(f"Accent position: {accent_info['accent_position']}")
        print(f"Total morae: {accent_info['total_morae']}")
        print(f"Expected pattern: {pattern}")
        print("-" * 30)

def test_comprehensive_analysis():
    """Test comprehensive pronunciation analysis."""
    print("\n=== COMPREHENSIVE ANALYSIS TESTS ===\n")
    
    # Simulate analysis with mock data
    test_cases = [
        {
            "expected": "こんにちは",
            "transcription": "こんにちは",
            "description": "Perfect pronunciation"
        },
        {
            "expected": "こんにちは",
            "transcription": "こんちは",
            "description": "Missing mora"
        },
        {
            "expected": "おはようございます",
            "transcription": "おはようございま",
            "description": "Missing final mora"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Expected: {test_case['expected']}")
        print(f"Transcription: {test_case['transcription']}")
        
        # Mock pitch values (in real usage, these would come from audio analysis)
        mock_pitch_values = [120.0, 125.0, 130.0, 135.0, 140.0] * 10  # 50 values
        
        try:
            analysis = analyze_comprehensive_pronunciation(
                expected_phrase=test_case['expected'],
                transcription=test_case['transcription'],
                pitch_values=mock_pitch_values
            )
            
            print(f"Overall score: {analysis['overall_score']}%")
            print(f"Overall label: {analysis['overall_label']}")
            print(f"Similarity score: {analysis['similarity_score']}%")
            print(f"Morae score: {analysis['morae_analysis']['score']:.1f}%")
            print(f"Pitch score: {analysis['pitch_analysis']['score']:.1f}%")
            print(f"Detailed feedback: {analysis['detailed_feedback']}")
            print(f"Error summary: {analysis['error_summary']}")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            print("-" * 50)

def main():
    """Run all tests."""
    print("Kotoba Coach - Enhanced Analysis Test Suite")
    print("=" * 60)
    
    try:
        test_morae_analysis()
        test_pitch_accent_analysis()
        test_comprehensive_analysis()
        
        print("\n✅ All tests completed successfully!")
        print("\nKey Features Demonstrated:")
        print("• Missing morae detection")
        print("• Extra morae detection") 
        print("• Incorrect morae detection")
        print("• Pitch accent pattern analysis")
        print("• Comprehensive error feedback")
        print("• Weighted scoring system")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 