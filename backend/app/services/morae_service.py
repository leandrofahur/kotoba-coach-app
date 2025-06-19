import pyopenjtalk

def extract_morae(phrase: str) -> list[str]:
    """
    Converts a Japanese phrase into a list of morae (hiragana units).
    """
    g2p_hiragana = pyopenjtalk.g2p(phrase)
    return g2p_hiragana.split(" ")