# backend/app/tag_suggester.py

import torch
import numpy as np
import json
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


class TagSuggester:
    """
    Uses a pre-trained BERT to embed both:
      1) a small set of domain-specific candidate tags
      2) a "text summary" derived from a GeoJSON file’s properties

    Then computes cosine similarity between the GeoJSON embedding and each tag embedding,
    returning the top-K most similar tags.
    """

    def __init__(self, model_name: str = "bert-base-uncased"):
        # 1) Load tokenizer + model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        # 2) Define a shortlist of candidate tags (you can expand this list)
        self.candidate_tags = [
            "roads",
            "buildings",
            "water",
            "vegetation",
            "boundaries",
            "transportation",
            "land_use",
            "elevation",
            "population_density",
            "points_of_interest",
        ]

        # 3) Pre-compute embeddings for each candidate tag
        self.tag_embeddings = self._compute_tag_embeddings(self.candidate_tags)

    def _compute_tag_embeddings(self, tags: list[str]) -> np.ndarray:
        """
        Given a list of short tag‐strings, return a NumPy array of shape (len(tags), hidden_size),
        where each row is the [CLS] token embedding for that tag.
        """
        embeddings: list[np.ndarray] = []

        for tag in tags:
            inputs = self.tokenizer(tag, return_tensors="pt", truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            # outputs.last_hidden_state: (batch_size=1, seq_len, hidden_size)
            # We take the [CLS] embedding: index 0 in seq_len
            cls_emb = outputs.last_hidden_state[:, 0, :].cpu().numpy()  # shape (1, hidden_size)
            embeddings.append(cls_emb)

        # Stack into shape (num_tags, hidden_size)
        return np.vstack(embeddings)

    def _geojson_to_text(self, geojson: dict) -> str:
        """
        For simplicity, build a raw text string by concatenating
        the keys and values of the first feature’s properties.
        You can expand this to loop over all features, combine geometry info, etc.
        """
        features = geojson.get("features", [])
        if not features:
            return ""

        # Grab the very first feature's properties (if it exists)
        props = features[0].get("properties", {})
        # Join "key value" pairs into one string
        tokens: list[str] = []
        for k, v in props.items():
            # Cast the value to string in case it's numeric, boolean, etc.
            tokens.append(f"{k} {v}")
        return " ".join(tokens)

    def suggest_tags(self, geojson: dict, top_k: int = 3) -> list[str]:
        """
        1) Convert geojson → single text string
        2) Tokenize & embed via BERT → a (1, hidden_size) array
        3) Compute cosine similarity (1 × num_tags) against pre-computed tag embeddings
        4) Return the top_k most similar candidate tags
        """
        # 1) Build a text summary from the GeoJSON
        text_summary = self._geojson_to_text(geojson)
        if text_summary.strip() == "":
            return []

        # 2) Tokenize + embed
        inputs = self.tokenizer(
            text_summary, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        # [CLS] embedding of the entire summary: shape (1, hidden_size)
        summary_emb = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        # 3) Cosine similarities → shape (1, num_tags)
        sims = cosine_similarity(summary_emb, self.tag_embeddings)[0]
        # 4) Get indices of top_k highest similarities
        top_indices = sims.argsort()[-top_k:][::-1]
        return [self.candidate_tags[i] for i in top_indices]


# For quick local testing:
if __name__ == "__main__":
    # Example: load a small GeoJSON snippet from disk (replace path as needed)
    example_path = "sample.geojson"
    try:
        with open(example_path, "r", encoding="utf-8") as fp:
            gj = json.load(fp)
    except FileNotFoundError:
        print(f"ERROR: Put a valid 'sample.geojson' (with at least one feature) in the same dir.")
        exit(1)

    suggester = TagSuggester()
    tags = suggester.suggest_tags(gj, top_k=5)
    print("Top 5 suggested tags:", tags)
