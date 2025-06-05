# MetaGuessr
_Reimagining Geospatial Metadata — with Intelligence_

## Overview

**MetaGuessr** is a collaborative reimplementation of the original [likeon/geometa](https://github.com/likeon/geometa) project, developed by a team of computing science students aiming to enhance metadata extraction from geospatial datasets.  

We worked alongside a talented team to rebuild the existing GeoMeta tool from the ground up—but with a twist: **we integrated machine learning–based tag recommendations** using pre-trained language models and domain-specific heuristics. This allows users to automatically receive relevant metadata suggestions for files lacking proper annotations.

## 🔀 What’s the Twist?

While the original project focused solely on extracting metadata from geospatial files using standard techniques (like reading headers, embedded metadata, and schema fields), **MetaGuessr adds an intelligent metadata inference layer** that:

- Uses **BERT embeddings** to analyze file content and suggest relevant tags.  
- Applies **NLP techniques** to generate descriptive summaries for shapefiles and GeoJSONs.  
- Offers **a web-based interface** where users can preview inferred tags and customize them before export.

## ✨ Key Features

- 🧠 **AI-Powered Metadata Suggestions**  
  Auto-generate metadata using contextual embeddings and natural language inference.
- 🗺️ **Support for Multiple Geospatial Formats**  
  Including `.geojson`, `.shp`, `.kml`, and `.gml`.
- 🔍 **Metadata Validator**  
  Warns users when required metadata fields are missing or inconsistent.
- 🧑‍💻 **Team Collaboration**  
  Built by a team passionate about GIS and AI to improve open-data usability.

## 🖥️ Web Interface

The frontend is built with React + Leaflet.js, letting users:

- Upload a geospatial file (GeoJSON, Shapefile, etc.).  
- View basic attribute tables and geometry previews on an interactive map.  
- See **AI-generated tag recommendations** in a sidebar.  
- Edit or approve tags before exporting a standardized metadata package.

## ⚙️ Architecture & Technologies

- **Backend**:  
  - Python 3.11  
  - FastAPI  
  - PyShp, Fiona, GeoPandas (for I/O and geometric processing)  
  - HuggingFace Transformers (`bert-base-uncased`) for embedding-based inference  

- **Frontend**:  
  - React 18  
  - Leaflet.js (for map rendering)  
  - Tailwind CSS (for styling)  
  - Axios (for API calls)  

📌 Limitations
Requires Internet & Paid API Access

The Street View preview (to show a sample “real-world” location for a given geometry) relies on the Google Street View API. Since that API is paid, MetaGuessr will not function fully on a private or offline machine.

Geoguessr Map Embedding

Some demo modes in MetaGuessr attempt to embed a sample map using Geoguessr’s visuals. Unfortunately, Geoguessr has not authorized us to redistribute or embed their proprietary map layers. As a result, upon cloning this repo and running locally, the “Geoguessr Demo” section will simply show a placeholder stating “Map preview unavailable—license required.”

You can remove or abstract out any Geoguessr-specific code if you plan to deploy entirely in a private environment.

Machine-Learning Model Download

The first run may be slow because the BERT model is pulled from HuggingFace. We recommend pre-caching bert-base-uncased (or a fine-tuned checkpoint) before conducting large-scale batch inference.

🙏 Acknowledgments & Shoutout
A special shoutout to the original author likeon for creating the foundational GeoMeta project. Without their work, this reimagination would not have been possible.

Thanks also to the entire open-source GIS and AI communities whose libraries and contributions made GeoMeta+ feasible.