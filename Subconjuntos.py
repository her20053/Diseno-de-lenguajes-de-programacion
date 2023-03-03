import string
from tabulate import tabulate

# Algoritmo 3.20: La construcción de subconjuntos de un AFD, a partir de un AFN.


class AFD:

    def __init__(self, Tabla, Afn):

        self.afd = Tabla
        self.afn = Afn

    def mostrarTablaAFD(self):

        headersTabla = []

        contenidoTabla = []

        headersTabla.append("Primitivo")

        headersTabla.append("Conjunto de estados AFN")

        headersTabla.append("Estado del AFD")

        headersTabla.append("Aceptacion")

        headersTabla.append("Inicial")

        for fila in self.afd:

            temporal = []

            temporal.append(fila.primitivo)

            temporal.append(fila.conjuntoDeEstadosAFN)

            temporal.append(fila.estadoDelAFD)

            temporal.append(fila.estadoAceptacion)

            temporal.append(fila.estadoInicial)

            for k, v in fila.transiciones.items():

                temporal.append(v)

                stringTemporal = "Transicion con " + str(k)

                if stringTemporal not in headersTabla:

                    headersTabla.append(stringTemporal)

            contenidoTabla.append(temporal)

        print(tabulate(contenidoTabla, headersTabla, tablefmt="grid"))


class FilaTablaD:

    def __init__(self, primitivo, conjuntoDeEstadosAFN, estadoDelAFD):

        self.primitivo = primitivo

        self.conjuntoDeEstadosAFN = conjuntoDeEstadosAFN

        self.estadoDelAFD = estadoDelAFD

        self.transiciones = {}

        self.estadoAceptacion = False

        self.estadoInicial = False

    def agregarTransicion(self, simboloTransicion, estadoDestino):

        self.transiciones[simboloTransicion] = estadoDestino

    def __str__(self):

        return str(self.primitivo) + " -> " + str(self.conjuntoDeEstadosAFN) + " -> " + str(self.estadoDelAFD) + " -> " + str(self.transiciones)

    def mostrarTabulateFila(self):

        headersTabla = []

        tablaTemporal = []

        tablaTemporal.append(self.primitivo)

        headersTabla.append("Primitivo")

        tablaTemporal.append(self.conjuntoDeEstadosAFN)

        headersTabla.append("Conjunto de estados AFN")

        tablaTemporal.append(self.estadoDelAFD)

        headersTabla.append("Estado del AFD")

        tablaTemporal.append([self.estadoAceptacion])

        headersTabla.append("Aceptacion")

        tablaTemporal.append([self.estadoInicial])

        headersTabla.append("Inicial")

        for k, v in self.transiciones.items():

            tablaTemporal.append(v)

            headersTabla.append("Transicion con " + str(k))

        print(tabulate([tablaTemporal], headersTabla, tablefmt="grid"))


class Subconjuntos:

    def __init__(self, afn):

        # ENTRADA: Un AFN N

        self.afn = afn

        # SALIDA: Un AFD D que acepta el mismo lenguaje que N

        self.afd = None

        # Tabla de transiciones del AFD (D)

        self.tablaD = []

        # Cuantos estados se han creado

        self.listaEstadosGenerados = []

        self.estadosGenerados = 0

        # Mantenemos una lista de los estados que ya se han generado (Primitivos)

        self.listaEstadosPrimitivos = []

        # Generamos el AFD a partir del AFN

        self.generarAutomataFinitoDeterminista()

    def mover(self, conjuntoEstados, simbolo):

        posiblesEstados = []

        for transicion in self.afn.transiciones:
            if transicion.origen in conjuntoEstados and transicion.simbolo == simbolo:
                posiblesEstados.append(transicion.destino)

        return posiblesEstados

    def cerraduraEpsilon(self, estado):
        pilaEstados = [estado]
        listaEstados = [estado]

        while len(pilaEstados) > 0:
            estadoActual = pilaEstados.pop()

            for transicion in self.afn.transiciones:
                if transicion.simbolo == "ε" and transicion.origen == estadoActual and transicion.destino not in listaEstados:
                    listaEstados.append(transicion.destino)
                    pilaEstados.append(transicion.destino)

        return listaEstados

    def revisarSiEstadoEsAceptacion(self, estadosEpsiliado):

        # print("Revisando si es aceptacion")

        # print(self.afn.transiciones[-1].destino, estadosEpsiliado)

        if self.afn.transiciones[-1].destino in estadosEpsiliado:

            return True

        return False

    def revisarSiEstadoEsInicial(self, estadosEpsiliados):

        # print("Revizando si es inicial")

        # print(self.afn.transiciones[0].origen, estadosEpsiliados)

        if self.afn.transiciones[0].origen in estadosEpsiliados:

            return True

        return False

    def generarAFD(self, primitivos):

        if primitivos in self.listaEstadosGenerados:

            return

        self.listaEstadosGenerados.append(primitivos)

        cerradurasEpsiliadasTotales = []

        for primitivo in primitivos:
            cerradurasEpsiliadasTotales += self.cerraduraEpsilon(primitivo)

        cerradurasEpsiliadasTotales = sorted(
            list(set(cerradurasEpsiliadasTotales)))

        EstadoDelAFD = list(string.ascii_uppercase)[
            self.estadosGenerados]  # 'C', 'D', 'E', 'F', 'G', 'H'...

        self.estadosGenerados += 1

        filaTemporal = FilaTablaD(
            primitivos, cerradurasEpsiliadasTotales, EstadoDelAFD)

        filaTemporal.estadoAceptacion = self.revisarSiEstadoEsAceptacion(
            cerradurasEpsiliadasTotales)
        filaTemporal.estadoInicial = self.revisarSiEstadoEsInicial(
            cerradurasEpsiliadasTotales)

        for simbolo in self.afn.obtenerCaracteres():

            # Para cada simbolo del AFN, aplicamos la cerradura epsilon a mover(estadoInicialTablaD, simbolo):

            # El resultado de mover puede tener varios estados, por lo que tenemos que aplicar la cerradura epsilon a cada uno de ellos

            resultadosMover = self.mover(cerradurasEpsiliadasTotales, simbolo)

            filaTemporal.agregarTransicion(simbolo, resultadosMover)

            self.generarAFD(resultadosMover)

        self.tablaD.insert(0, filaTemporal)

    def generarAutomataFinitoDeterminista(self):

        # El  estado  inicial  de  D  se  obtiene  al  aplicar cerraduraEpsilon al estado inicial de N.

        estadoInicialAFN = self.afn.getEstadoInicial()

        estadoInicialTablaD = self.cerraduraEpsilon(estadoInicialAFN)

        self.listaEstadosGenerados.append([estadoInicialAFN])

        # Agregamos el estado inicial a la tabla de transiciones del AFD

        # ['D', 'B', 'H', 'A', 'C']
        ConjuntoEstadosAFN = sorted(estadoInicialTablaD)

        EstadoDelAFD = list(string.ascii_uppercase)[
            self.estadosGenerados]  # 'A'

        self.estadosGenerados += 1

        filaInicial = FilaTablaD(
            [estadoInicialAFN], ConjuntoEstadosAFN, EstadoDelAFD)

        filaInicial.estadoAceptacion = self.revisarSiEstadoEsAceptacion(
            ConjuntoEstadosAFN)
        filaInicial.estadoInicial = self.revisarSiEstadoEsInicial(
            ConjuntoEstadosAFN)

        for simbolo in self.afn.obtenerCaracteres():

            # Para cada simbolo del AFN, aplicamos la cerradura epsilon a mover(estadoInicialTablaD, simbolo):

            # El resultado de mover puede tener varios estados, por lo que tenemos que aplicar la cerradura epsilon a cada uno de ellos

            resultadosMover = self.mover(estadoInicialTablaD, simbolo)

            movimientos = []

            # for resultado in resultadosMover:

            #     movimientos += self.cerraduraEpsilon(resultado)

            # movimientos = list(set(movimientos))

            movimientos = sorted(resultadosMover)

            filaInicial.agregarTransicion(simbolo, movimientos)

            self.generarAFD(movimientos)

        self.tablaD.insert(0, filaInicial)

        afd = AFD(self.tablaD, self.afn)

        self.afd = afd
