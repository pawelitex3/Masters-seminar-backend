import queue
from queue import LifoQueue
from models.edge import Edge, edge_sort
from bisect import insort


class Graph:
    def __init__(self, vertices=list(), adjacency_list=list(), current_vertex=0):
        self.vertices = vertices
        self.adjacency_list = adjacency_list
        self.current_vertex = current_vertex
        self.parents = [-1 for _ in range(len(self.vertices))]
        self.current_edge = (0,0)
        self.steps = list()
        self.collection = list()
        self.red_edges = set()
        self.green_edges = set()
        self.text = ''


class SearchGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, current_vertex=0, collection_type='queue'):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.visited = [0 for _ in range(len(self.vertices))]
        self.collection_type = collection_type

    def add_to_step_list(self, step_number):
        self.steps.append({
            "step_number": step_number,
            f"{self.collection_type}": list(self.collection.queue),
            "visited": self.visited.copy(),
            "parents": self.parents.copy(),
            "current_vertex": self.current_vertex,
            "current_edge": self.current_edge,
            "red_edges": list(self.red_edges),
            "green_edges": list(self.green_edges),
            "info": self.text
        })

    def search(self):
        self.steps = list()
        current_vertex_index = self.vertices.index(self.current_vertex)
        self.collection.put(self.current_vertex)
        self.visited[current_vertex_index] = 1
        step_number = 0

        while not self.collection.empty():
            self.current_vertex = self.collection.get()
            self.current_edge = (0, 0)
            current_vertex_index = self.vertices.index(self.current_vertex)
            neighbours = self.adjacency_list[current_vertex_index]
            #TODO: informacja, że przetwarzany jest pierwszy element z kolejki
            self.text = f'Przetwarzanie wierzchołka {self.current_vertex}.'
            self.add_to_step_list(step_number)

            for neighbour in neighbours:
                current_neighbour_index = self.vertices.index(neighbour)
                self.current_edge = (self.current_vertex, current_neighbour_index)
                if self.visited[current_neighbour_index] == 0:
                    # TODO: informacja, że do kolejki zostały dodane nowe wierzchołki
                    self.text = f'Dodanie wierzchołka {current_neighbour_index} do kolejki. Dodanie krawędzi łączącej wierzchołki {self.current_vertex} oraz {current_neighbour_index} do drzewa wynikowego.'
                    self.collection.put(neighbour)
                    self.visited[current_neighbour_index] = 1
                    self.parents[current_neighbour_index] = self.current_vertex
                    self.green_edges.add((self.current_vertex, current_neighbour_index))
                elif self.parents[self.current_vertex] != current_neighbour_index:
                    self.text = f'Krawędź łącząca wierzchołki {self.current_vertex} oraz {current_neighbour_index} nie zostaje dodana do drzewa wynikowego.'
                    self.red_edges.add((self.current_vertex, current_neighbour_index))
                else:
                    #TODO: ZMIENIĆ OPIS PRZY GRAFIE SKIEROWANYM!!!!!!!!
                    self.red_edges.add((self.current_vertex, current_neighbour_index))
                    self.text = f'Krawędź łącząca wierzchołki {self.current_vertex} oraz {current_neighbour_index} została już wcześniej odwiedzona i dodana do drzewa wynikowego.'
                step_number += 1
                self.add_to_step_list(step_number)

            self.visited[current_vertex_index] = 2
            step_number += 1

        self.text = f'Wynik działania algorytmu.'
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


class MinimumSpanningTreeGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.weights = weights
        self.edge_list = list()
        self.mst_edges = list()
        self.green_vertices = set()
        self.create_edge_list()

    def create_edge_list(self):
        for i in range(len(self.adjacency_list)):
            for j in range(len(self.adjacency_list[i])):
                if self.adjacency_list[i][j] > i:
                    self.edge_list.append(Edge(i, self.adjacency_list[i][j], self.weights[i][j]))    

    def add_to_step_list(self, step_number, current_edge):
        self.steps.append({
            "step_number": step_number,
            #"tree": self.mst_edges.copy(),
            #"parents": self.parents.copy(),
            "current_edge": (current_edge.start, current_edge.end),
            "red_edges": list(self.red_edges),
            "green_edges": list(self.green_edges),
            "green_vertices": list(self.green_vertices),
            "info": self.text
        })


class KruskalGraph(MinimumSpanningTreeGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None):
        super().__init__(vertices, adjacency_list, weights)
        self.edge_list.sort(key=edge_sort)

    def find_representative(self, vertex):
        parent = self.parents[vertex]
        if parent == -1:
            return vertex
        else:
            return self.find_representative(parent)

    def find_minimum_spanning_tree(self):
        step_number = 0
        for edge in self.edge_list:
            vertex1, vertex2 = edge.start, edge.end
            parent1, parent2 = self.find_representative(vertex1), self.find_representative(vertex2)
            self.text = f'Sprawdzanie krawędzi łączącej wierzchołki {vertex1} oraz {vertex2}.'
            self.add_to_step_list(step_number, edge)
            step_number += 1
            if parent1 != parent2:
                self.parents[parent2] = parent1
                self.mst_edges.append(edge.serialize())
                self.green_edges.add((edge.start, edge.end))
                self.green_vertices.add(edge.start)
                self.green_vertices.add(edge.end)
                self.text = f'Krawędź łącząca wierzchołki {vertex1} oraz {vertex2} nie utworzy cyklu - zostaje dodana do drzewa wynikowego.'
                self.add_to_step_list(step_number, edge)
                # TODO: informacja, że krawędź została dodana do drzewa
                if len(self.mst_edges) == len(self.vertices) - 1:
                    # TODO: informacja, że algorytm zakończył się
                    break
            else:
                self.text = f'Krawędź łącząca wierzchołki {vertex1} oraz {vertex2} spowoduje utworzenie cyklu - nie zostaje dodana do drzewa wynikowego.'
                self.red_edges.add((edge.start, edge.end))
                self.add_to_step_list(step_number, edge)
                # TODO: informacja, że krawędź nie została dodana do drzewa
            step_number += 1
        return self.steps


class PrimDijkstraGraph(MinimumSpanningTreeGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, weights, current_vertex)
        self.visited_edge = [-1 for _ in range(len(self.edge_list))]

    def find_and_add_edges(self, edges, vertex):
        # TODO: Czy można to zrobić szybciej?
        new_edges = [x for x in self.edge_list if x.start == vertex or x.end == vertex]
        for edge in new_edges:
            index = self.edge_list.index(edge)
            if self.visited_edge[index] == -1:
                insort(edges, edge, key=edge_sort)
                self.visited_edge[index] = 1

        return edges

    def find_minimum_spanning_tree(self):
        # Nadanie wartosci poczatkowych
        edges = [x for x in self.edge_list if x.start == self.current_vertex or x.end == self.current_vertex]
        edges.sort(key=edge_sort)
        n = len(self.vertices)
        self.parents[self.current_vertex] = -2
        step_number = 0

        for edge in edges:
            index = self.edge_list.index(edge)
            self.visited_edge[index] = 1

        # Sprawdzanie kazdej krawedzi, z ktora incydentne sa wierzcholki w grafie
        while len(edges) > 0 and n - 1 != len(self.mst_edges):
            current_edge = edges[0]
            edges.pop(0)
            vertex1, vertex2 = current_edge.start, current_edge.end
            self.text = f'Sprawdzanie krawędzi łączącej wierzchołki {vertex1} oraz {vertex2}.'
            self.add_to_step_list(step_number, current_edge)
            step_number += 1

            # Jesli pierwszy wierzcholek jeszcze nie jest w grafie
            if self.parents[vertex1] == -1:
                # TODO: Informacja, że krawędź została dodana
                self.mst_edges.append(current_edge.serialize())
                edges = self.find_and_add_edges(edges, vertex1)
                self.parents[vertex1] = vertex2
                self.green_edges.add((vertex1, vertex2))
                self.green_vertices.add(vertex1)
                self.green_vertices.add(vertex2)
                self.text = f'Krawędź łącząca wierzchołki {vertex1} oraz {vertex2} została dodana.'

            # Jesli drugi wierzcholek jeszcze nie jest w grafie
            elif self.parents[vertex2] == -1:
                # TODO: Informacja, że krawędź została dodana
                self.mst_edges.append(edges[0].serialize())
                edges = self.find_and_add_edges(edges, vertex2)
                self.parents[vertex2] = vertex1
                self.green_edges.add((vertex1, vertex2))
                self.green_vertices.add(vertex1)
                self.green_vertices.add(vertex2)
                self.text = f'Krawędź łącząca wierzchołki {vertex1} oraz {vertex2} nie utworzy cyklu - została dodana do drzewa wynikowego.'
            
            # Jesli obydwa wierzcholki sa juz w grafie
            else:
                # TODO: Informacja, że dodanie krawędzi spowoduje powstanie cyklu
                self.red_edges.add((vertex1, vertex2))
                self.text = f'Krawędź łącząca wierzchołki {vertex1} oraz {vertex2} spowoduje powstanie cyklu - nie została dodana do drzewa wynikowego.'

            self.add_to_step_list(step_number, current_edge)
            step_number += 1
            
        return self.steps

    


class ShortestPathsGraph(Graph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, current_vertex)
        self.weights = weights
        self.costs = [100000000 for _ in range(len(self.vertices))]


class DijkstraGraph(ShortestPathsGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, weights, current_vertex)
        self.visited = [-1 for _ in range(len(self.vertices))]
        self.green_vertices = set()

    def add_to_step_list(self, step_number, min_cost_vertex):
        self.steps.append({
            "step_number": step_number,
            "parents": self.parents.copy(),
            "current_vertex": self.current_vertex,
            "visited": self.visited.copy(),
            "costs": self.costs.copy(),
            "min_cost_vertex": min_cost_vertex,
            "green_vertices": list(self.green_vertices),
            "green_edges": list(self.green_edges),
            "info": self.text,
            "current_edge": self.current_edge
        })

    def find_shortest_paths(self):
        step_number = 0
        self.costs[self.current_vertex] = 0
        for vertex in self.adjacency_list[self.current_vertex]:
            vertex_index = self.adjacency_list[self.current_vertex].index(vertex)
            self.costs[vertex] = self.weights[self.current_vertex][vertex_index]
            self.parents[vertex] = self.current_vertex
        self.visited[self.current_vertex] = 1
        
        self.green_vertices.add(self.current_vertex)
        self.text = 'Inicjalizacja - poszukiwanie najtańszego sąsiada wierzchołka startowego.'
        self.add_to_step_list(step_number, self.current_vertex)
        step_number += 1

        for _ in range(len(self.vertices)-1):
            self.current_edge = (0, 0)
            min_cost_vertex = self.visited.index(-1)
            for i in range(min_cost_vertex+1, len(self.vertices)):
                if self.visited[i] == -1 and self.costs[i] < self.costs[min_cost_vertex]:
                    min_cost_vertex = i
            self.text = f'Wybór najtańszego nieodwiedzonego wierzchołka - wierzchołek {min_cost_vertex}.'
            self.green_vertices.add(min_cost_vertex)
            self.green_edges.add((self.parents[min_cost_vertex], min_cost_vertex))
            self.add_to_step_list(step_number, min_cost_vertex)
            step_number += 1

            for neighbour in self.adjacency_list[min_cost_vertex]:
                
                if self.visited[neighbour] == -1:
                    self.text = f'Korekta kosztu na podstawie krawędzi łączącej wierzchołki {min_cost_vertex} oraz {neighbour}.'
                    self.current_edge = (min_cost_vertex, neighbour)
                    neighbour_index = self.adjacency_list[min_cost_vertex].index(neighbour)
                    if self.costs[neighbour] > self.costs[min_cost_vertex] + self.weights[min_cost_vertex][neighbour_index]:
                        self.costs[neighbour] = self.costs[min_cost_vertex] + self.weights[min_cost_vertex][neighbour_index]
                        self.parents[neighbour] = min_cost_vertex
                    self.add_to_step_list(step_number, min_cost_vertex)
                    step_number += 1
            self.visited[min_cost_vertex] = 1
            self.text = f'Wszystkie korekty wierzchołka {min_cost_vertex} zostały dokonane - jest już odwiedzony.'
            self.current_edge = (0, 0)
            self.add_to_step_list(step_number, min_cost_vertex)
            step_number += 1
        return self.steps

    
        

class BellmanFordGraph(ShortestPathsGraph):
    def __init__(self, vertices=None, adjacency_list=None, weights=None, current_vertex=0):
        super().__init__(vertices, adjacency_list, weights, current_vertex)

    def add_to_step_list(self, step_number, current_vertex, current_neighbour):
        self.steps.append({
            "step_number": step_number,
            "parents": self.parents.copy(),
            "current_vertex": current_vertex,
            "current_neighbour": current_neighbour,
            "costs": self.costs.copy(),
            "green_edges": list(self.green_edges),
            "info": self.text,
            "current_edge": self.current_edge
        })

    def find_shortest_paths(self):
        step_number = 0
        self.costs[self.current_vertex] = 0
        for vertex in self.adjacency_list[self.current_vertex]:
            vertex_index = self.adjacency_list[self.current_vertex].index(vertex)
            self.costs[vertex] = self.weights[self.current_vertex][vertex_index]
            self.parents[vertex] = self.current_vertex
            self.green_edges.add((self.current_vertex, vertex))
        
        self.text = 'Inicjalizacja - ustalenie kosztów na podstawie danych o sąsiadach wierzchołka początkowego.'
        self.add_to_step_list(step_number, self.current_vertex, self.current_vertex)
        step_number += 1
        
        for i in range(len(self.vertices)-1):
            for vertex in self.vertices:
                for neighbour in self.adjacency_list[vertex]:
                    neighbour_index = self.adjacency_list[vertex].index(neighbour)
                    if self.costs[neighbour] > self.costs[vertex] + self.weights[vertex][neighbour_index]:
                        self.costs[neighbour] = self.costs[vertex] + self.weights[vertex][neighbour_index]
                        if self.parents[neighbour] != -1:
                            self.green_edges.remove((self.parents[neighbour], neighbour))
                            self.text = f'Iteracja {i+1}: usunięcie krawędzi łączącej wierzchołki {self.parents[neighbour]} oraz {neighbour} z wyniku. '
                        else:
                            self.text = f'Iteracja {i+1}: '
                        self.text += f'Dodanie krawędzi łączącej wierzchołki {vertex} oraz {neighbour} do wyniku. Aktualizacja kosztów dotarcia do wierzchołka {neighbour}.'
                        self.parents[neighbour] = vertex
                        self.green_edges.add((vertex, neighbour))
                    else:
                        self.text = f'Iteracja {i+1}: krawędź łącząca wierzchołki {vertex} oraz {neighbour} nie wnosi żadnych zmian.'

                    self.current_edge = (vertex, neighbour)
                    self.add_to_step_list(step_number, vertex, neighbour)
                    step_number += 1
                self.current_edge = (0, 0)
                self.text = f'Iteracja {i+1}: zakończenie przetwarzania wierzchołka {vertex}.'
                self.add_to_step_list(step_number, vertex, neighbour)
                step_number += 1
        return self.steps

    