from tabulate import tabulate


class Nodo:

    def __init__(self, valor, izquierda=None, derecha=None):

        self.valor = valor

        self.izquierda = izquierda

        self.derecha = derecha

        self.numeroUnicoIdentificacion = None

    def __str__(self):

        return str(self.valor) + " -> " + str(self.numeroUnicoIdentificacion)


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

        self.construir_arbol(self.expresionRegular)

        self.asignarNumeroUnicoArbol()
