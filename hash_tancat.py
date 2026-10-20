# Estats d'una posició de la taula (hash tancat).
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula hash amb adreçament obert i sondeig lineal."""

    def __init__(self, cap=13):
        self._table = [
            [None, None, LLIURE] for _ in range(cap)
        ]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)

    def _find(self, key):
        """Retorna la posició de la clau o None si no existeix."""
        m = len(self._table)
        j = self._hash_function(key)

        for i in range(m):
            pos = (j + i) % m
            estat = self._table[pos][2]

            if estat == LLIURE:
                return None

            if estat == OCUPAT and self._table[pos][0] == key:
                return pos

            # Si està ESBORRAT, continuem cercant.

        return None

    def put(self, key: int, value: int) -> None:
        m = len(self._table)
        j = self._hash_function(key)
        primer_esborrat = None

        for i in range(m):
            pos = (j + i) % m
            entrada = self._table[pos]
            estat = entrada[2]

            if estat == OCUPAT:
                if entrada[0] == key:
                    # La clau ja existeix: actualitzem el valor.
                    entrada[1] = value
                    break

            elif estat == ESBORRAT:
                # Guardem la primera posició reutilitzable.
                if primer_esborrat is None:
                    primer_esborrat = pos

            else:  # LLIURE
                # Ja podem inserir: no hi ha cap clau més endavant
                # en aquesta seqüència de sondeig.
                if primer_esborrat is not None:
                    pos = primer_esborrat

                self._table[pos] = [key, value, OCUPAT]
                self._n += 1
                break

        else:
            # Hem recorregut tota la taula sense trobar LLIURE.
            if primer_esborrat is not None:
                self._table[primer_esborrat] = [
                    key, value, OCUPAT
                ]
                self._n += 1

        # Factor de càrrega màxim: 0.5.
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        pos = self._find(key)

        if pos is None:
            return -1

        return self._table[pos][1]

    def remove(self, key: int) -> None:
        pos = self._find(key)

        if pos is not None:
            self._table[pos] = [None, None, ESBORRAT]
            self._n -= 1

    def _resize(self, c):
        """Redimensiona la taula i torna a inserir les claus ocupades."""
        taula_vella = self._table

        self._table = [
            [None, None, LLIURE] for _ in range(c)
        ]
        self._n = 0

        # Rehashing: les posicions antigues no es conserven.
        for entrada in taula_vella:
            if entrada[2] == OCUPAT:
                key = entrada[0]
                value = entrada[1]

                j = self._hash_function(key)
                m = len(self._table)

                for i in range(m):
                    pos = (j + i) % m

                    if self._table[pos][2] == LLIURE:
                        self._table[pos] = [key, value, OCUPAT]
                        self._n += 1
                        break

    def __len__(self):
        return self._n
