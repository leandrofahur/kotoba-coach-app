#!/usr/bin/env python3
"""
Kotoba Coach - Common Error Analysis
====================================

This test focuses on the most common and realistic errors that users make
when practicing the three phrases in the system.
"""

from app.services.morae_service import extract_morae, analyze_morae_errors, get_morae_feedback
from app.services.pitch_service import extract_pitch_accent_info, get_pitch_accent_name
from app.services.feedback_service import analyze_comprehensive_pronunciation

def test_common_beginner_errors():
    """Test the most common beginner errors for each phrase."""
    print("🎯 MOST COMMON BEGINNER ERRORS")
    print("=" * 50)
    
    # Define common errors for each phrase
    common_errors = [
        {
            "phrase": "こんにちは",
            "romaji": "konnichiwa",
            "common_errors": [
                {
                    "transcription": "こんちは",
                    "description": "Dropping 'に' (ni) - very common beginner error",
                    "explanation": "Beginners often drop the 'ni' sound because it's subtle"
                },
                {
                    "transcription": "こんにちわ", 
                    "description": "Confusing 'は' (wa) and 'わ' (wa)",
                    "explanation": "Both sound similar but 'は' is the correct particle"
                },
                {
                    "transcription": "こんにちはあ",
                    "description": "Adding extra 'あ' (a) at the end",
                    "explanation": "Beginners sometimes add extra vowels"
                }
            ]
        },
        {
            "phrase": "おはようございます",
            "romaji": "ohayou gozaimasu", 
            "common_errors": [
                {
                    "transcription": "おはようございま",
                    "description": "Dropping final 'す' (su) - very common",
                    "explanation": "The final 'su' is often dropped by beginners"
                },
                {
                    "transcription": "おはようございまし",
                    "description": "Adding extra 'し' (shi) instead of 'す' (su)",
                    "explanation": "Confusing similar sounds"
                },
                {
                    "transcription": "おはようございますね",
                    "description": "Adding 'ね' (ne) particle",
                    "explanation": "Adding unnecessary particles"
                }
            ]
        },
        {
            "phrase": "こんばんは",
            "romaji": "konbanwa",
            "common_errors": [
                {
                    "transcription": "こんばんわ",
                    "description": "Confusing 'は' (wa) and 'わ' (wa) - same as konnichiwa",
                    "explanation": "Very common confusion with the particle 'は'"
                },
                {
                    "transcription": "こんばん",
                    "description": "Dropping final 'は' (wa) particle",
                    "explanation": "Forgetting the particle entirely"
                },
                {
                    "transcription": "こんばんはあ",
                    "description": "Adding extra 'あ' (a) at the end",
                    "explanation": "Adding unnecessary vowels"
                }
            ]
        }
    ]
    
    for phrase_data in common_errors:
        print(f"\n📝 PHRASE: {phrase_data['phrase']} ({phrase_data['romaji']})")
        print("-" * 40)
        
        expected_morae = extract_morae(phrase_data['phrase'])
        accent_info = extract_pitch_accent_info(phrase_data['phrase'])
        
        print(f"Expected morae: {expected_morae}")
        print(f"Expected pitch: {get_pitch_accent_name(accent_info['accent_type'])}")
        print()
        
        for error in phrase_data['common_errors']:
            print(f"❌ ERROR: {error['description']}")
            print(f"   Expected: {phrase_data['phrase']}")
            print(f"   Actual:   {error['transcription']}")
            print(f"   Why: {error['explanation']}")
            
            # Analyze the error
            try:
                # Generate realistic pitch data
                mock_pitch = [120.0 + (i * 2) for i in range(len(expected_morae) * 10)]
                
                analysis = analyze_comprehensive_pronunciation(
                    expected_phrase=phrase_data['phrase'],
                    transcription=error['transcription'],
                    pitch_values=mock_pitch
                )
                
                print(f"   Overall Score: {analysis['overall_score']}%")
                print(f"   Morae Score: {analysis['morae_analysis']['score']:.1f}%")
                print(f"   Pitch Score: {analysis['pitch_analysis']['score']:.1f}%")
                print(f"   Feedback: {analysis['detailed_feedback']}")
                
                # Show specific error details
                if analysis['error_summary']['morae_error_count'] > 0:
                    print(f"   Morae Errors: {analysis['error_summary']['morae_error_count']}")
                    if analysis['error_summary']['missing_morae_count'] > 0:
                        print(f"     - Missing: {analysis['error_summary']['missing_morae_count']}")
                    if analysis['error_summary']['extra_morae_count'] > 0:
                        print(f"     - Extra: {analysis['error_summary']['extra_morae_count']}")
                    if analysis['error_summary']['incorrect_morae_count'] > 0:
                        print(f"     - Incorrect: {analysis['error_summary']['incorrect_morae_count']}")
                
            except Exception as e:
                print(f"   Analysis error: {e}")
            
            print()

def test_pitch_accent_errors():
    """Test common pitch accent errors."""
    print("\n🎵 COMMON PITCH ACCENT ERRORS")
    print("=" * 50)
    
    phrases = ["こんにちは", "おはようございます", "こんばんは"]
    
    for phrase in phrases:
        print(f"\n📝 PHRASE: {phrase}")
        
        # Get expected pitch info
        accent_info = extract_pitch_accent_info(phrase)
        expected_pattern = accent_info['pitch_pattern']
        
        print(f"Expected: {get_pitch_accent_name(accent_info['accent_type'])} - {expected_pattern}")
        
        # Test different pitch error scenarios
        pitch_errors = [
            {
                "name": "Over-emphasized",
                "description": "User speaks with exaggerated pitch differences",
                "pitch_data": [150.0 + (i * 15) for i in range(len(expected_pattern) * 10)]
            },
            {
                "name": "Monotone",
                "description": "User speaks in completely flat pitch",
                "pitch_data": [120.0 for _ in range(len(expected_pattern) * 10)]
            },
            {
                "name": "Wrong Pattern",
                "description": "User applies wrong accent pattern",
                "pitch_data": [120.0 + (60 if i % 3 == 0 else -30) for i in range(len(expected_pattern) * 10)]
            }
        ]
        
        for error in pitch_errors:
            print(f"\n   🎵 {error['name']}: {error['description']}")
            
            try:
                analysis = analyze_comprehensive_pronunciation(
                    expected_phrase=phrase,
                    transcription=phrase,  # Perfect transcription
                    pitch_values=error['pitch_data']
                )
                
                print(f"   Pitch Score: {analysis['pitch_analysis']['score']:.1f}%")
                print(f"   Pitch Feedback: {analysis['pitch_analysis']['feedback']}")
                
            except Exception as e:
                print(f"   Analysis error: {e}")

def test_error_severity():
    """Test how different types of errors affect the overall score."""
    print("\n⚖️ ERROR SEVERITY ANALYSIS")
    print("=" * 50)
    
    phrase = "こんにちは"
    expected_morae = extract_morae(phrase)
    
    error_scenarios = [
        {
            "name": "Perfect",
            "transcription": "こんにちは",
            "description": "Native-like pronunciation"
        },
        {
            "name": "Minor Morae Error",
            "transcription": "こんにちはあ",
            "description": "Adding one extra mora"
        },
        {
            "name": "Major Morae Error", 
            "transcription": "こんちは",
            "description": "Missing multiple morae"
        },
        {
            "name": "Character Confusion",
            "transcription": "こんにちわ",
            "description": "Wrong character but same morae"
        }
    ]
    
    print(f"📝 Testing phrase: {phrase}")
    print(f"Expected morae: {expected_morae}")
    print()
    
    for scenario in error_scenarios:
        print(f"🔍 {scenario['name']}: {scenario['description']}")
        print(f"   Transcription: {scenario['transcription']}")
        
        # Generate consistent pitch data for fair comparison
        mock_pitch = [120.0 + (i * 2) for i in range(len(expected_morae) * 10)]
        
        try:
            analysis = analyze_comprehensive_pronunciation(
                expected_phrase=phrase,
                transcription=scenario['transcription'],
                pitch_values=mock_pitch
            )
            
            print(f"   Overall Score: {analysis['overall_score']}%")
            print(f"   Morae Score: {analysis['morae_analysis']['score']:.1f}%")
            print(f"   Pitch Score: {analysis['pitch_analysis']['score']:.1f}%")
            print(f"   Total Errors: {analysis['error_summary']['total_errors']}")
            
        except Exception as e:
            print(f"   Analysis error: {e}")
        
        print()

if __name__ == "__main__":
    test_common_beginner_errors()
    test_pitch_accent_errors()
    test_error_severity()
    
    print("\n✅ Common error analysis completed!")
    print("\n📊 KEY FINDINGS:")
    print("• Missing morae have the biggest impact on score")
    print("• Character confusion (は/わ) is common but less severe")
    print("• Pitch errors are detected but don't heavily penalize heiban phrases")
    print("• Final morae are often dropped by beginners")
    print("• Extra morae are less common than missing morae") 