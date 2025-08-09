# NLP-research

## Description
This project implements **Retrieval Augumented Generation**, designed to be an experiment to see the different answers generated based on different changes that include various **Chunking** and **Vector Search**. It is built in **Python** and uses external libraries like **uvicorn** and **FastAPI** for api managment.

The system is designed with the following goals in mind:
- Different searching options: similarity_search, hybrid_search
- Different chunking strategies: fixed, semantic or structure_based
- LLM 

---

## Folder Structure

```bash
.
├── Design-Document.txt
├── main.py
├── src/
│   |-- api/
│       ├── endpoints/
│       ├── models/
|   |-- config/
│       ├── settings/
|   |-- research/
│       ├── chunking_strategies/
│       ├── default_retrieval/
|   |-- services/
│       ├── data_utils/
│       ├── document_service/
│       ├── vector_store/
│       └── embedding_service/
|   |-- utils/
│       ├── generate_request_id/
│       ├── generate_response_llm/
│       └── logger_config/
└── README.md
```

---
### Building the Project

1. Clone the repository:
2. Get into the source directory:

   ```bash
   cd src
   ```

3. Run pip install to configure the dependancies for the projects:

   ```bash
    pip install -r requirements.txt
   ```

4. Build the project:

   ```bash
    uvicorn main:app --reload
   ```


When needing to deploy this project
https://medium.com/aspiring-data-scientist/deploy-a-fastapi-app-on-aws-ecs-034b8b7b5ac2

