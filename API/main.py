from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from models.graph import BFSGraph, BellmanFordGraph, DFSGraph, KruskalGraph, PrimDijkstraGraph, DijkstraGraph

app = Flask(__name__, template_folder='swagger/templates')
app.config['RESTPLUS_MASK_SWAGGER'] = False


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Graph-API'
    }
)


@app.route("/api/BFS", methods=['POST'])
def BFS():
    """
    Funkcja obslugujaca punkt koncowy /api/BFS. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu BFS wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    start_vertex = request_data['start_vertex']
    graph = BFSGraph(vertices, adjacency_list, start_vertex)
    return jsonify(graph.search())


@app.route("/api/DFS", methods=['POST'])
def DFS():
    """
    Funkcja obslugujaca punkt koncowy /api/DFS. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu DFS wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    current_vertex = request_data['start_vertex']
    graph = DFSGraph(vertices, adjacency_list, current_vertex)
    return jsonify(graph.search())


@app.route("/api/Kruskal", methods=['POST'])
def Kruskal():
    """
    Funkcja obslugujaca punkt koncowy /api/Kruskal. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu Kruskala wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    weights = request_data['weights']
    graph = KruskalGraph(vertices, adjacency_list, weights)
    return jsonify(graph.find_minimum_spanning_tree())


@app.route("/api/PrimDijkstra", methods=['POST'])
def PrimDijkstra():
    """
    Funkcja obslugujaca punkt koncowy /api/PrimDijkstra. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu Prima-Dijkstry wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    weights = request_data['weights']
    current_vertex = request_data['start_vertex']
    graph = PrimDijkstraGraph(vertices, adjacency_list, weights, current_vertex)
    return jsonify(graph.find_minimum_spanning_tree())

@app.route("/api/Dijkstra", methods=['POST'])
def Dijkstra():
    """
    Funkcja obslugujaca punkt koncowy /api/Dijkstra. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu Dijkstry wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    weights = request_data['weights']
    current_vertex = request_data['start_vertex']
    graph = DijkstraGraph(vertices, adjacency_list, weights, current_vertex)
    return jsonify(graph.find_shortest_paths())


@app.route("/api/BellmanFord", methods=['POST'])
def BellmanFord():
    """
    Funkcja obslugujaca punkt koncowy /api/BellmanFord. Jako odpowiedz na zapytanie zwraca liste krokow algorytmu Bellmana-Forda wykonanego na danym grafie.
    """
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    weights = request_data['weights']
    current_vertex = request_data['start_vertex']
    graph = BellmanFordGraph(vertices, adjacency_list, weights, current_vertex)
    return jsonify(graph.find_shortest_paths())

if __name__ == '__main__':
    """
    Glowna funkcja programu uruchamiajaca aplikacje webowa.
    """
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.run(debug=True)

