import queue
import json
from flask import jsonify

class BFS:
    vertices = [0, 1, 2, 3, 4, 5, 6, 7]
    adjacency_list = [[1, 3], [0, 4, 6], [4, 5], [0], [1, 2, 6, 7], [2, 7], [1, 4], [4, 5]]
    visited = [0 for i in range(len(vertices))]
    parent = [100000 for i in range(len(vertices))]
    q = queue.Queue()
    vertex_number = 0
    vertex = 0
    steps = []

    def get_request(self):
        self.search()
        return jsonify(self.steps)

    def search(self):
        self.vertex = self.vertices[self.vertex_number]
        self.q.put(self.vertex)
        self.visited[self.vertex_number] = 1
        step = 0
        self.steps.append({"step": step, "queue": list(self.q.queue), "visited": self.visited.copy(), "parent": self.parent.copy()})
        while not self.q.empty():
            current_vertex = self.q.get()
            neighbours = self.adjacency_list[self.vertices[current_vertex]]
            for neighbour in neighbours:
                if self.visited[neighbour] == 0:
                    self.q.put(neighbour)
                    self.visited[neighbour] = 1
                    self.parent[neighbour] = current_vertex
                    self.steps.append({"step": step, "queue": list(self.q.queue), "visited": self.visited.copy(), "parent": self.parent})
                    step += 1
            self.visited[current_vertex] = 2
            self.steps.append({"step": step, "queue": list(self.q.queue), "visited": self.visited.copy(), "parent": self.parent})
            step += 1
