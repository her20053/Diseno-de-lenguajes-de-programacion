import string


class AFN:

    def __init__(self):

        self.transiciones = []

    def agregarTransicion(self, transicion):

        self.transiciones.append(transicion)

    def obtenerCaracteres(self):

        listaCaracteres = []

        for transicion in self.transiciones:

            if transicion.simbolo not in listaCaracteres:

                listaCaracteres.append(transicion.simbolo)

        return listaCaracteres

    def __str__(self):

        resultado = "\nAFN: \n"

        for transicion in self.transiciones:

            resultado += str(transicion) + "\n"

        return resultado


class Transicion:
    def __init__(self, origen, destino, simbolo):
        self.origen = origen
        self.destino = destino
        self.simbolo = simbolo

    def __str__(self):
        return f"[Transicion ({self.origen}, {self.simbolo}, {self.destino})]"


class Thompson:

    # Constructor de la clase Thompson
    # Recibe como parametro una expresion regular en notacion posfija
    # Inicializa la cantidad de estados generados en 0

    def __init__(self, expresion):

        self.expresion = expresion

        self.cantidadEstadosGenerados = 0

        self.generarAutomataFinitoNoDeterminista()

    # Metodo encargado de renombrar los estados del AFN para un mejor manejo

    def renombrarEstados(self):

        listaLetras = list(string.ascii_uppercase)

        diccionarioEstados = {}

        for transicion in self.afn.transiciones:

            if transicion.origen not in diccionarioEstados:

                diccionarioEstados[transicion.origen] = listaLetras.pop(0)

            if transicion.destino not in diccionarioEstados:

                diccionarioEstados[transicion.destino] = listaLetras.pop(0)

        for transicion in self.afn.transiciones:

            transicion.origen = diccionarioEstados[transicion.origen]
            transicion.destino = diccionarioEstados[transicion.destino]

    # Metodo encargado de obtener todos los estados que tiene el AFN

    def obtenerEstados(self):

        estados = []

        for transicion in self.afn.transiciones:

            if transicion.origen not in estados:

                estados.append(transicion.origen)

            if transicion.destino not in estados:

                estados.append(transicion.destino)

        self.estadoAceptacion = self.afn.transiciones[-1].destino
        self.estadoInicial = self.afn.transiciones[0].origen

        return estados

    # Metodo utilizado para ilustrar el AFN generado por el algoritmo de Thompson

    def crearGrafoNeo4J(self):

        from neo4j import GraphDatabase
        import logging
        from neo4j.exceptions import ServiceUnavailable

        # Obtenemos todos los estados del afn

        listaEstados = self.obtenerEstados()

        # Creamos la conexion con la base de datos

        # ILxqsaeqWbPY4PMQkzTjoxL0nYYbip7wCsJcyRDNfx4

        grafo = GraphDatabase.driver(
            uri="neo4j+ssc://96c06d72.databases.neo4j.io", auth=("neo4j", "ILxqsaeqWbPY4PMQkzTjoxL0nYYbip7wCsJcyRDNfx4"))

        session = grafo.session()

        # Borramos cualquier grafo que exista

        session.run('MATCH (n) DETACH DELETE n')

        # Creamos los nodos

        for estado in listaEstados:

            if estado == self.estadoAceptacion:

                session.run(
                    f'CREATE (n:Node {{name: "{estado}", aceptacion: true}})')

            elif estado == self.estadoInicial:

                session.run(
                    f'CREATE (n:Node {{name: "{estado}", inicial: true}})')

            else:
                session.run(f'CREATE (n:Node {{name: "{estado}"}})')

        # Creamos las relaciones

        for transicion in self.afn.transiciones:

            primerNodo = transicion.origen
            segundoNodo = transicion.destino
            simbolo = transicion.simbolo

            session.run(f''' 
                MATCH (n1:Node {{name: "{primerNodo}"}})
                MATCH (n2:Node {{name: "{segundoNodo}"}})
                CREATE (n1)-[:{simbolo}]->(n2)
                ''')

        # Almacenamos el resultado de la consulta
        result = session.run("MATCH p=()-[:b|e|a]->() RETURN p")

        print()
        print("Grafo creado con exito")

        session.close()

    def guardarImagenAFN(self):

        from py2neo import Graph
        from py2neo.data import Node, Relationship
        from pydot import Dot, Node as pydotNode, Edge

        # Connect to the Neo4j database
        graph = Graph("neo4j+ssc://96c06d72.databases.neo4j.io",
                      auth=("neo4j", "ILxqsaeqWbPY4PMQkzTjoxL0nYYbip7wCsJcyRDNfx4"))

        results = graph.run("MATCH p=()-[:b|e|a]->() RETURN p LIMIT 25")

        dot = Dot()

        for record in results:
            for segment in record['p'].segments:
                start_node = segment.start_node
                end_node = segment.end_node
                rel = segment.relationship
                dot.add_node(pydotNode(str(start_node.identity),
                             label=str(start_node.properties)))
                dot.add_node(pydotNode(str(end_node.identity),
                             label=str(end_node.properties)))
                dot.add_edge(Edge(str(start_node.identity), str(
                    end_node.identity), label=rel.type))

        dot.write_png('afn.png')

    # Metodo que se encarga de verificar si un caracter es un operador

    def esOperador(self, caracter):

        return caracter == '*' or caracter == '.' or caracter == '|' or caracter == '+'

    # Metodo que se encarga de verificar si un operador es binario o unario

    def esBinario(self, caracter):

        return caracter == '.' or caracter == '|' or caracter == '+'

    # Regla 1: Simbolo, esta regla se encarga de generar un AFN que solo acepta un simbolo
    # Ejemplo: a
    # AFN: estado 0 -> a -> estado 1
    # Ejemplo concreto:  a = [0a1]

    def reglaSimbolo(self, simbolo):

        afnTemporal = AFN()

        estadoActual = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        estadoSiguiente = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        transicionTemporal = Transicion(estadoActual, estadoSiguiente, simbolo)

        afnTemporal.agregarTransicion(transicionTemporal)

        return afnTemporal

    # Regla 2: Concatenacion, esta regla se encarga de generar un AFN que acepta la concatenacion de dos AFN
    # Ejemplo: ab.
    # AFN: estado 0 -> a -> estado 1 -> b -> estado 2
    # Ejemplo concreto:  [0a1][2b3] = [0a1][1b3]

    def reglaConcatenacion(self, afn1, afn2):

        afnFinal = AFN()

        # Agregamos las transiciones del primer AFN

        for transicion in afn1.transiciones:

            afnFinal.agregarTransicion(transicion)

        # Organizamos los estados del segundo AFN de tal manera que el ultimo estado del primer AFN sea el estado inicial del segundo AFN

        estadoFAFN1 = afn1.transiciones[-1].destino
        estadoIAFN2 = afn2.transiciones[0].origen

        for transicion in afn2.transiciones:

            if transicion.origen == estadoIAFN2:

                transicion.origen = estadoFAFN1

        # Agregamos las transiciones del segundo AFN

        for transicion in afn2.transiciones:

            afnFinal.agregarTransicion(transicion)

        return afnFinal

    # Regla 3: OR, esta regla se encarga de generar un AFN que acepta la union de dos AFN
    # Ejemplo: b|c
    # AFN:          estado 1 -> b -> estado 2
    #           / e                             \ e
    # estado 0                                      estado 5
    #           \ e                             / e
    #               estado 3 -> c -> estado 4
    #
    # Ejemplo concreto:  [2b3][4c5] =
    #      [2b3]
    # [1e2]     [3e6]
    # [1e4]     [5e6]
    #      [4c5]

    def reglaOR(self, afn1, afn2):

        afnFinal = AFN()

        # Creamos el estado inicial

        estadoInicial = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        # Creamos el estado final

        estadoFinal = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        # Creamos la transicion vacia del estado inicial al primer AFN

        transicionTemporal1 = Transicion(
            estadoInicial, afn1.transiciones[0].origen, 'e')

        # Creamos la transicion vacia del estado inicial al segundo AFN

        transicionTemporal2 = Transicion(
            estadoInicial, afn2.transiciones[0].origen, 'e')

        # Agregamos las transiciones al AFN final

        afnFinal.agregarTransicion(transicionTemporal1)
        afnFinal.agregarTransicion(transicionTemporal2)

        # Para este paso ya tenemos:
        #
        # [1e2]
        # [1e4]
        #

        # Agregamos las transiciones del primer AFN

        for transicion in afn1.transiciones:

            afnFinal.agregarTransicion(transicion)

        # Agregamos las transiciones del segundo AFN

        for transicion in afn2.transiciones:

            afnFinal.agregarTransicion(transicion)

        # Para este paso ya tenemos:

        #      [2b3]
        # [1e2]
        # [1e4]
        #      [4c5]

        # Obtenemos el ultimo estado del primer AFN

        ultimoEstadoAFN1 = afn1.transiciones[-1].destino

        # Obtener el ultimo estado del segundo AFN

        ultimoEstadoAFN2 = afn2.transiciones[-1].destino

        # Creamos la transicion vacia del ultimo estado del primer AFN al estado final

        transicionTemporal1 = Transicion(ultimoEstadoAFN1, estadoFinal, 'e')

        # Creamos la transicion vacia del ultimo estado del segundo AFN al estado final

        transicionTemporal2 = Transicion(ultimoEstadoAFN2, estadoFinal, 'e')

        # Agregamos las transiciones al AFN final

        afnFinal.agregarTransicion(transicionTemporal1)
        afnFinal.agregarTransicion(transicionTemporal2)

        # Para este paso ya tenemos:

        #      [2b3]
        # [1e2]     [3e6]
        # [1e4]     [5e6]
        #      [4c5]

        return afnFinal

    # Regla 4: Cerradura de Kleene, esta regla se encarga de generar un AFN que acepta la cerradura de Kleene de un AFN
    # Ejemplo: a*
    # AFN:
    #                  ____________________>_____________________
    #                 / e                                        \ e
    #          estado 0 -> e -> estado 1 -> a -> estado 2 -> e -> estado 3
    #                               e\             / e
    #                                 \___________/

    def reglaKleene(self, afn):

        afnFinal = AFN()

        # Creamos el estado inicial

        estadoInicial = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        # Creamos el estado final

        estadoFinal = self.cantidadEstadosGenerados

        self.cantidadEstadosGenerados += 1

        # Creamos la transicion vacia del estado inicial al estado final

        transicionEstadoInicialAFinal = Transicion(
            estadoInicial, estadoFinal, 'e')

        # Creamos la transicion vacia desde el estado inicial al primer del AFN

        transicionEstadoInicialAIncialAFN = Transicion(
            estadoInicial, afn.transiciones[0].origen, 'e')

        # Agregamos las transiciones al AFN final

        afnFinal.agregarTransicion(transicionEstadoInicialAIncialAFN)

        # Agregamos las transiciones del AFN

        for transicion in afn.transiciones:

            afnFinal.agregarTransicion(transicion)

        # Creamos la transicion vacia desde el ultimo estado del AFN al estado final

        transicionEstadoUltimoAFNAFinal = Transicion(
            afn.transiciones[-1].destino, estadoFinal, 'e')

        # Agregamos la transicion al AFN final

        afnFinal.agregarTransicion(transicionEstadoUltimoAFNAFinal)

        # Creamos la transicion vacia desde el ultimo estado del AFN al primer estado del AFN

        transicionEstadoUltimoAPrimero = Transicion(
            afn.transiciones[-1].destino, afn.transiciones[0].origen, 'e')

        # Agregamos la transicion al AFN final

        afnFinal.agregarTransicion(transicionEstadoUltimoAPrimero)

        # Agregamos la transicion vacia del estado inicial al estado final

        afnFinal.agregarTransicion(transicionEstadoInicialAFinal)

        return afnFinal

    # Generacion de AFN: Se encarga de generar un AFN a partir de una expresion regular en notacion posfija
    # Ejemplo: ab.
    # AFN: estado 0 -> a -> estado 1 -> b -> estado 2

    def generarAutomataFinitoNoDeterminista(self):

        stack = []

        for caracter in self.expresion:

            # Si el caracter no es un operador, entonces es un simbolo
            if not self.esOperador(caracter):

                # Regla 1: Simbolo

                afnTemporal = self.reglaSimbolo(caracter)

                stack.append(afnTemporal)

            # Si el caracter es un operador, entonces
            else:

                # Si el caracter es un operador binario

                if self.esBinario(caracter):

                    # Extraemos los dos ultimos AFN del stack

                    afnTemporal2 = stack.pop()
                    afnTemporal1 = stack.pop()

                    # Revisamos que operando es, para aplicar la regla correspondiente

                    if caracter == '.':

                        # Regla 2: Concatenacion

                        afnTemporal = self.reglaConcatenacion(
                            afnTemporal1, afnTemporal2
                        )

                        stack.append(afnTemporal)

                    elif caracter == '|' or caracter == '+':

                        # Regla 3: OR

                        afnTemporal = self.reglaOR(afnTemporal1, afnTemporal2)

                        stack.append(afnTemporal)

                # Si el caracter es un operador unario "Kleen"

                else:

                    # Extraemos el ultimo AFN del stack

                    afnTemporal = stack.pop()

                    # Regla 4: Kleen

                    afnTemporal = self.reglaKleene(afnTemporal)

                    stack.append(afnTemporal)

        # Retornamos el AFN final

        self.afn = stack.pop()

        # Reorganizamos los estados del AFN

        self.renombrarEstados()

        # Obtenemos los estados del AFN

        self.obtenerEstados()
