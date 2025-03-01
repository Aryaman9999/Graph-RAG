# Import required libraries
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import AzureOpenAIEmbeddings
from langchain.chains import RetrievalQA

# Load environment variables from .env file (for security)
load_dotenv()

# Neo4j Database Credentials (Use environment variables instead of hardcoding)
NEO4J_URL = os.getenv("NEO4J_URL", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Store securely

# Initialize the Neo4j Graph connection
graph = Neo4jGraph(
    url=NEO4J_URL, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD
)
print("✅ Connected to Neo4j Knowledge Graph!")

# Define Cypher query for creating an enriched Space Exploration Graph
space_exploration_query = """
CREATE
  (voyager1:Spacecraft {name: 'Voyager 1', launch_year: 1977, mission_type: 'Interstellar Probe', status: 'Operational', funding: 'NASA'}),
  (voyager2:Spacecraft {name: 'Voyager 2', launch_year: 1977, mission_type: 'Interstellar Probe', status: 'Operational', funding: 'NASA'}),
  (perseverance:Spacecraft {name: 'Perseverance', launch_year: 2020, mission_type: 'Mars Rover', status: 'Operational', funding: 'NASA'}),
  (apollo11:Spacecraft {name: 'Apollo 11', launch_year: 1969, mission_type: 'Lunar Lander', status: 'Completed', funding: 'NASA'}),
  (chandrayaan3:Spacecraft {name: 'Chandrayaan-3', launch_year: 2023, mission_type: 'Lunar Lander', status: 'Operational', funding: 'ISRO'}),
  (tianwen1:Spacecraft {name: 'Tianwen-1', launch_year: 2020, mission_type: 'Mars Orbiter & Rover', status: 'Operational', funding: 'CNSA'}),
  (hubble:Spacecraft {name: 'Hubble Space Telescope', launch_year: 1990, mission_type: 'Space Telescope', status: 'Operational', funding: 'NASA/ESA'}),
  (jwst:Spacecraft {name: 'James Webb Space Telescope', launch_year: 2021, mission_type: 'Infrared Space Telescope', status: 'Operational', funding: 'NASA/ESA/CSA'}),
  (artemis1:Spacecraft {name: 'Artemis I', launch_year: 2022, mission_type: 'Lunar Mission', status: 'Completed', funding: 'NASA'}),
  
  (nasa:Agency {name: 'NASA', country: 'USA'}),
  (isro:Agency {name: 'ISRO', country: 'India'}),
  (spacex:Agency {name: 'SpaceX', country: 'USA'}),
  (cnsa:Agency {name: 'CNSA', country: 'China'}),
  (esa:Agency {name: 'ESA', country: 'Europe'}),
  (roscosmos:Agency {name: 'Roscosmos', country: 'Russia'}),

  (mars:Planet {name: 'Mars'}),
  (moon:Moon {name: 'Moon'}),
  (earth:Planet {name: 'Earth'}),
  (jupiter:Planet {name: 'Jupiter'}),
  (saturn:Planet {name: 'Saturn'}),

  (voyager1)-[:LAUNCHED_BY]->(nasa),
  (voyager2)-[:LAUNCHED_BY]->(nasa),
  (perseverance)-[:LAUNCHED_BY]->(nasa),
  (apollo11)-[:LAUNCHED_BY]->(nasa),
  (chandrayaan3)-[:LAUNCHED_BY]->(isro),
  (tianwen1)-[:LAUNCHED_BY]->(cnsa),
  (hubble)-[:LAUNCHED_BY]->(nasa),
  (jwst)-[:LAUNCHED_BY]->(nasa),
  (artemis1)-[:LAUNCHED_BY]->(nasa),

  (voyager1)-[:EXPLORED]->(jupiter),
  (voyager1)-[:EXPLORED]->(saturn),
  (voyager2)-[:EXPLORED]->(jupiter),
  (voyager2)-[:EXPLORED]->(saturn),
  (perseverance)-[:LANDED_ON]->(mars),
  (apollo11)-[:LANDED_ON]->(moon),
  (chandrayaan3)-[:LANDED_ON]->(moon),
  (tianwen1)-[:ORBITED]->(mars),
  (hubble)-[:ORBITED]->(earth),
  (jwst)-[:ORBITED]->(earth)
"""

# Run the query in Neo4j to create nodes and relationships
graph.query(space_exploration_query)
print("🚀 Space Exploration Knowledge Graph Created!")

# Initialize Neo4j Vector Store for Retrieval-Augmented Generation (RAG)
vector_index = Neo4jVector.from_existing_graph(
    AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("CHAT_GPT_KEY"),
        api_version="",
        azure_deployment="text-embedding-ada"
    ),
    url=NEO4J_URL,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name='space_missions',
    node_label=["Spacecraft", "Agency", "Planet", "Mission"],
    text_node_properties=['name', 'mission_type', 'status', 'funding'],
    embedding_node_property='embedding',
)

# Initialize Azure OpenAI LLM for answering queries
llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    model="gpt-4o",
    azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    openai_api_version=",
    openai_api_key=os.getenv("CHAT_GPT_KEY2"),
    temperature=0.1,
    request_timeout=30
)

# Create RetrievalQA pipeline using Neo4j Vector search
vector_qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 5})
)

# Example query
query = "Which spacecraft explored Mars? Provide details including launch year and mission type."
response = vector_qa.invoke(query)

# Print Query and Response
print("❓ Query:", query)
print("🤖 Response:", response)
