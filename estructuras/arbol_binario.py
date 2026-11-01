"""
estructuras/arbol_binario.py — Árbol Binario de Búsqueda (BST), TP3.

Un BST es un árbol donde cada nodo tiene como máximo DOS hijos y cumple
una regla de orden:

        todo lo MENOR va al subárbol izquierdo
        todo lo MAYOR va al subárbol derecho

Gracias a esa regla, para buscar un elemento se compara con el nodo actual
y se descarta una de las dos mitades del árbol en cada paso.

Complejidad (n = cantidad de elementos, h = altura del árbol):
    - insertar y buscar cuestan O(h).
    - Si el árbol está equilibrado, h ≈ log2(n)  ->  O(log n).
    - Si se insertan datos YA ORDENADOS, el árbol se degenera en una cadena
      (h = n)  ->  O(n). Ese es el problema que resuelve el AVL (estructuras/avl.py).
    - Los recorridos visitan todos los nodos: O(n).

En Juegoteca se usa para los recorridos (opción 4 del menú) y como punto de
comparación contra el AVL. La búsqueda del menú ya la hace el AVL.

Las funciones son RECURSIVAS (se llaman a sí mismas), así que Python gasta un
nivel de recursión por cada nivel del árbol. Con árboles muy desbalanceados
(más de ~1000 niveles) hay que subir sys.setrecursionlimit, como hace
algoritmos/comparar_bst_avl.py.
"""


class NodoArbol:
    """Cada caja del árbol. Tiene UN dato y hasta DOS hijos."""

    def __init__(self, dato):
        self.dato = dato          # el elemento (ej: el juego)
        self.izquierdo = None     # hijo menor (va hacia la izquierda)
        self.derecho = None       # hijo mayor (va hacia la derecha)


class ArbolBST:
    """Árbol Binario de Búsqueda ordenado por clave del elemento.

    El árbol no sabe qué tipo de dato guarda (juegos, números, textos...).
    Para ordenar usa una función "clave" que se le pasa en cada operación:
    por ejemplo lambda j: j.get_nombre().lower() ordena los juegos por nombre.
    """

    def __init__(self):
        # La raíz es el nodo de arriba de todo. None significa árbol vacío.
        self.raiz = None

    # ---------- INSERTAR ----------
    def insertar(self, dato, clave):
        """Agrega un elemento. `clave` es una función que devuelve el valor
        por el que se ordena (ej: lambda j: j.get_nombre().lower())."""
        # Si el árbol está vacío, el nuevo dato se convierte en la raíz.
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
        else:
            # Si no, se baja por el árbol buscando su lugar.
            self._insertar_recursivo(self.raiz, dato, clave)

    def _insertar_recursivo(self, nodo, dato, clave):
        # Comparamos la clave del dato nuevo con la del nodo actual.
        if clave(dato) < clave(nodo.dato):
            # Es menor: le toca ir por la izquierda.
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(dato)  # lugar libre: lo ponemos acá
            else:
                self._insertar_recursivo(nodo.izquierdo, dato, clave)  # seguimos bajando
        else:
            # Es mayor o IGUAL: va por la derecha. (A diferencia del AVL, el BST
            # sí guarda los repetidos: por eso con los 2000 juegos tiene 2000
            # nodos y el AVL 1999.)
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(dato)
            else:
                self._insertar_recursivo(nodo.derecho, dato, clave)

    # ---------- BUSCAR ----------
    def buscar(self, valor, clave):
        """Busca por valor. Devuelve el elemento o None si no existe."""
        return self._buscar_recursivo(self.raiz, valor, clave)

    def _buscar_recursivo(self, nodo, valor, clave):
        # Caso base 1: llegamos a un hueco -> el valor no está en el árbol.
        if nodo is None:
            return None
        # Caso base 2: encontramos el valor en este nodo.
        if valor == clave(nodo.dato):
            return nodo.dato
        # Si el valor buscado es menor, solo puede estar en el subárbol
        # izquierdo; si es mayor, en el derecho. La otra mitad se descarta.
        if valor < clave(nodo.dato):
            return self._buscar_recursivo(nodo.izquierdo, valor, clave)
        return self._buscar_recursivo(nodo.derecho, valor, clave)

    # ---------- RECORRIDOS ----------
    # Un recorrido visita TODOS los nodos una vez (O(n)). Lo que cambia entre
    # los tres es el momento en que se "visita" el nodo respecto de sus hijos.
    # Cada uno usa una lista (resultado) que va juntando los datos en orden.
    def inorder(self):
        """Izquierda → raíz → derecha. Devuelve los elementos ORDENADOS."""
        resultado = []
        self._inorder_recursivo(self.raiz, resultado)
        return resultado

    def _inorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierdo, resultado)   # 1º todo lo menor
            resultado.append(nodo.dato)                          # 2º el nodo
            self._inorder_recursivo(nodo.derecho, resultado)     # 3º todo lo mayor

    def preorder(self):
        """Raíz → izquierda → derecha."""
        resultado = []
        self._preorder_recursivo(self.raiz, resultado)
        return resultado

    def _preorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            resultado.append(nodo.dato)                          # 1º el nodo
            self._preorder_recursivo(nodo.izquierdo, resultado)  # 2º izquierda
            self._preorder_recursivo(nodo.derecho, resultado)    # 3º derecha

    def postorder(self):
        """Izquierda → derecha → raíz."""
        resultado = []
        self._postorder_recursivo(self.raiz, resultado)
        return resultado

    def _postorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._postorder_recursivo(nodo.izquierdo, resultado)  # 1º izquierda
            self._postorder_recursivo(nodo.derecho, resultado)    # 2º derecha
            resultado.append(nodo.dato)                           # 3º el nodo

    # ---------- EXTRA: mostrar la estructura ----------
    def altura(self):
        """Profundidad máxima del árbol (cantidad de niveles)."""
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo):
        # Un árbol vacío tiene altura 0.
        if nodo is None:
            return 0
        # La altura de un nodo es 1 (él mismo) más la altura de su rama más
        # profunda. Recorre todo el árbol: O(n).
        return 1 + max(self._altura_recursiva(nodo.izquierdo),
                        self._altura_recursiva(nodo.derecho))