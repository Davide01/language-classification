from fastapi import FastAPI

from lang_model.recognize import RecognizeLang

app = FastAPI()


@app.get(
    "/lang",
    summary="Recognizes the language of the provided text.",
    response_description="Language of the text",
)
def language(text: str):
    try:
        recognize = RecognizeLang()
        language = recognize.recognize(text)
        print(f"Language {language}")
        return str(language)
    except ValueError as ve:
        return ve.args