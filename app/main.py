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
        recognize = RecognizeLang(model_name="lstm")
        language = recognize.recognize(text)
        return str(language)
    except ValueError as ve:
        return ve.args