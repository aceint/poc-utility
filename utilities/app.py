import time
import json
import numpy as np
import hnswlib
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel, Field
from typing import Annotated
from contextlib import asynccontextmanager
import os  # Import the os module

# --- Configuration ---
HNSWLIB_INDEX_PATH = 'hnswlib_index.bin'
EMBEDDING_DIM = 768
DATA_FILE = "embeddings.json"

# --- Globals ---
hnsw_index: Optional[hnswlib.Index] = None
vector_data: List[Dict] = []

# --- Data Models ---
class Item(BaseModel):
    id: str = Field(..., description="Unique identifier for the item")
    vector: List[float] = Field(..., description="The embedding vector")
    data: Optional[Optional[dict]] = Field(None, description="Additional data associated with the vector")


class QueryRequest(BaseModel):
    vector: List[float] = Field(..., description="The query vector")
    k: int = Field(..., description="The number of nearest neighbors to retrieve (must be > 0)", gt=0)
    include_data: bool = Field(False, description="Whether to include associated data in the response")


class QueryResult(BaseModel):
    id: str = Field(..., description="ID of the retrieved item")
    vector: List[float] = Field(..., description="The vector of the retrieved item")
    distance: float = Field(..., description="The distance between the query vector and the retrieved item's vector")
    data: Optional[dict] = Field(None, description="Associated data of the retrieved item (if include_data was true)")


class QueryResponse(BaseModel):
    results: List[QueryResult] = Field(..., description="List of query results")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


# --- Helper Functions ---
def load_data(filename: str = DATA_FILE) -> List[Dict]:
    """Loads data from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:  # Specify encoding
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Data file '{filename}' not found. Returning empty data.")
        return []



def create_hnsw_index(embeddings: List[List[float]], dim: int) -> hnswlib.Index:
    """Creates and initializes the HNSWlib index."""
    p = hnswlib.Index(space='l2', dim=dim)
    p.init_index(max_elements=len(embeddings), ef_construction=200, M=16)
    p.add_items(np.array(embeddings), list(range(len(embeddings))))
    return p



def load_hnsw_index(index_path: str, dim: int) -> hnswlib.Index:
    """Loads the HNSWlib index from a file or creates a new one."""
    p = hnswlib.Index(space='l2', dim=dim)
    try:
        p.load_index(index_path)
        print("Loaded hnsw index")
        return p
    except RuntimeError:
        print("HNSWlib index file not found. Creating a new index.")
        return p



def save_hnsw_index(index: hnswlib.Index, index_path: str) -> None:
    """Saves the HNSWlib index to a file."""
    index.save_index(index_path)



# --- FastAPI App ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI to initialize HNSWlib index and load data.
    """
    global hnsw_index, vector_data
    vector_data = load_data()
    hnsw_index = load_hnsw_index(HNSWLIB_INDEX_PATH, EMBEDDING_DIM)
    if not hnsw_index.get_current_count() and vector_data:
        embeddings = [item['vector'] for item in vector_data]
        hnsw_index = create_hnsw_index(embeddings=embeddings, dim=EMBEDDING_DIM)
        save_hnsw_index(hnsw_index, HNSWLIB_INDEX_PATH)
    yield



app = FastAPI(
    title="Vector Database API",
    description="API for performing similarity search with HNSWlib.",
    version="1.0.0",
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    lifespan=lifespan,
)



@app.post(
    "/items",
    response_model=dict,
    status_code=201,
    summary="Add items to the database.",
    responses={201: {"description": "Items added successfully."}},
)
async def post_items(
    items: Annotated[List[Item], Body(..., description="List of items to add")],
) -> dict:
    """
    Adds items to the database (HNSWlib and in-memory).
    """
    global hnsw_index, vector_data
    new_embeddings = [item.vector for item in items]
    new_ids = [item.id for item in items]
    vector_data.extend([item.dict() for item in items])

    if not hnsw_index:
        hnsw_index = create_hnsw_index(embeddings=new_embeddings, dim=EMBEDDING_DIM)
    else:
        max_elements = hnsw_index.get_max_elements()
        current_count = hnsw_index.get_current_count()
        if current_count + len(new_embeddings) > max_elements:
            raise HTTPException(
                status_code=400,
                detail=f"Adding these vectors exceeds max_elements ({max_elements}).",
            )
        hnsw_index.add_items(np.array(new_embeddings), new_ids)
    save_hnsw_index(hnsw_index, HNSWLIB_INDEX_PATH)
    return {"status": "OK"}



@app.post(
    "/query",
    response_model=QueryResponse,
    summary="Query for nearest neighbors.",
)
async def post_query(
    body: Annotated[QueryRequest, Body(..., description="Query parameters")],
) -> QueryResponse:
    """
    Queries the database for nearest neighbors.
    """
    global hnsw_index, vector_data

    if not hnsw_index:
        raise HTTPException(status_code=500, detail="HNSWlib index not initialized.")

    query_vector = np.array(body.vector)
    k = body.k
    include_data = body.include_data

    labels, distances = hnsw_index.knn_query(query_vector, k=k)
    results = []
    for i, label in enumerate(labels[0]):
        item_id = hnsw_index.get_ids_list()[label]
        item_data = next((item for item in vector_data if item['id'] == item_id), None)
        if item_data:
            result = {
                "id": item_id,
                "vector": item_data['vector'],
                "distance": distances[0][i],
            }
            if include_data:
                result["data"] = item_data.get('data', None)
            results.append(result)
        else:
            print(f"Warning: Item with label {label} and id {item_id} not found.")
    return QueryResponse(results=results)



@app.get(
    "/items/{id}",
    response_model=Item,
    summary="Retrieve an item by its ID.",
    responses={404: {"description": "Item not found."}},
)
async def get_item_by_id(
    id: Annotated[str, Path(..., description="The ID of the item to retrieve")],
) -> Item:
    """
    Retrieves a specific item by its ID.
    """
    global vector_data
    item = next((item for item in vector_data if item['id'] == id), None)
    if item:
        return Item(**item)
    else:
        raise HTTPException(status_code=404, detail="Item not found.")



@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the Vector Database API. See /docs for API documentation."}


if __name__ == "__main__":
    import uvicorn

    uvicorn_config = {
        "app": "app:app",  # The app variable in your main.py
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,  # Enable auto-reloading for development
    }

    # Check if running on Windows
    if os.name == 'nt':
        uvicorn_config["loop"] = "asyncio"  # Use asyncio on Windows
    else:
        uvicorn_config["loop"] = "uvloop" #Use uvloop on other systems

    uvicorn.run(**uvicorn_config)
