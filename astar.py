import heapq
from typing import Dict, List, Tuple, Optional
from graph_data import CUENCA_NODES, GRAPH_EDGES, haversine_distance, euclidean_distance

class AStarPathFinder:
    def __init__(self, nodes: Dict, edges: Dict):
        self.nodes = nodes
        self.edges = edges
        self.explored: List[str] = []
        self.frontier: List[Tuple[float, int, str, List[str], float]] = []

    def heuristic(self, node: str, goal: str) -> float:
        n, g = self.nodes[node], self.nodes[goal]
        return euclidean_distance(n["lat"], n["lon"], g["lat"], g["lon"])

    def get_distance(self, node1: str, node2: str) -> float:
        n1, n2 = self.nodes[node1], self.nodes[node2]
        return haversine_distance(n1["lat"], n1["lon"], n2["lat"], n2["lon"])

    def find_path(self, start: str, goal: str) -> Tuple[Optional[List[str]], float, int]:
        self.explored = []
        self.frontier = []
        counter = 0
        heapq.heappush(self.frontier, (0.0, counter, start, [start], 0.0))
        visited = set()

        while self.frontier:
            f_score, _, current, path, g_score = heapq.heappop(self.frontier)
            if current in visited:
                continue
            visited.add(current)
            self.explored.append(current)

            if current == goal:
                return path, g_score, len(self.explored)

            for neighbor in self.edges.get(current, []):
                if neighbor in visited:
                    continue
                edge_cost = self.get_distance(current, neighbor)
                new_g = g_score + edge_cost
                h = self.heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(self.frontier, (new_g + h, counter, neighbor, path + [neighbor], new_g))

        return None, float("inf"), len(self.explored)

# Instancia global
pathfinder = AStarPathFinder(CUENCA_NODES, GRAPH_EDGES)
