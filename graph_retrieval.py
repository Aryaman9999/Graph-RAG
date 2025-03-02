from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI
from neo4j import GraphDatabase
from rich import print
from rich.table import Table

# Load environment variables
load_dotenv()

# Neo4j Database Credentials
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Securely load password

# Initialize Neo4j connection
neo4j_driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

# Function to extract schema from Neo4j
def extract_schema():
    node_query = """
        CALL db.schema.nodeTypeProperties()
        YIELD nodeType, propertyName
        RETURN nodeType AS label, collect(propertyName) AS properties
    """
    rel_query = """
        MATCH (a)-[r]->(b)
        RETURN DISTINCT labels(a)[0] AS start, type(r) AS type, labels(b)[0] AS end
    """

    with neo4j_driver.session() as session:
        node_result = session.run(node_query)
        nodes = [record.data() for record in node_result]

        rel_result = session.run(rel_query)
        relationships = [record.data() for record in rel_result]

    # Formatting schema
    formatted_schema = "### Nodes and Properties:\n"
    for node in nodes:
        formatted_schema += f"- (: {node['label']}) → Properties: {node['properties']}\n"

    formatted_schema += "\n### Relationships:\n"
    for rel in relationships:
        formatted_schema += f"- (: {rel['start']}) -[:{rel['type']}]-> (: {rel['end']})\n"

    return formatted_schema.strip()


# Extract schema from Neo4j
graph_schema = extract_schema()

# Initialize Azure OpenAI LLM
llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    model="gpt-4o",
    azure_endpoint="",
    openai_api_version="",
    openai_api_key=os.getenv('CHAT_GPT_KEY'),
)

# Define expected output schema
response_schemas = [ResponseSchema(name="cypher_query", description="The Cypher query to execute.")]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

cypher_prompt = PromptTemplate(
    template="""You are an expert in Neo4j Cypher queries. 
    Generate a Cypher query based on the given **Graph Schema** while ensuring correct relationships.

    ### **Graph Schema**:
    {schema}

    ### **Rules**:
    - `[:LAUNCHED_BY]` exists **between (Spacecraft) and (Agency) only**.
    - `[:EXPLORED]`, `[:LANDED_ON]`, and `[:ORBITED]` exist **between (Spacecraft) and (Planet)**.
    - A `Planet` is **not directly connected** to an `Agency`.

    ### **Examples**:
    **Q:** "Which spacecraft explored Mars? Provide details including launch year and mission type."
    **A:** 
    ```cypher
    MATCH (s:Spacecraft)-[:EXPLORED]->(p:Planet {{name: "Mars"}}) 
    RETURN s.name, s.launch_year, s.mission_type
    ```

    **Q:** "Which agency launched Voyager 1?"
    **A:** 
    ```cypher
    MATCH (s:Spacecraft {{name: "Voyager 1"}})-[:LAUNCHED_BY]->(a:Agency) 
    RETURN a.name
    ```

    **Q:** "Which spacecraft was sent to Mars and by whom?"
    **A:** 
    ```cypher
    MATCH (s:Spacecraft)-[:EXPLORED]->(p:Planet {{name: "Mars"}}) 
    MATCH (s)-[:LAUNCHED_BY]->(a:Agency) 
    RETURN s.name AS spacecraft_name, a.name AS agency_name
    ```

    ### **User Query**:
    {question}

    {format_instructions}
    """,
    input_variables=["schema", "question"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
)


# RunnableSequence for Cypher query generation
cypher_chain = (
    cypher_prompt 
    | llm 
    | output_parser
)

# User question
user_question = "Which spacecraft did isro launch and to where and when?"

# Generate Cypher query
cypher_result = cypher_chain.invoke({"schema": graph_schema, "question": user_question})

# Extract Cypher query
cypher_query = cypher_result["cypher_query"]

# Function to run Cypher query
def run_cypher_query(query):
    with neo4j_driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Run the generated query
results = run_cypher_query(cypher_query)

# Summarization prompt
final_prompt = PromptTemplate(
    template="""
    ### User Question:
    {user_question}      
    Generated the following Cypher query:
    
    ```
    {cypher_query}
    ```
    The result being:
    {results}
    
    \n \n Based only on the generated result information, answer the user question concisely.
    """,
    input_variables=["user_question", "cypher_query", "results"]
)

# RunnableSequence for final summarization
summary_chain = (
    final_prompt 
    | llm
)

# Get final summary
final_summary = summary_chain.invoke({
    "user_question": user_question,
    "cypher_query": cypher_query,
    "results": results
})

# Print formatted output
print("[bold yellow]User Query:[/bold yellow]\n[yellow]{}[/yellow]".format(user_question))
print("[bold cyan]Generated Cypher:[/bold cyan]\n[cyan]{}[/cyan]".format(cypher_query))

# Display results in a Rich table
table = Table(title="Query Results", show_header=True, header_style="bold green")
table.add_column("Spacecraft", style="green", justify="left")
table.add_column("Launch Year", style="yellow", justify="center")
table.add_column("Mission Type", style="blue", justify="left")
for result in results:
    spacecraft = result.get("spacecraft", "N/A")  # Using "spacecraft" from RETURN statement
    agency = result.get("agency", "N/A")
    landed_on = result.get("landed_on_planet") or result.get("landed_on_moon") or "Unknown"

    table.add_row(spacecraft, agency, landed_on)
for result in results:
    print("Query result:", result) 


# Print final answer
print("[bold magenta]Final Answer:[/bold magenta]\n" + final_summary.content)
