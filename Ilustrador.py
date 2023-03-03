from neo4j import GraphDatabase


class Ilustrador:

    def dibujarAFD(afd, mostrarPrimitivos):

        # Creamos el driver para la conexion con Neo4J

        grafo = GraphDatabase.driver(
            uri="neo4j+ssc://96c06d72.databases.neo4j.io", auth=("neo4j", "ILxqsaeqWbPY4PMQkzTjoxL0nYYbip7wCsJcyRDNfx4"))

        session = grafo.session()

        # Borramos cualquier grafo que exista

        session.run('MATCH (n) DETACH DELETE n')

        # Creamos todos los nodos

        diccionarioEstados = {}

        tipoDeNodo = {}

        for fila in afd.afd:

            if fila.estadoAceptacion == True:

                if mostrarPrimitivos == True:

                    session.run(
                        f'CREATE (n:NodeA {{name: "{str(fila.primitivo)}", aceptacion: true}})')

                else:
                    session.run(
                        f'CREATE (n:NodeA {{name: "{fila.estadoDelAFD}", aceptacion: true}})')

                diccionarioEstados[str(fila.primitivo)] = fila
                tipoDeNodo[str(fila.primitivo)] = "NodeA"

            elif fila.estadoInicial == True:

                if mostrarPrimitivos == True:

                    session.run(
                        f'CREATE (n:NodeI {{name: "{str(fila.primitivo)}", inicial: true}})')

                else:

                    session.run(
                        f'CREATE (n:NodeI {{name: "{fila.estadoDelAFD}", inicial: true}})')

                diccionarioEstados[str(fila.primitivo)] = fila
                tipoDeNodo[str(fila.primitivo)] = "NodeI"

            else:

                # Revisemos si es un estado Nulo
                if len(fila.primitivo) == 0:

                    # Es un estado nulo, creamos un nodo especial

                    if mostrarPrimitivos == True:

                        session.run(
                            f'CREATE (n:NodeN {{name: "{str(fila.primitivo)}"}})')

                    else:

                        session.run(
                            f'CREATE (n:NodeN {{name: "{fila.estadoDelAFD}"}})')

                    diccionarioEstados[str(fila.primitivo)] = fila
                    tipoDeNodo[str(fila.primitivo)] = "NodeN"

                else:

                    # Es un estado normal

                    if mostrarPrimitivos == True:

                        session.run(
                            f'CREATE (n:Node {{name: "{str(fila.primitivo)}"}})')

                    else:

                        session.run(
                            f'CREATE (n:Node {{name: "{fila.estadoDelAFD}"}})')

                    diccionarioEstados[str(fila.primitivo)] = fila
                    tipoDeNodo[str(fila.primitivo)] = "Node"

        # print(tipoDeNodo)

        for fila in afd.afd:

            for simbolo, estadoDestino in fila.transiciones.items():

                if simbolo.isdigit():

                    simbolo = 'N' + str(simbolo)

                filaDestino = diccionarioEstados[str(estadoDestino)]

                # Creamos la relacion utilizando el diccionario de tipos de nodo

                if mostrarPrimitivos == True:

                    session.run(f'''
                    MATCH (n1:{tipoDeNodo[str(fila.primitivo)]} {{name: "{tipoDeNodo[str(fila.primitivo)]}"}})
                    MATCH (n2:{tipoDeNodo[str(filaDestino.primitivo)]} {{name: "{tipoDeNodo[str(fila.primitivo)]}"}})
                    CREATE (n1)-[:{str(simbolo)}]->(n2)
                    ''')

                else:
                    session.run(f'''
                    MATCH (n1:{tipoDeNodo[str(fila.primitivo)]} {{name: "{fila.estadoDelAFD}"}})
                    MATCH (n2:{tipoDeNodo[str(filaDestino.primitivo)]} {{name: "{filaDestino.estadoDelAFD}"}})
                    CREATE (n1)-[:{str(simbolo)}]->(n2)
                    ''')

        print("\nGrafo creado con exito\n")

        session.close()

    def dibujarAFN():

        pass
