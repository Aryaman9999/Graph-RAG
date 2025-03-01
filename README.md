# 🚀 Space Exploration Knowledge Graph using Neo4j + Azure OpenAI

This project builds a **Space Exploration Knowledge Graph** using **Neo4j** and integrates it with **Azure OpenAI** for **Retrieval-Augmented Generation (RAG)**. The system allows querying a **Neo4j knowledge base** using **vector embeddings** and **LLM-powered responses**.

## 📌 Features
- **Graph-based knowledge representation** of spacecraft, agencies, and planets.
- **Neo4j Vector Search** for efficient retrieval.
- **Azure OpenAI LLM** for answering natural language queries.
- **Integration of multiple space missions with rich metadata.**

---

# 📦 Setup Instructions

## 1️⃣ Install Neo4j Desktop
### **For Windows, Mac, and Linux:**
1. **Download Neo4j Desktop** from [Neo4j Download](https://neo4j.com/download/)
2. **Install Neo4j Desktop** and create a new local database.
3. **Set up authentication:**
   - Default credentials:
     - **Username:** `neo4j`
     - **Password:** `neo4j` (Change it after the first login)

4. **Install Neo4j Plugins:**
   - Open **Neo4j Desktop** → Select **Manage** for your database → Click **Plugins**
   - Install:
     - **APOC** (for advanced Cypher queries)
     - **Graph Data Science (GDS)** (for vector search capabilities)

5. **Start the Neo4j Database.**

---

## 2️⃣ Install Python Dependencies
### **Pre-requisites:**
- **Python 3.8+** installed
- **pip** and **virtual environment**

```sh
# Create a virtual environment
python -m venv neo4j_env
source neo4j_env/bin/activate  # On Windows: neo4j_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt` should contain:**
```txt
langchain
neo4j
python-dotenv
openai
langchain-openai
langchain-neo4j
langchain-community
```

---

## 3️⃣ Configure Environment Variables
Create a `.env` file in the project root and add your credentials:

```ini
NEO4J_URL=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password
AZURE_OPENAI_ENDPOINT=https://your-openai-instance.openai.azure.com/
CHAT_GPT_KEY=your_openai_api_key
CHAT_GPT_KEY2=your_openai_api_key_2
```

---

## 4️⃣ Run the Knowledge Graph Script

```sh
python space_knowledge_graph.py
```

---

# 🛠️ How It Works

1. **Connects to Neo4j** using authentication.
2. **Creates a Space Exploration Graph** with spacecraft, agencies, and missions.
3. **Indexes the knowledge base** using Neo4j Vector Search.
4. **Queries the LLM** for intelligent retrieval.

### Example Query:
```python
query = "Which spacecraft explored Mars? Provide details including launch year and mission type."
response = vector_qa.invoke(query)
print(response)
```

### Example Output:
```json
{
  "Voyager 1": {"launch_year": 1977, "mission_type": "Interstellar Probe"},
  "Perseverance": {"launch_year": 2020, "mission_type": "Mars Rover"}
}
```

---

# 🎯 Next Steps
- **Deploy as an API** (FastAPI, Flask, or Streamlit for UI)
- **Enhance Graph Schema** (add more relationships & metadata)
- **Fine-tune the vector search** with optimized embeddings

---

💡 *Now you have a powerful RAG pipeline with Neo4j & Azure OpenAI!* 🚀


