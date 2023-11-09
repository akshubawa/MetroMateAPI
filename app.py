from fastapi import FastAPI, HTTPException
import csv
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict, deque

app = FastAPI()

app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, u, v, line):
        self.adj[u].append((v, line))
        self.adj[v].append((u, line))

    def find_path(self, source, destination):
        visited = set()
        queue = deque()
        parent = {}

        visited.add(source)
        queue.append(source)

        while queue:
            current = queue.popleft()

            if current == destination:
                path = []
                lines = []
                node = destination

                while node != source:
                    path.append(node)

                    for neighbor, line in self.adj[node]:
                        if neighbor == parent[node]:
                            lines.append(line)
                            break

                    node = parent[node]
                path.append(source)
                lines.append(lines[-1])

                lines = lines[::-1]
                path = path[::-1]
                interchange = []

                for i in range(0,len(lines)-1):
                    if (lines[i]!=lines[i+1]):
                        interchange.append(path[i])                    

                return {
                    "source": source,
                    "destination": destination,
                    "number_of_stations": len(path),
                    "number_of_interchanges": sum(lines[i] != lines[i + 1] for i in range(len(lines) - 1)),
                    "interchange": interchange,
                    "time": len(path) * 2.5,
                    "path": path,
                    "lines": lines
                    
                }

            for neighbor, line in self.adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        raise HTTPException(status_code=404, detail=f"No path found between {source} and {destination}")

metro_graph = Graph()

with open("dataset/metro_data.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        u = row["SOURCE"]
        v = row["DESTINATION"]
        line = row["LINE"]
        metro_graph.add_edge(u, v, line)

@app.get("/route")
def get_route(source: str, destination: str):
    result = metro_graph.find_path(source.upper(), destination.upper())
    return result
