import queue
from queue import LifoQueue
from models.edge import Edge, edge_sort
from bisect import insort


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
            #TODO: informacja, że przetwarzany jest pierwszy element z kolejki
            self.add_to_step_list(step_number)

            for neighbour in neighbours:
                current_neighbour_index = self.vertices.index(neighbour)
                if self.visited[current_neighbour_index] == 0:
                    # TODO: informacja, że do kolejki zostały dodane nowe wierzchołki
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


class MinimumSpinningTreeGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.weights = weights
        self.edge_list = list()
        self.parents = [-1 for _ in range(len(self.vertices))]
        self.minimum_spinning_tree_edges = list()
        self.steps = list()

        self.create_edge_list()

    def create_edge_list(self):
        for i in range(len(self.adjacency_list)):
            for j in range(len(self.adjacency_list[i])):
                self.edge_list.append(Edge(i, self.adjacency_list[i][j], self.weights[i][j]))

    def find_representative(self, vertex):
        parent = self.parents[vertex]
        if parent == -1:
            return vertex
        else:
            return self.find_representative(parent)

    def add_to_step_list(self, step_number, current_edge):
        self.steps.append({
            "step_number": step_number,
            "tree": self.minimum_spinning_tree_edges.copy(),
            "parents": self.parents.copy(),
            "current_edge": current_edge.serialize()
        })


class KruskalGraph(MinimumSpinningTreeGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None):
        super().__init__(vertices, adjacency_list, weights)
        self.edge_list.sort(key=edge_sort)

    def find_minimum_spinning_tree(self):
        step_number = 0
        for edge in self.edge_list:
            vertex1, vertex2 = edge.start, edge.end
            parent1, parent2 = self.find_representative(vertex1), self.find_representative(vertex2)
            self.add_to_step_list(step_number, edge)
            step_number += 1
            if parent1 != parent2:
                self.parents[parent2] = parent1
                self.minimum_spinning_tree_edges.append(edge.serialize())
                self.add_to_step_list(step_number, edge)
                # TODO: informacja, że krawędź została dodana do drzewa
                if len(self.minimum_spinning_tree_edges) == len(self.vertices) - 1:
                    # TODO: informacja, że algorytm zakończył się
                    break
            else:
                self.add_to_step_list(step_number, edge)
                # TODO: informacja, że krawędź nie została dodana do drzewa
            step_number += 1
        return self.steps


class PrimDijkstraGraph(MinimumSpinningTreeGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, weights, current_vertex)
        self.visited_edge = [-1 for _ in range(len(self.edge_list))]

    def find_minimum_spinning_tree(self):
        edges = [x for x in self.edge_list if x.start == self.current_vertex or x.end == self.current_vertex]
        edges.sort(key=edge_sort)
        n = len(self.vertices)
        self.parents[self.current_vertex] = -2
        step_number = 0

        for edge in edges:
            index = self.edge_list.index(edge)
            self.visited_edge[index] = 1

        self.add_to_step_list(step_number, edges[0])
        step_number += 1

        while len(edges) > 0 and n - 1 != len(self.minimum_spinning_tree_edges):
            current_edge = edges[0]
            vertex1, vertex2 = current_edge.start, current_edge.end
            if self.parents[vertex1] == -1:
                # TODO: Informacja, że krawędź została dodana
                self.minimum_spinning_tree_edges.append(current_edge.serialize())
                edges = self.find_and_add_edges(edges, vertex1)
                self.parents[vertex1] = vertex2

            elif self.parents[vertex2] == -1:
                # TODO: Informacja, że krawędź została dodana
                self.minimum_spinning_tree_edges.append(edges[0].serialize())
                edges = self.find_and_add_edges(edges, vertex2)
                self.parents[vertex2] = vertex1

            else:
                # TODO: Informacja, że dodanie krawędzi spowoduje powstanie cyklu
                pass

            self.add_to_step_list(step_number, current_edge)
            step_number += 1
            edges.pop(0)

        return self.steps

    def find_and_add_edges(self, edges, vertex):
        # TODO: Czy można to zrobić szybciej?
        new_edges = [x for x in self.edge_list if x.start == vertex or x.end == vertex]
        for edge in new_edges:
            index = self.edge_list.index(edge)
            if self.visited_edge[index] == -1:
                insort(edges, edge, key=edge_sort)
                self.visited_edge[index] = 1

        return edges


class ShortestPathsGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.weights = weights
        self.parents = [-1 for _ in range(len(self.vertices))]
        self.costs = [float('inf') for _ in range(len(self.vertices))]
        self.steps = list()


class DijkstraGraph(ShortestPathsGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, weights, current_vertex)
        self.visited = [-1 for _ in range(len(self.vertices))]

    def find_shortest_paths(self):
        self.costs[self.current_vertex] = 0
        for vertex in self.adjacency_list[self.current_vertex]:
            print(f"{self.current_vertex}, {vertex}")
            vertex_index = self.adjacency_list[self.current_vertex].index(vertex)
            self.costs[vertex] = self.weights[self.current_vertex][vertex_index]
            self.parents[vertex] = self.current_vertex
        self.visited[self.current_vertex] = 1

        while self.visited.count(-1) > 0:
            min_cost_vertex = self.visited.index(-1)
            for i in range(min_cost_vertex+1, len(self.vertices)):
                if self.visited[i] == -1 and self.costs[i] < self.costs[min_cost_vertex]:
                    min_cost_vertex = i
            for neighbour in self.adjacency_list[min_cost_vertex]:
                if self.visited[neighbour] == -1:
                    neighbour_index = self.adjacency_list[min_cost_vertex].index(neighbour)
                    if self.costs[neighbour] > self.costs[min_cost_vertex] + self.weights[min_cost_vertex][neighbour_index]:
                        self.costs[neighbour] = self.costs[min_cost_vertex] + self.weights[min_cost_vertex][neighbour_index]
                        self.parents[neighbour] = min_cost_vertex
                self.visited[min_cost_vertex] = 1

        print(self.parents)
