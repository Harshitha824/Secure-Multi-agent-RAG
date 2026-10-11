import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def test_connection():
    if not URI or not USERNAME or not PASSWORD:
        raise ValueError(
            "Neo4j credentials are missing from the .env file."
        )

    try:
        with GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        ) as driver:

            driver.verify_connectivity()
            print("Neo4j connection successful!")

            with driver.session() as session:
                result = session.run("RETURN 1 AS test")
                print("Database test:", result.single()["test"])

    except Exception as error:
        print("Neo4j connection failed.")
        print("Error type:", type(error).__name__)
        print("Error details:", error)


if __name__ == "__main__":
    test_connection()