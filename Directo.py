from tabulate import tabulate


class Nodo:

    def __init__(self, valor, izquierda=None, derecha=None):

        self.valor = valor

        self.izquierda = izquierda

        self.derecha = derecha

        self.numeroUnicoIdentificacion = None

        # Propiedades para el algoritmo de AFD directo

        # Su numero adignado en caso de ser un nodo con un simbolo

        self.numeracionSimbolica = None

        # Su propiedad de anulable:

        self.anulable = None

        # Su conjunto de primeros:

        self.firstpos = None

        # Su conjunto de ultimos:

        self.lastpos = None

        # Su conjunto de siguientes:

        self.followpos = []

    def __str__(self):

        return self.valor

    def obtenerListaHoja(self):

        contenido_tabla = []

        contenido_tabla.append(str(self.valor))
        contenido_tabla.append(str(self.numeracionSimbolica))
        contenido_tabla.append(str(self.anulable))
        contenido_tabla.append(str(self.firstpos))
        contenido_tabla.append(str(self.lastpos))
        contenido_tabla.append(str(self.followpos))

        return contenido_tabla

    def mostrarArbol(self):

        # En post order

        headers = []

        headers.append("Valor")
        headers.append("Numero")
        headers.append("Anulable")
        headers.append("Firstpos")
        headers.append("Lastpos")
        headers.append("Followpos")

        contenido = []

        def postOrder(nodo):
            if nodo is None:
                return
            postOrder(nodo.izquierda)
            postOrder(nodo.derecha)
            contenido.append(nodo.obtenerListaHoja())

        postOrder(self)

        print(tabulate(contenido, headers, tablefmt="grid"))


class AutomataFinitoDeterminista:

    def __init__(self):

        pass


class FilaTabla:

    pass


class Directo:

    def asignarNumeroUnicoArbol(self):

        # Utilizando postorder para asignar un numero unico a cada nodo del arbol

        def recorridoPostOrder(nodo):

            if nodo is None:

                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            nodo.numeroUnicoIdentificacion = self.numeroUnicoNodo

            self.numeroUnicoNodo += 1

        recorridoPostOrder(self.arbol)

    def construir_arbol(self, er):
        pila = []
        for simbolo in er:
            if simbolo == '.':
                derecha = pila.pop()
                izquierda = pila.pop()
                nodo = Nodo('.', izquierda, derecha)
                pila.append(nodo)
            elif simbolo == '|':
                derecha = pila.pop()
                izquierda = pila.pop()
                nodo = Nodo('|', izquierda, derecha)
                pila.append(nodo)
            elif simbolo == '*':
                hijo = pila.pop()
                nodo = Nodo('*', hijo)
                pila.append(nodo)
            elif simbolo == '+':
                hijo = pila.pop()
                nodo = Nodo('+', hijo)
                pila.append(nodo)
            elif simbolo == '?':
                hijo = pila.pop()
                nodo = Nodo('?', hijo)
                pila.append(nodo)
            else:
                nodo = Nodo(simbolo)
                pila.append(nodo)
        self.arbol = pila.pop()

    def obtenerSimbolos(self):

        self.simbolosExpresionRegular = []

        for caracter in self.expresionRegular:
            if caracter not in ["|", ".", "*", "+", "?", "ε", "#"] and caracter not in self.simbolosExpresionRegular:
                self.simbolosExpresionRegular.append(caracter)

    def __init__(self, expresionRegularExpandida):

        self.expresionRegular = expresionRegularExpandida

        self.afd = None

        self.numeroUnicoNodo = 1

        self.numeroPorSimbolo = 1

        self.estadosVisitados = []

        self.transiciones = {}

        self.obtenerSimbolos()

        self.construir_arbol(self.expresionRegular)

        self.asignarNumeroUnicoArbol()

        self.crearAFDdesdeArbol()

    def asignarNumeroPorSimbolo(self):

        def recorridoPostOrder(nodo):

            if nodo is None:

                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            if nodo.valor not in ["|", ".", "*", "+", "?"]:
                nodo.numeracionSimbolica = self.numeroPorSimbolo
                self.numeroPorSimbolo += 1

            nodo.numeroUnicoIdentificacion = self.numeroUnicoNodo

            self.numeroUnicoNodo += 1

        recorridoPostOrder(self.arbol)

    def verificarAnulable(self, nodo):

        # Hoja etiquetada como ε > Verdadero

        if nodo.valor == "ε":
            return True

        # Hoja etiquetada como i > Falso

        if nodo.valor not in ["|", ".", "*", "+", "?"]:
            return False

        # Hoja etiquetada como | > anular(izquierda) or anular(derecha)

        if nodo.valor == "|":
            return self.verificarAnulable(nodo.izquierda) or self.verificarAnulable(nodo.derecha)

        # Hoja etiquetada como . > anular(izquierda) and anular(derecha)

        if nodo.valor == ".":
            return self.verificarAnulable(nodo.izquierda) and self.verificarAnulable(nodo.derecha)

        # Hoja etiquetada como * > Verdadero

        if nodo.valor == "*":
            return True

    def calcularFirstPos(self, nodo):

        if nodo is None:
            return []

        # Hoja etiquetada como ε > Conjunto vacio

        if nodo.valor == "ε":
            return []

        # Hoja etiquetada como i > [numeracionSimbolica]

        if nodo.valor not in ["|", ".", "*", "+", "?"]:
            return [nodo.numeracionSimbolica]

        # Hoja etiquetada como | > firstpos(izquierda) union firstpos(derecha)

        if nodo.valor == "|":
            return self.calcularFirstPos(nodo.izquierda) + self.calcularFirstPos(nodo.derecha)

        # Hoja etiquetada como . > firstpos(izquierda) union firstpos(derecha) si anular(izquierda) es verdadero, sino firstpos(izquierda)

        if nodo.valor == ".":
            if self.verificarAnulable(nodo.izquierda):
                return self.calcularFirstPos(nodo.izquierda) + self.calcularFirstPos(nodo.derecha)
            else:
                return self.calcularFirstPos(nodo.izquierda)

        # Hoja etiquetada como * > firstpos(hijo)

        if nodo.valor == "*":

            if nodo.izquierda != None:

                return self.calcularFirstPos(nodo.izquierda)

            else:

                return self.calcularFirstPos(nodo.derecha)

    def calcularLastPos(self, nodo):

        if nodo is None:
            return []

        # Hoja etiquetada como ε > Conjunto vacio

        if nodo.valor == "ε":
            return []

        # Hoja etiquetada como i > [numeracionSimbolica]

        if nodo.valor not in ["|", ".", "*", "+", "?"]:
            return [nodo.numeracionSimbolica]

        # Hoja etiquetada como | > lastpos(izquierda) union lastpos(derecha)

        if nodo.valor == "|":
            return self.calcularLastPos(nodo.izquierda) + self.calcularLastPos(nodo.derecha)

        # Hoja etiquetada como . > lastpos(izquierda) union lastpos(derecha) si anular(derecha) es verdadero, sino lastpos(derecha)

        if nodo.valor == ".":
            if self.verificarAnulable(nodo.derecha):
                return self.calcularLastPos(nodo.izquierda) + self.calcularLastPos(nodo.derecha)
            else:
                return self.calcularLastPos(nodo.derecha)

        # Hoja etiquetada como * > lastpos(hijo)

        if nodo.valor == "*":
            if nodo.izquierda != None:
                return self.calcularLastPos(nodo.izquierda)
            else:
                return self.calcularLastPos(nodo.derecha)

    def calcularFollowPos(self, raiz):

        # Agregamos todos los nodos a una lista de una forma postorder

        listaNodos = []

        def recorridoPostOrder(nodo):

            if nodo is None:
                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            listaNodos.append(nodo)

        recorridoPostOrder(raiz)

        for nodo in listaNodos:

            if nodo.valor == ".":

                for i in nodo.izquierda.lastpos:

                    # Buscamos el nodo que tenga el numeroUnicoIdentificacion igual a i

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos += nodo.derecha.firstpos

                    # Ordenamos la lista de followpos

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos = sorted(nodo2.followpos)

                    # Eliminamos los elementos repetidos

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos = list(set(nodo2.followpos))

            if nodo.valor == "*":

                for i in nodo.lastpos:

                    # Agregamos los firstpos del nodo hijo

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos += nodo.firstpos

                    # Ordenamos la lista de followpos

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos = sorted(nodo2.followpos)

                    # Eliminamos los elementos repetidos

                    for nodo2 in listaNodos:

                        if nodo2.numeracionSimbolica == i:

                            nodo2.followpos = list(set(nodo2.followpos))

        # Ahora recorremos el arbol de nuevo para asignarle a cada nodo su followpos de manera postorder

        def recorridoPostOrder(nodo):

            if nodo is None:
                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            for i in listaNodos:

                if i.numeroUnicoIdentificacion == nodo.numeroUnicoIdentificacion:

                    nodo.followpos = i.followpos

        recorridoPostOrder(raiz)

        self.listaNodos = listaNodos

        return raiz

    def asignarEstado(self, estado):

        nuevo_estado = tuple(estado)

        if nuevo_estado in self.estadosVisitados:

            return

        self.estadosVisitados.append(nuevo_estado)

        diccionarioTemporal = {}

        for simbolo in self.simbolosExpresionRegular:

            diccionarioTemporal[simbolo] = []

            for numero in estado:

                for nodo in self.listaNodos:

                    if nodo.numeracionSimbolica == numero:

                        if nodo.valor == simbolo:

                            diccionarioTemporal[simbolo].extend(nodo.followpos)

                            diccionarioTemporal[simbolo] = sorted(
                                diccionarioTemporal[simbolo])

                            diccionarioTemporal[simbolo] = list(
                                set(diccionarioTemporal[simbolo]))

                self.asignarEstado(diccionarioTemporal[simbolo])

        self.transiciones[tuple(estado)] = diccionarioTemporal

    def crearAFDRecursivo(self):

        # El estado inicial de D es primera posición de la raíz del árbol sintáctico.

        PosicionInicial = self.arbol.firstpos

        # print(self.simbolosExpresionRegular)

        self.asignarEstado(PosicionInicial)

        self.transiciones = dict(list(self.transiciones.items())[::-1])

        self.transiciones = {k: v for k,
                             v in self.transiciones.items() if k != ()}

        # self.transiciones:
        # (1, 2, 3) {'a': [1, 2, 3, 4], 'b': [1, 2, 3]}
        # (1, 2, 3, 4) {'a': [1, 2, 3, 4], 'b': [1, 2, 3, 5]}
        # (1, 2, 3, 5) {'a': [1, 2, 3, 4], 'b': [1, 2, 3, 6]}
        # (1, 2, 3, 6) {'a': [1, 2, 3, 4], 'b': [1, 2, 3]}

    def crearAFDdesdeArbol(self):

        # Siguiendo los pasos de la presentacion, tenemos que asignarle un numero a cada simbolo (NO OPERADOR) del arbol

        # Esto lo podemos hacer con un recorrido postorder del arbol que llamaremos "asignarNumeroPorSimbolo"

        self.asignarNumeroPorSimbolo()

        # Para el siguiente paso tenemos que crear verificar su funcion anulable:

        # Esto lo podemos conseguir recorriendo el arbol de una manera postorder y verificando si es anulable o no

        def recorridoPostOrder(nodo):

            if nodo is None:

                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            nodo.anulable = self.verificarAnulable(nodo)

        recorridoPostOrder(self.arbol)

        # El siguiente paso es calcular su primera posicion 'firstpos':

        # Esto al igual, los podemos hacer con un recorrido postorder del arbol

        def recorridoPostOrder(nodo):

            if nodo is None:

                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            nodo.firstpos = self.calcularFirstPos(nodo)

        recorridoPostOrder(self.arbol)

        # El siguiente paso es calcular su ultima posicion 'lastpos':

        # Para esto, tenemos que recorrer el arbol de manera postorder y calcular su lastpos

        def recorridoPostOrder(nodo):

            if nodo is None:

                return

            recorridoPostOrder(nodo.izquierda)
            recorridoPostOrder(nodo.derecha)

            nodo.lastpos = self.calcularLastPos(nodo)

        recorridoPostOrder(self.arbol)

        # El siguiente paso es calcular su conjunto de siguientes posiciones 'followpos':

        self.calcularFollowPos(self.arbol)

        self.crearAFDRecursivo()
