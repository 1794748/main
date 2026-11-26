def minTrioDegree(n: int, edges: list[list[int]]) -> int:
    # Matriu d'adjacència de mida (n + 1) x (n + 1) i array de graus
    adj = [[False] * (n + 1) for _ in range(n + 1)]
    degree = [0] * (n + 1)

    for u, v in edges:
        adj[u][v] = True
        adj[v][u] = True
        degree[u] += 1
        degree[v] += 1

    min_degree = float("inf")

    # Recorregut d'ordenació estricta (i < j < k) per evitar comprovar el mateix trio 6 vegades
    for i in range(1, n - 1):
        # Poda: un trio amb node i té com a mínim grau (degree[i] - 2)
        if degree[i] < 2 or degree[i] - 2 >= min_degree:
            continue

        row_i = adj[i]
        for j in range(i + 1, n):
            if not row_i[j] or degree[j] < 2:
                continue
            if degree[i] + degree[j] - 4 >= min_degree:
                continue

            row_j = adj[j]
            for k in range(j + 1, n + 1):
                if row_i[k] and row_j[k]:
                    trio_deg = degree[i] + degree[j] + degree[k] - 6
                    if trio_deg < min_degree:
                        min_degree = trio_deg

    return -1 if min_degree == float("inf") else min_degree


if __name__ == "__main__":
    assert minTrioDegree(6, [[1, 2], [1, 3], [2, 3], [1, 4], [2, 5], [3, 6], [4, 5], [5, 6]]) == 3
    assert minTrioDegree(7, [[1, 2], [2, 3], [3, 1], [3, 4], [4, 5], [5, 6], [6, 4], [6, 7]]) == 1
    assert minTrioDegree(4, [[1, 2], [2, 3], [3, 4]]) == -1
