class GrafHash:

    def __init__(self, ln=None, lv=None, lp=None):
        self._nodes = {}
        self._num_edges = 0

        if ln is not None:
            for x in ln:
                self.insert_vertex(x)

        if lv is not None:
            if lp is not None:
                for (n1, n2), p in zip(lv, lp):
                    self.insert_edge(n1, n2, p)
            else:
                for n1, n2 in lv:
                    self.insert_edge(n1, n2)

    def insert_vertex(self, x) -> None:
        if x not in self._nodes:
            self._nodes[x] = {}

    def insert_edge(self, n1, n2, p=1) -> None:
        if n2 not in self._nodes[n1]:
            self._num_edges += 1
        self._nodes[n1][n2] = p
        self._nodes[n2][n1] = p

    def remove_edge(self, n1, n2) -> None:
        if n1 in self._nodes and n2 in self._nodes[n1]:
            del self._nodes[n1][n2]
            del self._nodes[n2][n1]
            self._num_edges -= 1

    def remove_vertex(self, x) -> None:
        if x in self._nodes:
            veins = self._nodes[x]
            self._num_edges -= len(veins)
            for v in veins:
                del self._nodes[v][x]
            del self._nodes[x]

    def has_edge(self, n1, n2) -> bool:
        return n1 in self._nodes and n2 in self._nodes[n1]

    def weight(self, n1, n2):
        if n1 in self._nodes:
            return self._nodes[n1].get(n2, None)
        return None

    def degree(self, x) -> int:
        return len(self._nodes[x])

    def num_vertices(self) -> int:
        return len(self._nodes)

    def num_edges(self) -> int:
        return self._num_edges

    def vertices(self):
        return iter(self._nodes)

    def edges(self, x):
        return iter(self._nodes[x])


if __name__ == "__main__":
    g = GrafHash(
        ["Sants Est.", "Pl. Sants", "Hostafr."],
        [["Sants Est.", "Pl. Sants"], ["Pl. Sants", "Hostafr."]],
        [1585, 511],
    )
    assert g.has_edge("Pl. Sants", "Sants Est.") is True
    assert g.weight("Sants Est.", "Pl. Sants") == 1585
    assert g.degree("Pl. Sants") == 2

    g.insert_vertex("Esp.")
    g.insert_edge("Hostafr.", "Esp.")
    assert g.weight("Esp.", "Hostafr.") == 1
    assert g.num_edges() == 3
    assert sorted(g.edges("Hostafr.")) == ["Esp.", "Pl. Sants"]

    g.remove_vertex("Pl. Sants")
    assert g.has_edge("Sants Est.", "Pl. Sants") is False
    assert g.num_edges() == 1
    assert g.degree("Sants Est.") == 0
    assert sorted(g.vertices()) == ["Esp.", "Hostafr.", "Sants Est."]
