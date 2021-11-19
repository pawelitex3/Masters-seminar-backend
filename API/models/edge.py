class Edge:
    def __init__(self, start=0, end=0, weight=0):
        self.start = start
        self.end = end
        self.weight = weight


def edge_sort(edge):
    return edge.weight
