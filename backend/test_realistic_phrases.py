#!/usr/bin/env python3
"""
Kotoba Coach - Realistic Phrase Analysis Test Suite
===================================================

This test suite demonstrates realistic pronunciation errors that users might make
when practicing the three phrases in the system:
1. こんにちは (konnichiwa) - "Good afternoon"
2. おはようございます (ohayou gozaimasu) - "Good morning"
3. こんばんは (konbanwa) - "Good evening"

Each test shows different types of morae and pitch errors that commonly occur.
"""

from app.services.morae_service import extract_morae, extract_morae_from_transcription, analyze_morae_errors, get_morae_feedback
from app.services.pitch_service import extract_pitch_accent_info, analyze_comprehensive_pitch, get_pitch_accent_name
from app.services.feedback_service import analyze_comprehensive_pronunciation

def test_realistic_phrase_errors():
    """Test realistic pronunciation errors for the three system phrases."""
    print("Kotoba Coach - Realistic Phrase Analysis Test Suite")
    print("=" * 60)
    print()
    
    # Define the three phrases in the system
    system_phrases = [
        {
            "id": "1",
            "text": "こんにちは",
            "romaji": "konnichiwa",
            "translation": "Good afternoon",
            "description": "Standard greeting"
        },
        {
            "id": "2", 
            "text": "おはようございます",
            "romaji": "ohayou gozaimasu",
            "translation": "Good morning",
            "description": "Formal morning greeting"
        },
        {
            "id": "3",
            "text": "こんばんは", 
            "romaji": "konbanwa",
            "translation": "Good evening",
            "description": "Evening greeting"
        }
    ]
    
    # Test scenarios for each phrase
    test_scenarios = [
        # Perfect pronunciation
        {
            "name": "Perfect Pronunciation",
            "description": "Native-like pronunciation",
            "pitch_pattern": "natural_flat"  # All phrases are heiban (flat)
        },
        
        # Common morae errors
        {
            "name": "Missing Mora",
            "description": "User drops a mora (common with beginners)",
            "pitch_pattern": "natural_flat"
        },
        {
            "name": "Extra Mora", 
            "description": "User adds an extra sound",
            "pitch_pattern": "natural_flat"
        },
        {
            "name": "Incorrect Mora",
            "description": "User substitutes one mora for another",
            "pitch_pattern": "natural_flat"
        },
        
        # Pitch accent errors
        {
            "name": "Wrong Pitch Pattern",
            "description": "User applies wrong pitch accent pattern",
            "pitch_pattern": "wrong_accent"
        },
        {
            "name": "Over-emphasized Pitch",
            "description": "User over-emphasizes pitch differences",
            "pitch_pattern": "over_emphasized"
        },
        {
            "name": "Flat Pitch (Monotone)",
            "description": "User speaks in monotone",
            "pitch_pattern": "monotone"
        }
    ]
    
    for phrase in system_phrases:
        print(f"📝 PHRASE: {phrase['text']} ({phrase['romaji']})")
        print(f"   Translation: {phrase['translation']}")
        print(f"   Description: {phrase['description']}")
        print("=" * 60)
        
        # Get expected morae and pitch info
        expected_morae = extract_morae(phrase['text'])
        accent_info = extract_pitch_accent_info(phrase['text'])
        
        print(f"Expected morae: {expected_morae}")
        print(f"Expected pitch: {get_pitch_accent_name(accent_info['accent_type'])} - {accent_info['pitch_pattern']}")
        print()
        
        for scenario in test_scenarios:
            print(f"🔍 TEST: {scenario['name']}")
            print(f"   Description: {scenario['description']}")
            
            # Generate realistic transcription and pitch based on scenario
            transcription, mock_pitch = generate_realistic_error(
                phrase['text'], 
                expected_morae, 
                scenario['name'], 
                scenario['pitch_pattern']
            )
            
            print(f"   Expected: {phrase['text']}")
            print(f"   Actual:   {transcription}")
            
            # Run comprehensive analysis
            try:
                analysis = analyze_comprehensive_pronunciation(
                    expected_phrase=phrase['text'],
                    transcription=transcription,
                    pitch_values=mock_pitch
                )
                
                print(f"   Overall Score: {analysis['overall_score']}% ({analysis['overall_label']})")
                print(f"   Morae Score: {analysis['morae_analysis']['score']:.1f}%")
                print(f"   Pitch Score: {analysis['pitch_analysis']['score']:.1f}%")
                print(f"   Feedback: {analysis['detailed_feedback']}")
                
                # Show specific errors
                if analysis['error_summary']['has_errors']:
                    print(f"   Errors: {analysis['error_summary']['total_errors']} total")
                    if analysis['error_summary']['morae_error_count'] > 0:
                        print(f"     - Morae: {analysis['error_summary']['morae_error_count']} errors")
                    if analysis['error_summary']['pitch_error_count'] > 0:
                        print(f"     - Pitch: {analysis['error_summary']['pitch_error_count']} errors")
                
            except Exception as e:
                print(f"   Error in analysis: {e}")
            
            print("-" * 40)
        
        print("\n" + "=" * 60 + "\n")

def generate_realistic_error(phrase: str, expected_morae: list, scenario: str, pitch_pattern: str) -> tuple:
    """
    Generate realistic transcription and pitch errors based on the scenario.
    """
    if scenario == "Perfect Pronunciation":
        return phrase, generate_natural_pitch(len(expected_morae), "natural_flat")
    
    elif scenario == "Missing Mora":
        # Remove one mora (common with beginners)
        if phrase == "こんにちは":
            return "こんちは", generate_natural_pitch(len(expected_morae) - 1, pitch_pattern)
        elif phrase == "おはようございます":
            return "おはようございま", generate_natural_pitch(len(expected_morae) - 2, pitch_pattern)
        elif phrase == "こんばんは":
            return "こんばん", generate_natural_pitch(len(expected_morae) - 1, pitch_pattern)
    
    elif scenario == "Extra Mora":
        # Add an extra mora
        if phrase == "こんにちは":
            return "こんにちはあ", generate_natural_pitch(len(expected_morae) + 1, pitch_pattern)
        elif phrase == "おはようございます":
            return "おはようございますね", generate_natural_pitch(len(expected_morae) + 2, pitch_pattern)
        elif phrase == "こんばんは":
            return "こんばんはあ", generate_natural_pitch(len(expected_morae) + 1, pitch_pattern)
    
    elif scenario == "Incorrect Mora":
        # Substitute one mora for another
        if phrase == "こんにちは":
            return "こんにちわ", generate_natural_pitch(len(expected_morae), pitch_pattern)
        elif phrase == "おはようございます":
            return "おはようございまし", generate_natural_pitch(len(expected_morae), pitch_pattern)
        elif phrase == "こんばんは":
            return "こんばんわ", generate_natural_pitch(len(expected_morae), pitch_pattern)
    
    elif scenario == "Wrong Pitch Pattern":
        # Apply wrong pitch accent pattern
        if phrase == "こんにちは":
            return phrase, generate_natural_pitch(len(expected_morae), "atamadaka")
        elif phrase == "おはようございます":
            return phrase, generate_natural_pitch(len(expected_morae), "nakadaka")
        elif phrase == "こんばんは":
            return phrase, generate_natural_pitch(len(expected_morae), "odaka")
    
    elif scenario == "Over-emphasized Pitch":
        # Over-emphasize pitch differences
        return phrase, generate_natural_pitch(len(expected_morae), "over_emphasized")
    
    elif scenario == "Flat Pitch (Monotone)":
        # Speak in monotone
        return phrase, generate_natural_pitch(len(expected_morae), "monotone")
    
    # Default fallback
    return phrase, generate_natural_pitch(len(expected_morae), "natural_flat")

def generate_natural_pitch(morae_count: int, pattern: str) -> list:
    """
    Generate realistic pitch values based on the pattern and morae count.
    """
    base_pitch = 120.0  # Base pitch in Hz
    pitch_variation = 20.0  # Natural variation
    
    if pattern == "natural_flat":
        # Natural heiban (flat) with slight variations
        return [base_pitch + (i * 2) for i in range(morae_count * 10)]
    
    elif pattern == "atamadaka":
        # Head-high pattern: high-low
        pitch_values = []
        for i in range(morae_count * 10):
            if i < morae_count * 5:  # First half high
                pitch_values.append(base_pitch + 40 + (i * 1))
            else:  # Second half low
                pitch_values.append(base_pitch - 20 + (i * 1))
        return pitch_values
    
    elif pattern == "nakadaka":
        # Middle-high pattern: low-high-low
        pitch_values = []
        for i in range(morae_count * 10):
            if i < morae_count * 3:  # First third low
                pitch_values.append(base_pitch - 10 + (i * 1))
            elif i < morae_count * 7:  # Middle third high
                pitch_values.append(base_pitch + 50 + (i * 1))
            else:  # Last third low
                pitch_values.append(base_pitch - 20 + (i * 1))
        return pitch_values
    
    elif pattern == "odaka":
        # Tail-high pattern: low-high
        pitch_values = []
        for i in range(morae_count * 10):
            if i < morae_count * 5:  # First half low
                pitch_values.append(base_pitch - 20 + (i * 1))
            else:  # Second half high
                pitch_values.append(base_pitch + 40 + (i * 1))
        return pitch_values
    
    elif pattern == "over_emphasized":
        # Over-emphasized pitch differences
        return [base_pitch + (i * 10) for i in range(morae_count * 10)]
    
    elif pattern == "monotone":
        # Monotone (very flat)
        return [base_pitch for _ in range(morae_count * 10)]
    
    elif pattern == "wrong_accent":
        # Wrong accent pattern (mix of patterns)
        pitch_values = []
        for i in range(morae_count * 10):
            if i % 3 == 0:
                pitch_values.append(base_pitch + 60)  # Very high
            elif i % 3 == 1:
                pitch_values.append(base_pitch - 30)  # Very low
            else:
                pitch_values.append(base_pitch + 10)  # Medium
        return pitch_values
    
    # Default fallback
    return [base_pitch + (i * 2) for i in range(morae_count * 10)]

def test_specific_error_patterns():
    """Test specific error patterns that commonly occur."""
    print("\n🎯 SPECIFIC ERROR PATTERN TESTS")
    print("=" * 60)
    
    # Common beginner errors
    common_errors = [
        {
            "phrase": "こんにちは",
            "error": "こんちは",
            "description": "Dropping 'に' (common beginner error)",
            "expected_morae": ['k', 'o', 'N', 'n', 'i', 'ch', 'i', 'w', 'a'],
            "actual_morae": ['k', 'o', 'N', 'ch', 'i', 'w', 'a']
        },
        {
            "phrase": "おはようございます",
            "error": "おはようございま",
            "description": "Dropping final 'す' (common error)",
            "expected_morae": ['o', 'h', 'a', 'y', 'o', 'o', 'g', 'o', 'z', 'a', 'i', 'm', 'a', 's', 'U'],
            "actual_morae": ['o', 'h', 'a', 'y', 'o', 'o', 'g', 'o', 'z', 'a', 'i', 'm', 'a']
        },
        {
            "phrase": "こんばんは",
            "error": "こんばんわ",
            "description": "Confusing 'は' and 'わ' (common confusion)",
            "expected_morae": ['k', 'o', 'N', 'b', 'a', 'N', 'w', 'a'],
            "actual_morae": ['k', 'o', 'N', 'b', 'a', 'N', 'w', 'a']  # Same morae, different character
        }
    ]
    
    for error_case in common_errors:
        print(f"\n📝 Testing: {error_case['description']}")
        print(f"   Expected: {error_case['phrase']}")
        print(f"   Actual:   {error_case['error']}")
        
        # Test morae analysis
        morae_errors = analyze_morae_errors(error_case['expected_morae'], error_case['actual_morae'])
        print(f"   Morae accuracy: {morae_errors['overall_accuracy']:.1f}%")
        print(f"   Morae feedback: {get_morae_feedback(morae_errors)}")
        
        # Test with realistic pitch
        mock_pitch = generate_natural_pitch(len(error_case['expected_morae']), "natural_flat")
        
        # Comprehensive analysis
        analysis = analyze_comprehensive_pronunciation(
            expected_phrase=error_case['phrase'],
            transcription=error_case['error'],
            pitch_values=mock_pitch
        )
        
        print(f"   Overall score: {analysis['overall_score']}%")
        print(f"   Detailed feedback: {analysis['detailed_feedback']}")

if __name__ == "__main__":
    test_realistic_phrase_errors()
    test_specific_error_patterns()
    print("\n✅ All realistic phrase tests completed!")
    print("\nKey Insights:")
    print("• Morae errors are more critical than pitch errors for overall score")
    print("• Pitch accent errors are common but less severe for heiban phrases")
    print("• Missing morae are the most common beginner errors")
    print("• Character confusion (は/わ) is a common issue")
    print("• Final morae are often dropped by beginners") 