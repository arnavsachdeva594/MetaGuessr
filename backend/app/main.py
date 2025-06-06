
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tag_suggester import TagSuggester

app = FastAPI(title="GeoMeta+ Tag Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

suggester = TagSuggester()


@app.post("/recommend_tags")
async def recommend_tags(file: UploadFile = File(...)):
    """
    Expects:
      - Content-Type: multipart/form-data
      - A file field named 'file' containing a valid GeoJSON file.
    Returns:
      { "suggested_tags": [ "roads", "buildings", ... ] }
    """
    if file.content_type not in ("application/json", "application/geo+json", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a GeoJSON (.json)")

    try:
        raw = await file.read()
        geojson = json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse GeoJSON: {e}")

    suggestions = suggester.suggest_tags(geojson, top_k=5)
    return {"suggested_tags": suggestions}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
