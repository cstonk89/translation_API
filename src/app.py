from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from shared_utils.utils import (
    TranslationRequest,
    TranslationResponse,
    profanity_check,
    supported_languages,
)
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import os

model_name = os.getenv("model_name", "facebook/m2m100_418M")

app = FastAPI()


@app.get("/supported_languages")
def return_supported_languages():
    return supported_languages


@app.on_event("startup")
def load_model():
    print("Loading model...")
    app.state.model = M2M100ForConditionalGeneration.from_pretrained(model_name)
    app.state.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    print("Model loaded.")


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)


@app.post("/translate", response_model=TranslationResponse)
def translate_(request: TranslationRequest):

    if request.target_language not in supported_languages:
        raise HTTPException(
            status_code=400, detail="Unsupported target language selected"
        )

    if request.source_language not in supported_languages:
        raise HTTPException(
            status_code=400, detail="Unsupported source language selected"
        )

    if profanity_check(request.source_text) == 1:
        raise HTTPException(status_code=400, detail="Remove profanity from input")

    tokenizer = app.state.tokenizer
    model = app.state.model

    tokenizer.src_lang = request.source_language

    encoded = tokenizer(request.source_text, return_tensors="pt")

    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.get_lang_id(request.target_language),
    )

    translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return TranslationResponse(
        source_text=request.source_text,
        source_language=request.source_language,
        target_language=request.target_language,
        translation=translated,
    )
