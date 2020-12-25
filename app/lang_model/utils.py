
def map_language_code(language_code: str) -> str:
    languages = {
        "da": "Danish",
        "sv": "Swedish",
        "no": "Norwegian"
    }

    if language_code not in languages:
        raise ValueError("Language not supported")

    return languages[language_code]