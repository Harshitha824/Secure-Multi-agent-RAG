
import json
from pathlib import Path

import networkx as nx


class LocalKnowledgeGraph:
    def __init__(self, storage_path="data/knowledge_graph.json"):
        self.graph = nx.MultiDiGraph()
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.load()

    def add_entity(self, entity_id, name, entity_type="Entity"):
        self.graph.add_node(
            entity_id,
            name=name,
            entity_type=entity_type,
        )

    def add_relationship(self, source_id, target_id, relation):
        if source_id not in self.graph or target_id not in self.graph:
            raise ValueError("Both entities must exist before adding a relationship.")

        self.graph.add_edge(
            source_id,
            target_id,
            relation=relation,
        )

    def get_relationships(self, entity_id):
        if entity_id not in self.graph:
            return []

        relationships = []

        for _, target, data in self.graph.out_edges(entity_id, data=True):
            relationships.append({
                "source": self.graph.nodes[entity_id].get("name", entity_id),
                "relationship": data.get("relation", "RELATED_TO"),
                "target": self.graph.nodes[target].get("name", target),
            })

        for source, _, data in self.graph.in_edges(entity_id, data=True):
            relationships.append({
                "source": self.graph.nodes[source].get("name", source),
                "relationship": data.get("relation", "RELATED_TO"),
                "target": self.graph.nodes[entity_id].get("name", entity_id),
            })

        return relationships

    def save(self):
        data = nx.node_link_data(self.graph)
        self.storage_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self):
        if not self.storage_path.exists():
            return

        try:
            data = json.loads(
                self.storage_path.read_text(encoding="utf-8")
            )
            self.graph = nx.node_link_graph(data)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Could not load knowledge graph from {self.storage_path}"
            ) from exc


if __name__ == "__main__":
    kg = LocalKnowledgeGraph()

    kg.add_entity("python", "Python", "Programming Language")
    kg.add_entity("networkx", "NetworkX", "Python Library")
    kg.add_relationship("networkx", "python", "WRITTEN_IN")

    kg.save()

    print("Local knowledge graph test successful!")
    print("Entities:", kg.graph.number_of_nodes())
    print("Relationships:", kg.graph.number_of_edges())
    print("Python relationships:", kg.get_relationships("python"))
