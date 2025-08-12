from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import unicodedata
import codecs

try:
    import regex as re  # supports \X grapheme segmentation
    _HAS_REGEX = True
except ImportError:
    import re
    _HAS_REGEX = False

app = FastAPI(title="Character Counter API")

# CORS: safe, permissive (you can tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to specific origins/domains
    allow_methods=["*"],
    allow_headers=["*"],
)

class CountRequest(BaseModel):
    text: str
    include: list[str] | None = None
    encoding: str = "utf-8"
    normalize: str | None = Field(default=None, pattern="^(NFC|NFD|NFKC|NFKD)$")

class CountResponse(BaseModel):
    text: str
    results: dict
    normalization: dict | None = None

@app.get("/")
def root():
    return {"status": "ok", "service": "charcount-api"}

@app.post("/count", response_model=CountResponse)
def count_characters(req: CountRequest):
    include = req.include or ["pythonLen"]
    text = req.text

    # Normalize first if requested
    applied = False
    form = None
    if req.normalize:
        form = req.normalize
        text = unicodedata.normalize(form, text)
        applied = True

    results = {}

    if "pythonLen" in include:
        results["pythonLen"] = len(text)

    if "bytes" in include:
        try:
            codecs.lookup(req.encoding)
        except LookupError:
            raise HTTPException(status_code=400, detail=f"Unsupported encoding: {req.encoding}")
        results["bytes"] = {"value": len(text.encode(req.encoding)), "encoding": req.encoding}

    if "graphemes" in include:
        if _HAS_REGEX:
            results["graphemes"] = len(re.findall(r"\X", text))
        else:
            # Fallback = code points (documented limitation)
            results["graphemes"] = len(text)

    normalization = {"applied": applied}
    if applied:
        normalization["form"] = form

    return CountResponse(text=text, results=results, normalization=normalization)
