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

        for fila in self.afd:

            temporal = []

            temporal.append(fila.primitivo)

            temporal.append(fila.conjuntoDeEstadosAFN)

            temporal.append(fila.estadoDelAFD)

            for k, v in fila.transiciones.items():

                temporal.append(v)

                stringTemporal = "Transicion con " + str(k)

                if stringTemporal not in headersTabla:

                    headersTabla.append(stringTemporal)

            contenidoTabla.append(temporal)

        print(tabulate(contenidoTabla, headersTabla, tablefmt="grid"))

    def crearGrafoNeo4j(self):

        from neo4j import GraphDatabase

        grafo = GraphDatabase.driver(
            uri="neo4j+ssc://96c06d72.databases.neo4j.io", auth=("neo4j", "ILxqsaeqWbPY4PMQkzTjoxL0nYYbip7wCsJcyRDNfx4"))

        session = grafo.session()

        session.run('MATCH (n) DETACH DELETE n')

        # +-------------+-------------------------------------+------------------+--------------------+--------------------+
        # | Primitivo   | Conjunto de estados AFN             | Estado del AFD   | Transicion con a   | Transicion con b   |
        # +=============+=====================================+==================+====================+====================+
        # | ['A']       | ['A']                               | A                | ['B']              | []                 |
        # +-------------+-------------------------------------+------------------+--------------------+--------------------+
        # | []          | []                                  | E                | []                 | []                 |
        # +-------------+-------------------------------------+------------------+--------------------+--------------------+
        # | ['B']       | ['B', 'C', 'D', 'E', 'I']           | B                | ['F']              | ['G', 'J']         |
        # +-------------+-------------------------------------+------------------+--------------------+--------------------+
        # | ['F']       | ['C', 'D', 'E', 'F', 'H', 'I']      | C                | ['F']              | ['G', 'J']         |
        # +-------------+-------------------------------------+------------------+--------------------+--------------------+
        # | ['G', 'J']  | ['C', 'D', 'E', 'G', 'H', 'I', 'J'] | D                | ['F']              | ['G', 'J']         |
        # +-------------+-------------------------------------+------------------+--------------------+--------------------+

        listaEstadosAcepatcion = []
        listaEstadosIniciales = []

        # Estados de aceptacion:  ['D']
        # Estados iniciales:  ['A']

        for fila in self.afd:

            estadosEpsilum = fila.conjuntoDeEstadosAFN

            # Revisamos si contiene al estado de aceptacion el conjunto de estados AFN, si lo contiene, entonces creamos un Nodo de aceptacion en Neo4J

            if self.afn.transiciones[-1].destino in estadosEpsilum:

                session.run(
                    f'CREATE (n:NodeA {{name: "{fila.estadoDelAFD}", aceptacion: true}})')

                listaEstadosAcepatcion.append(fila.estadoDelAFD)

            elif self.afn.transiciones[0].origen in estadosEpsilum:

                session.run(
                    f'CREATE (n:NodeI {{name: "{fila.estadoDelAFD}", inicial: true}})')

                listaEstadosIniciales.append(fila.estadoDelAFD)

            else:

                session.run(f'CREATE (n:Node {{name: "{fila.estadoDelAFD}"}})')

        print("Estados de aceptacion: ", listaEstadosAcepatcion)
        print("Estados iniciales: ", listaEstadosIniciales)

        # Creamos las relaciones entre los nodos

        for fila in self.afd:

            # +-------------+-------------------------------------+------------------+--------------------+--------------------+
            # | Primitivo   | Conjunto de estados AFN             | Estado del AFD   | Transicion con a   | Transicion con b   |
            # +=============+=====================================+==================+====================+====================+
            # | ['A']       | ['A']                               | A                | ['B']              | []                 |
            # +-------------+-------------------------------------+------------------+--------------------+--------------------+

            # Estados de aceptacion:  ['D']
            # Estados iniciales:  ['A']

            # Tenemos que crear una relacion entre el nodo A y el nodo B, con el simbolo a

            for keySimbolo, valuePrimitivo in fila.transiciones.items():

                NodoInicio = fila.estadoDelAFD

                for fila2 in self.afd:

                    if fila2.primitivo == valuePrimitivo:

                        NodoFin = fila2.estadoDelAFD

                        # Ahora revisamos si el nodo de inicio es un estado de aceptacion o inicial o ninguno de los dos

                        if NodoInicio in listaEstadosAcepatcion and NodoFin in listaEstadosAcepatcion:

                            session.run(
                                f''' MATCH (n1:NodeA {{name: "{NodoInicio}"}}) MATCH (n2:NodeA {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio in listaEstadosAcepatcion and NodoFin in listaEstadosIniciales:

                            session.run(
                                f''' MATCH (n1:NodeA {{name: "{NodoInicio}"}}) MATCH (n2:NodeI {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio in listaEstadosIniciales and NodoFin in listaEstadosAcepatcion:

                            session.run(
                                f''' MATCH (n1:NodeI {{name: "{NodoInicio}"}}) MATCH (n2:NodeA {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio in listaEstadosIniciales and NodoFin in listaEstadosIniciales:

                            session.run(
                                f''' MATCH (n1:NodeI {{name: "{NodoInicio}"}}) MATCH (n2:NodeI {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio not in listaEstadosAcepatcion and NodoFin not in listaEstadosIniciales:

                            session.run(
                                f''' MATCH (n1:Node {{name: "{NodoInicio}"}}) MATCH (n2:Node {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio not in listaEstadosAcepatcion and NodoFin in listaEstadosAcepatcion:

                            session.run(
                                f''' MATCH (n1:Node {{name: "{NodoInicio}"}}) MATCH (n2:NodeA {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio not in listaEstadosAcepatcion and NodoFin in listaEstadosIniciales:

                            session.run(
                                f''' MATCH (n1:Node {{name: "{NodoInicio}"}}) MATCH (n2:NodeI {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio in listaEstadosAcepatcion and NodoFin not in listaEstadosIniciales:

                            session.run(
                                f''' MATCH (n1:NodeA {{name: "{NodoInicio}"}}) MATCH (n2:Node {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

                        elif NodoInicio in listaEstadosIniciales and NodoFin not in listaEstadosAcepatcion:

                            session.run(
                                f''' MATCH (n1:NodeI {{name: "{NodoInicio}"}}) MATCH (n2:Node {{name: "{NodoFin}"}}) CREATE (n1)-[:{keySimbolo}]->(n2) ''')

        print("\nGrafo creado con exito\n")

        session.close()


class FilaTablaD:

    def __init__(self, primitivo, conjuntoDeEstadosAFN, estadoDelAFD):

        self.primitivo = primitivo

        self.conjuntoDeEstadosAFN = conjuntoDeEstadosAFN

        self.estadoDelAFD = estadoDelAFD

        self.transiciones = {}

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

        # Tenemos que revisar todos los estados al que el estado actual puede llegar con un epsilon

        listaEstados = []

        listaEstados.append(estado)

        for transicion in self.afn.transiciones:

            if transicion.origen == estado and transicion.simbolo == "ε":

                listaEstados.append(transicion.destino)

                listaEstados += self.cerraduraEpsilon(transicion.destino)

        return list(set(listaEstados))

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
