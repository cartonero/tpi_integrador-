"""
arbol_general.py — Árbol General (N-ario)

Un árbol general es un árbol donde cada nodo puede tener CUALQUIER cantidad
de hijos (0, 1, 2, 10...). En un árbol binario, en cambio, el límite es 2.
Por eso sirve para representar jerarquías del dominio (categorías, géneros,
carpetas, etc.), donde cada grupo tiene una cantidad distinta de elementos.

En Juegoteca:
    - servicios/categorias.py arma la jerarquía grupos -> géneros con esta clase.
    - La opción 5 del menú ("Explorar categorías") navega y recorre ese árbol.

A diferencia del BST/AVL, acá NO hay regla de orden entre los nodos (un hijo
no es "menor" ni "mayor" que otro): el árbol refleja una jerarquía, no un
orden. Por eso no hay nada que balancear y buscar un nodo cuesta O(n).

Uso:
    from estructuras.arbol_general import NodoGeneral, ArbolGeneral

    arbol = ArbolGeneral()
    raiz = arbol.insertar_raiz("Películas")
    nodo_cat = arbol.agregar_hijo(raiz, "Ciencia Ficción")
    arbol.agregar_hijo(nodo_cat, "Cyberpunk")
    arbol.agregar_hijo(nodo_cat, "Viajes temporales")

Nota: agregar_hijo recibe el NODO padre (lo que devuelven insertar_raiz y
agregar_hijo), no su nombre.
"""


class NodoGeneral:
    """Nodo de un árbol general: tiene un dato y una lista de hijos."""

    def __init__(self, dato):
        self.dato = dato   # lo que guarda el nodo (en Juegoteca, el nombre de una categoría)
        self.hijos = []    # lista de NodoGeneral; vacía = el nodo es una hoja

    def __repr__(self):
        # Texto que se muestra al imprimir un nodo, por ejemplo: Nodo(Indie)
        return f"Nodo({self.dato})"


class ArbolGeneral:
    """Árbol General (n-ario). Cada nodo puede tener 0 o más hijos.

    Se usa para representar jerarquías naturales del dominio, como:
    Películas → Ciencia Ficción → Cyberpunk, Viajes Temporales, IA
             → Acción
             → Comedia
    """

    def __init__(self):
        # La raíz es el nodo de arriba de todo. None significa árbol vacío.
        self.raiz = None

    # ==================== INSERCIÓN ====================

    def insertar_raiz(self, dato):
        """Crea el nodo raíz del árbol. Devuelve el nodo creado.

        Si el árbol ya tenía una raíz, se reemplaza y se pierde lo anterior.
        """
        self.raiz = NodoGeneral(dato)
        return self.raiz

    def agregar_hijo(self, nodo_padre, dato):
        """Agrega un hijo al nodo padre y retorna el nuevo nodo creado.

        Costo O(1): solo agrega un elemento al final de la lista de hijos.
        Se devuelve el nodo nuevo para poder colgarle hijos a él después
        (así se construyen los niveles de arriba hacia abajo).
        """
        # Protección: no se puede agregar un hijo si el árbol no tiene raíz.
        if nodo_padre is None and self.raiz is None:
            raise ValueError("El árbol no tiene raíz. Use insertar_raiz primero.")

        nuevo_nodo = NodoGeneral(dato)
        nodo_padre.hijos.append(nuevo_nodo)
        return nuevo_nodo

    def buscar(self, valor):
        """Busca un nodo cuyo dato == valor en todo el árbol (búsqueda en amplitud).

        Devuelve el nodo o None si no existe.
        """
        if self.raiz is None:
            return None

        # "cola" de nodos pendientes de revisar. Se saca de adelante (pop(0)) y
        # los hijos se agregan atrás (extend): así se revisan primero todos los
        # nodos de un nivel y recién después los del nivel siguiente.
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if actual.dato == valor:
                return actual
            cola.extend(actual.hijos)
        return None

    def buscar_recursivo(self, valor, nodo=None):
        """Busca un nodo por profundidad (DFS). Devuelve el nodo o None.

        Hace lo mismo que buscar(), pero bajando hasta el fondo de cada rama
        antes de pasar a la siguiente. La app usa buscar(); esta versión es
        una alternativa.
        """
        # En la primera llamada nodo es None: se arranca desde la raíz.
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return None  # árbol vacío
        if nodo.dato == valor:
            return nodo
        # Se prueba cada hijo; el primero que encuentre el valor corta la búsqueda.
        for hijo in nodo.hijos:
            resultado = self.buscar_recursivo(valor, hijo)
            if resultado is not None:
                return resultado
        return None

    # ==================== RECORRIDOS ====================

    def amplitud(self):
        """Recorrido en amplitud (BFS): nivel por nivel, de arriba hacia abajo.

        Devuelve una lista con los datos en orden de nivel.
        """
        if self.raiz is None:
            return []

        # Misma técnica de la cola que en buscar(), pero en vez de buscar un
        # valor va anotando todos los datos en el orden en que los visita.
        resultado = []
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            resultado.append(actual.dato)
            cola.extend(actual.hijos)
        return resultado

    def profundidad_preorder(self, nodo=None, resultado=None):
        """Recorrido en profundidad preorder (DFS): nodo → hijos de izquierda a derecha.

        Devuelve una lista con los datos en preorder.
        """
        # Los parámetros nodo y resultado son para la recursión. Cuando se
        # llama desde afuera sin argumentos, se arranca en la raíz y se crea
        # la lista de resultados (se hace acá adentro y no como valor por
        # defecto [] para que no se comparta entre llamadas).
        if nodo is None:
            nodo = self.raiz
        if resultado is None:
            resultado = []
        if nodo is None:
            return resultado

        resultado.append(nodo.dato)          # primero el nodo
        for hijo in nodo.hijos:              # después cada hijo, completo
            self.profundidad_preorder(hijo, resultado)
        return resultado

    def profundidad_postorder(self, nodo=None, resultado=None):
        """Recorrido en profundidad postorder (DFS): hijos → nodo.

        Devuelve una lista con los datos en postorder.
        """
        if nodo is None:
            nodo = self.raiz
        if resultado is None:
            resultado = []
        if nodo is None:
            return resultado

        for hijo in nodo.hijos:              # primero cada hijo, completo
            self.profundidad_postorder(hijo, resultado)
        resultado.append(nodo.dato)          # al final el nodo
        return resultado

    # ==================== INFORMACIÓN ====================

    def altura(self, nodo=None):
        """Altura máxima del árbol (o del subárbol dado)."""
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return 0   # árbol vacío
        if not nodo.hijos:
            return 1   # una hoja tiene altura 1
        # 1 (el nodo) + la altura de su hijo más profundo.
        return 1 + max(self.altura(hijo) for hijo in nodo.hijos)

    def cantidad_nodos(self, nodo=None):
        """Cantidad total de nodos en el árbol (o subárbol)."""
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return 0
        # 1 (el nodo) + la cantidad de nodos de cada uno de sus hijos.
        return 1 + sum(self.cantidad_nodos(hijo) for hijo in nodo.hijos)

    def es_vacio(self):
        return self.raiz is None

    # ==================== UTILIDADES ====================

    def listar_hijos(self, nodo):
        """Retorna los datos de los hijos directos de un nodo."""
        return [hijo.dato for hijo in nodo.hijos]

    def obtener_niveles(self):
        """Retorna los datos organizados por nivel.

        Devuelve una lista de listas: [[raíz], [hijos_de_raíz], [nietos], ...]
        """
        if self.raiz is None:
            return []

        niveles = []
        nivel_actual = [self.raiz]  # nodos del nivel que se está procesando
        while nivel_actual:
            # Se guardan los datos de todos los nodos de este nivel...
            niveles.append([n.dato for n in nivel_actual])
            # ...y se juntan todos sus hijos: ese es el nivel siguiente.
            siguiente = []
            for nodo in nivel_actual:
                siguiente.extend(nodo.hijos)
            nivel_actual = siguiente  # cuando ya no hay hijos, la lista queda vacía y termina
        return niveles

    def __repr__(self):
        # Texto al imprimir el árbol: Árbol General (raíz: Juegoteca, altura: 3)
        if self.raiz is None:
            return "Árbol General vacío"
        return f"Árbol General (raíz: {self.raiz.dato}, altura: {self.altura()})"


# ==================== EJEMPLO DE USO ====================
# Este bloque solo corre al ejecutar el archivo directamente
# (py -m estructuras.arbol_general); NO se ejecuta cuando otro módulo lo importa.

if __name__ == "__main__":
    # Crear un árbol de categorías de películas
    arbol = ArbolGeneral()
    arbol.insertar_raiz("Películas")

    ciencia = arbol.agregar_hijo(arbol.raiz, "Ciencia Ficción")
    accion = arbol.agregar_hijo(arbol.raiz, "Acción")
    comedia = arbol.agregar_hijo(arbol.raiz, "Comedia")

    arbol.agregar_hijo(ciencia, "Cyberpunk")
    arbol.agregar_hijo(ciencia, "Viajes temporales")
    arbol.agregar_hijo(ciencia, "Inteligencia artificial")

    arbol.agregar_hijo(accion, "Superhéroes")
    arbol.agregar_hijo(accion, "Guerra")

    arbol.agregar_hijo(comedia, "Comedia romántica")
    arbol.agregar_hijo(comedia, "Comedia negra")

    print("=== Árbol General de Categorías ===")
    print("Raíz:", arbol.raiz.dato)
    print("Altura:", arbol.altura())
    print("Cantidad de nodos:", arbol.cantidad_nodos())
    print()

    print("--- Recorrido en amplitud ---")
    print(arbol.amplitud())
    print()

    print("--- Recorrido en profundidad (preorder) ---")
    print(arbol.profundidad_preorder())
    print()

    print("--- Recorrido en profundidad (postorder) ---")
    print(arbol.profundidad_postorder())
    print()

    print("--- Niveles ---")
    for i, nivel in enumerate(arbol.obtener_niveles()):
        print(f"  Nivel {i}: {nivel}")
    print()

    print("--- Hijos de 'Ciencia Ficción' ---")
    nodo_ciencia = arbol.buscar("Ciencia Ficción")
    if nodo_ciencia:
        print(arbol.listar_hijos(nodo_ciencia))

    print()
    print("--- Buscar 'Cyberpunk' ---")
    resultado = arbol.buscar("Cyberpunk")
    print("Encontrado:", resultado)