# Vector Database Performance Comparison Project

## Project Description

This project is a tool for benchmarking the performance of vector databases, specifically HNSWlib and ChromaDB. It allows users to compare these databases based on key metrics:

* **Query Time**: Measures the speed of similarity searches.
* **Memory Usage**: Tracks the amount of system memory consumed.
* **Index Size**: Indicates the storage space required for the database index.

The project aims to provide insights into the efficiency and scalability of these vector databases, which are crucial for various applications like:

* Recommendation systems
* Semantic search
* Image and audio retrieval
* Large Language Model (LLM) applications

##  Key Features

* **Performance Evaluation**: Compares HNSWlib and ChromaDB across query time, memory usage, and index size.
* **Configurable Testing**:  The script allows you to configure the number of queries and the number of nearest neighbors (k).
* **Data Loading**:  The project loads vector embeddings from a JSON file (`embeddings.json`).
* **HNSWlib Integration**:  Uses HNSWlib for efficient approximate nearest neighbor (ANN) search.
* **ChromaDB Integration**:  Incorporates ChromaDB, a vector database designed for AI applications.
* **Reporting**:  Prints a summary of the performance metrics for both databases.

##  Target Audience

This project is useful for:

* Developers working with vector databases.
* Researchers evaluating vector search performance.
* Anyone interested in understanding the trade-offs between different vector database solutions.

##  Local Setup

1.  **Prerequisites**

    * **Python 3.6 or higher**:  Download from [python.org](https://www.python.org/downloads/).
    * **pip**:  Python's package installer (usually included with Python).
    * **Git**:  For cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads).

2.  **Installation**

    * **Clone the repository:**

        ```bash
        git clone <your_repository_url>
        cd Vector-Databases
        ```

    * **Create a virtual environment (recommended):**

        ```bash
        python3 -m venv venv
        source venv/bin/activate  # Linux/macOS
        venv\Scripts\activate  # Windows
        ```

    * **Install dependencies:**

        ```bash
        pip install -r requirements.txt
        ```
        (or  `pip install hnswlib psutil chromadb`)

    * **Prepare the data:**

        * Place your vector embeddings data in a file named `embeddings.json` in the project's root directory.  The file should contain a JSON list of dictionaries, where each dictionary has an `"embedding"` key and an `"id"` key.
        * Example `embeddings.json` structure:
            ```json
            [
              {"id": "0", "embedding": [0.1, 0.2, 0.3, ...]},
              {"id": "1", "embedding": [0.4, 0.5, 0.6, ...]},
              ...
            ]
            ```

    * **Run the performance test:**
        ```bash
        python performance.py
        ```

##  Contributions

Contributions are welcome!  Feel free to submit pull requests to improve the project.
