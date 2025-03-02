from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Database Credentials (Replace with secure credentials)
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # Use environment variable for security

# Initialize the Neo4j Graph connection
graph = Neo4jGraph(
    url=NEO4J_URL, 
    username=NEO4J_USERNAME, 
    password=NEO4J_PASSWORD
)
print("✅ Connected to Neo4j Knowledge Graph!")

# Define Cypher query for Space Exploration Missions
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

  (perseverance)-[:EXPLORED]->(mars),
  (perseverance)-[:LANDED_ON]->(mars),  // Kept for historical accuracy
  (tianwen1)-[:EXPLORED]->(mars),
  (tianwen1)-[:ORBITED]->(mars),

  (apollo11)-[:LANDED_ON]->(moon),
  (chandrayaan3)-[:LANDED_ON]->(moon),
  
  (hubble)-[:ORBITED]->(earth),
  (jwst)-[:ORBITED]->(earth)

"""

# Run the query in Neo4j
graph.query(space_exploration_query)
print("🚀 Space Exploration Knowledge Graph Created!")

