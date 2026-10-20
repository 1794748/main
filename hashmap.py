
class MyHashMap:
    """Taula hash amb encadenament separat i redimensionament."""

    def __init__(self, cap=13):
        self._table = cap * [None]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)

    def _bucket_put(self, j, key, value):
        """Insereix o actualitza una parella dins del bucket j."""
        if self._table[j] is None:
            self._table[j] = []

        for parella in self._table[j]:
            if parella[0] == key:
                parella[1] = value
                return

        self._table[j].append([key, value])
        self._n += 1

    def _bucket_get(self, j, key):
        """Retorna el valor de la clau dins del bucket j, o -1."""
        if self._table[j] is not None:
            for parella in self._table[j]:
                if parella[0] == key:
                    return parella[1]

        return -1

    def _bucket_remove(self, j, key):
        """Elimina una parella del bucket j, si existeix."""
        if self._table[j] is not None:
            for i, parella in enumerate(self._table[j]):
                if parella[0] == key:
                    self._table[j].pop(i)
                    self._n -= 1

                    if len(self._table[j]) == 0:
                        self._table[j] = None

                    return

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        self._bucket_put(j, key, value)

        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        self._bucket_remove(j, key)

    def _resize(self, c):
        """Crea una taula nova i hi reinsereix totes les parelles."""
        taula_vella = self._table

        self._table = [None] * c
        self._n = 0

        for bucket in taula_vella:
            if bucket is not None:
                for key, value in bucket:
                    j = self._hash_function(key)
                    self._bucket_put(j, key, value)

    def __len__(self):
        return self._n
