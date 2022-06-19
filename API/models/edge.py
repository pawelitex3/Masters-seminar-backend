class Edge:
    """
    Klasa reprezentujaca pojedyncza krawedz grafu.
    """
    def __init__(self, start=0, end=0, weight=0):
        """
        Tworzy obiekt krawedzi zawierajacej poczatek, koniec oraz wage.
        """
        self.start = start
        self.end = end
        self.weight = weight

    def serialize(self):
        """
        Zwraca obiekt klasy w postaci zserializowanej (w postaci slownika).
        """
        return {
            "start": self.start,
            "end": self.end,
            "weight": self.weight
        }


def edge_sort(edge):
    """
    Wskazuje atrybut klasy Edge, wedlug ktorego ma byc wykonane sortowanie.
    """
    return edge.weight
