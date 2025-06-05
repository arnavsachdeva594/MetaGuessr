# backend/app/main.py

import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tag_suggester import TagSuggester

app = FastAPI(title="GeoMeta+ Tag Recommendation API")

# Allow CORS from the frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, lock this down
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize a single TagSuggester instance on startup
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
    # 1) Ensure it’s a GeoJSON
    if file.content_type not in ("application/json", "application/geo+json", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a GeoJSON (.json)")

    # 2) Read and parse
    try:
        raw = await file.read()
        geojson = json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse GeoJSON: {e}")

    # 3) Generate suggestions (empty list if nothing to infer)
    suggestions = suggester.suggest_tags(geojson, top_k=5)
    return {"suggested_tags": suggestions}


# If you’d like to run via `uvicorn backend.app.main:app --reload`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
