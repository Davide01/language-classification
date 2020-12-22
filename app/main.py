from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get(
    "/lang",
    summary="Recognizes the language of the provided text.",
    response_description="Language of the text",
)
async def language(text: str):
    return text