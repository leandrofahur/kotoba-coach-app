from typing import List
from models.phrase import Phrase

def get_all_phrases() -> List[Phrase]:
    return [
        Phrase(id="1", 
               text="おはようございます", 
               romaji="ohayou gozaimasu", 
               translation="Good morning", 
               audio_url="/assets/audio/ohayougozaimasu.mp3"),
        Phrase(id="2", 
               text="こんにちは", 
               romaji="konnichiwa", 
               translation="Good afternoon", 
               audio_url="/assets/audio/konnichiwa.mp3"),
        Phrase(id="3", 
               text="こんばんは", 
               romaji="konbanwa", 
               translation="Good evening", 
               audio_url="/assets/audio/konbanwa.mp3"),        
    ]

def get_phrase_by_id(id: str) -> Phrase:
    return next((phrase for phrase in get_all_phrases() if phrase.id == id), None)