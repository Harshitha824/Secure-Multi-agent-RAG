
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


class Neo4jKnowledgeGraph:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        if not all([uri, username, password]):
            raise ValueError(
                "NEO4J_URI, NEO4J_USERNAME, and "
                "NEO4J_PASSWORD must be set in .env"
            )

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password),
        )
        self.driver.verify_connectivity()

    def add_entity(self, entity_id, name, entity_type="Entity"):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (e:Entity {entity_id: $entity_id})
                SET e.name = $name,
                    e.entity_type = $entity_type
                """,
                entity_id=entity_id,
                name=name,
                entity_type=entity_type,
            ).consume()

    def add_relationship(self, source_id, target_id, relation):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (source:Entity {entity_id: $source_id})
                MATCH (target:Entity {entity_id: $target_id})
                MERGE (source)-[r:RELATED_TO {relation: $relation}]->(target)
                RETURN count(r) AS created
                """,
                source_id=source_id,
                target_id=target_id,
                relation=relation,
            ).single()

            if result is None or result["created"] == 0:
                raise ValueError(
                    "Both entities must exist before adding a relationship."
                )

    def get_relationships(self, entity_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (e:Entity {entity_id: $entity_id})
                      -[r:RELATED_TO]-(other:Entity)
                RETURN startNode(r).name AS source,
                       r.relation AS relationship,
                       endNode(r).name AS target
                """,
                entity_id=entity_id,
            )

            return [record.data() for record in result]

    
    def search_relationships(self, question, limit=10):
        """Find graph relationships relevant to a question."""

        stop_words = {
            "what", "which", "where", "when", "who", "how",
            "does", "did", "the", "and", "for", "from",
            "with", "about", "into", "are", "was", "is",
            "can", "could", "explain", "tell", "me", "in"
        }

        terms = [
            word.lower().strip(".,?!:;()[]{}\"'")
            for word in question.split()
        ]
        terms = list(dict.fromkeys(
            word for word in terms
            if len(word) > 2 and word not in stop_words
        ))

        if not terms:
            return []

        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (source:Entity)-[r:RELATED_TO]->(target:Entity)
                WITH source, r, target,
                     toLower(
                         coalesce(source.name, '') + ' ' +
                         coalesce(source.entity_type, '') + ' ' +
                         coalesce(r.relation, '') + ' ' +
                         coalesce(target.name, '') + ' ' +
                         coalesce(target.entity_type, '')
                     ) AS searchable_text
                WHERE any(term IN $terms
                          WHERE searchable_text CONTAINS term)
                RETURN source.name AS source,
                       r.relation AS relationship,
                       target.name AS target
                LIMIT $limit
                """,
                terms=terms,
                limit=limit,
            )

            return [record.data() for record in result]

    
    def add_knowledge(self, data: dict):
        """Store extracted entities and relationships in Neo4j."""

        entities = data.get("entities", [])
        relationships = data.get("relationships", [])

        # Map entity names to stable IDs.
        entity_ids = {}

        for entity in entities:
            name = entity.get("name", "").strip()
            entity_type = entity.get("type", "Entity")

            if not name:
                continue

            entity_id = name.lower()

            self.add_entity(
                entity_id=entity_id,
                name=name,
                entity_type=entity_type
            )

            entity_ids[name.lower()] = entity_id

        # Store relationships only when both entities exist.
        for relationship in relationships:
            source = relationship.get("source", "").strip()
            target = relationship.get("target", "").strip()
            relation = relationship.get("relation", "").strip()

            if (
                source.lower() in entity_ids
                and target.lower() in entity_ids
                and relation
            ):
                self.add_relationship(
                    entity_ids[source.lower()],
                    entity_ids[target.lower()],
                    relation
                )


    def close(self):
        self.driver.close()


if __name__ == "__main__":
    kg = Neo4jKnowledgeGraph()

    try:
        kg.add_entity("python", "Python", "Programming Language")
        kg.add_entity("networkx", "NetworkX", "Python Library")
        kg.add_relationship("networkx", "python", "WRITTEN_IN")

        print("Neo4j knowledge graph test successful!")
        print("Python relationships:", kg.get_relationships("python"))
        print(
            "Search results:",
            kg.search_relationships("How is NetworkX related to Python?")
)
    finally:
        kg.close()
