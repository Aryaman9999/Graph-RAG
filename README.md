# 🚀 Knowledge Graph Based RAG Demonstration

## Overview
This project creates and queries a **Knowledge Graph** for space exploration missions using **Neo4j** and **LangChain**. The graph represents spacecraft, space agencies, planets, and their relationships, allowing users to ask natural language questions and retrieve insights using **Azure OpenAI (GPT-4o)**.

## Features
- **Graph Building:** Automatically constructs a Neo4j Knowledge Graph with spacecraft, agencies, planets, and their relationships.
- **Graph Retrieval:** Uses **Azure OpenAI** to generate **Cypher queries** dynamically based on user questions.
- **Schema Extraction:** Extracts the graph schema dynamically from Neo4j.
- **Query Execution:** Runs generated Cypher queries on Neo4j and formats results in a readable format.
- **Rich Output:** Displays results using **Rich tables** for better visualization.

## Setup & Installation
### Prerequisites
Ensure you have the following installed:
- **Python 3.9+ **
- **Neo4j (Community or Enterprise Edition)**
- **Docker (optional for Neo4j setup)**
- **Azure OpenAI API Access**

### Clone the Repository
```sh
git clone https://github.com/Aryaman9999/Graph-RAG/
cd /Graph-RAG
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the project root with the following:
```env
NEO4J_URL=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<your-neo4j-password>
CHAT_GPT_KEY=<your-azure-openai-key>
AZURE_ENDPOINT=<your-azure-openai-endpoint>
OPENAI_API_VERSION=<your-api-version>
```

## Running the Project
## Step 1: Set Up Neo4j Desktop

1. **Install Neo4j Desktop**  
   - Download and install **[Neo4j Desktop](https://neo4j.com/download/)**.
   - Open Neo4j Desktop and create a **new database project**.
   - Start a **local Neo4j database** (default Bolt URL: `bolt://localhost:7687`).

2. **Set Up Database Credentials**  
   - Go to the **database settings** in Neo4j Desktop.
   - Note the **username (default: neo4j)** and set a **secure password**.
   - Update the `.env` file with these credentials:
     ```env
     NEO4J_URL=bolt://localhost:7687
     NEO4J_USERNAME=neo4j
     NEO4J_PASSWORD=your_password_here
     ```

3. **Enable APOC & Full-Text Indexing (Optional, for advanced queries)**  
   - In **Neo4j Desktop**, open the `neo4j.conf` file and add:
     ```
     dbms.security.procedures.unrestricted=apoc.*
     dbms.security.procedures.allowlist=apoc.*
     dbms.index.fulltext.enabled=true
     ```
   - Restart the database for changes to take effect.

If running Neo4j locally, start the Neo4j database and ensure it is accessible.

### Step 2: Build the Knowledge Graph
Run the following command to construct the Knowledge Graph in Neo4j:
```sh
python graph_builder.py
```
This script will:
- Establish a connection to Neo4j
- Create nodes and relationships for spacecraft, space agencies, and planets
- Populate the database with relevant space exploration data

### Step 3: Query the Knowledge Graph
Use the retrieval script to ask natural language questions:
```sh
python graph_retrieval.py
```
This script will:
- Extract the current **graph schema**
- Generate **Cypher queries** using **Azure OpenAI**
- Execute queries and display results in a structured format

## Example Query
**Input:**
```sh
Which spacecraft did ISRO launch, to where, and when?
```
**Generated Cypher Query:**
```cypher
MATCH (s:Spacecraft)-[:LAUNCHED_BY]->(a:Agency {name: "ISRO"})
MATCH (s)-[:EXPLORED|:LANDED_ON|:ORBITED]->(p)
RETURN s.name AS spacecraft, s.launch_year AS launch_year, p.name AS destination
```
**Output:**
| Spacecraft     | Launch Year | Destination |
|---------------|------------|-------------|
| Chandrayaan-3 | 2023       | Moon        |

## Code Structure
```
📂 project-root
 ├── graph_builder.py       # Builds the Neo4j Knowledge Graph
 ├── graph_retrieval.py     # Generates and executes Cypher queries
 ├── requirements.txt       # Required Python packages
 ├── .env                   # Environment variables (excluded in .gitignore)
 ├── README.md              # Project documentation
```

## Dependencies
The project relies on the following Python libraries:
```sh
pip install langchain langchain_openai neo4j python-dotenv rich
```

## Future Enhancements
- ✅ Expand the graph with more detailed space exploration data.
- ✅ Support multiple LLMs for query generation.
- ✅ Add a Streamlit web UI for interactive query execution.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests.

## License
This project is licensed under the **MIT License**.

---
🚀 **Happy Space Exploration!** 🌌

