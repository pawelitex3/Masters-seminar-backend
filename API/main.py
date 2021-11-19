from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from models.graph import BFSGraph, DFSGraph


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
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    current_vertex = request_data['start_vertex']
    graph = BFSGraph(vertices, adjacency_list, current_vertex)
    return jsonify(graph.search())


@app.route("/api/DFS", methods=['POST'])
def DFS():
    request_data = request.get_json(force=True)
    vertices = request_data['vertices']
    adjacency_list = request_data['adjacency_list']
    current_vertex = request_data['start_vertex']
    graph = DFSGraph(vertices, adjacency_list, current_vertex)
    return jsonify(graph.search())


if __name__ == '__main__':
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    # app.register_blueprint(swaggerui_blueprint, url_prefix='/')
    # app.register_blueprint(swaggerui_blueprint, url_prefix='/api')
    app.run(debug=True)
