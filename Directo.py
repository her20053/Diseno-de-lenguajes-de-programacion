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

        self.followpos = None

    def __str__(self):

        return str(self.valor)


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

    def __init__(self, expresionRegularExpandida):

        self.expresionRegular = expresionRegularExpandida

        self.afd = None

        self.numeroUnicoNodo = 1

        self.numeroPorSimbolo = 1

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
