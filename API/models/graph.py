import queue
from queue import LifoQueue


class Graph:
    def __init__(self, vertices=None, adjacency_list=None, current_vertex=0):
        if adjacency_list is None:
            adjacency_list = list()
        if vertices is None:
            vertices = list()
        self.vertices = vertices
        self.adjacency_list = adjacency_list
        self.current_vertex = current_vertex
        self.steps = list()
        self.collection = list()


class SearchGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, current_vertex=0, collection_type='queue'):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.parents = [-1 for _ in range(len(self.vertices))]
        self.visited = [0 for _ in range(len(self.vertices))]
        self.collection_type = collection_type

    def add_to_step_list(self, step_number):
        self.steps.append({
            "step_number": step_number,
            f"{self.collection_type}": list(self.collection.queue),
            "visited": self.visited.copy(),
            "parents": self.parents.copy(),
            "current_vertex": self.current_vertex
        })

    def search(self):
        self.steps = list()
        current_vertex_index = self.vertices.index(self.current_vertex)
        self.collection.put(self.current_vertex)
        self.visited[current_vertex_index] = 1
        step_number = 0

        while not self.collection.empty():
            self.current_vertex = self.collection.get()
            current_vertex_index = self.vertices.index(self.current_vertex)
            neighbours = self.adjacency_list[current_vertex_index]
            self.add_to_step_list(step_number)

            for neighbour in neighbours:
                current_neighbour_index = self.vertices.index(neighbour)
                if self.visited[current_neighbour_index] == 0:
                    self.collection.put(neighbour)
                    self.visited[current_neighbour_index] = 1
                    self.parents[current_neighbour_index] = self.current_vertex
                step_number += 1
                self.add_to_step_list(step_number)

            self.visited[current_vertex_index] = 2
            step_number += 1

        self.add_to_step_list(step_number)

        return self.steps

class BFSGraph(SearchGraph):
    def __init__(self, vertices=None, adjacency_list=None, current_vertex=0, collection_type='queue'):
        super().__init__(vertices, adjacency_list, current_vertex, collection_type)
        self.collection = queue.Queue()


class DFSGraph(SearchGraph):
    def __init__(self, vertices=None, adjacency_list=None, current_vertex=0, collection_type='stack'):
        super().__init__(vertices, adjacency_list, current_vertex, collection_type)
        self.collection = LifoQueue()
