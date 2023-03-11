import graphviz as gv


def graficarAutomataFinitoNoDeterminista(afn):

    # Creamos el grafo
    grafo = gv.Digraph(format='png', graph_attr={'rankdir': 'LR'})

    # Agregamos los estados
    for transicion in afn.transiciones:

        estado_dest = str(transicion.destino)
        estado_simb = str(transicion.simbolo)
        estado_orig = str(transicion.origen)

        grafo.edge(estado_orig, estado_dest, label=estado_simb)

    # Agregamos el estado inicial
    grafo.node(str(afn.getEstadoInicial()), shape='circle', style='bold')

    # Agregamos la flecha de inicio
    grafo.node('Inicio', shape='point')

    # Conectamos el estado inicial con la flecha de inicio
    grafo.edge('Inicio', str(afn.getEstadoInicial()))

    # Agregamos el estado de aceptacion
    grafo.node(str(afn.getEstadoFinal()),
               shape='doublecircle', style='bold')

    # Guardamos el grafo
    grafo.render('AFN_Thompson', view=True)


def graficarAutomataFinitoDeterminista(afd, titulo):

    # Creamos el grafo
    grafo = gv.Digraph(format='png', graph_attr={'rankdir': 'LR'})

    # print(afd.transiciones)

    # print(afd.estadosAceptacion)

    # print(afd.estadosIniciales)

    # Agregamos los estados
    for transicion in afd.transiciones:

        estado_dest = str(transicion[2])
        estado_simb = str(transicion[1])
        estado_orig = str(transicion[0])

        grafo.edge(estado_orig, estado_dest, label=estado_simb)

    # Agregamos el estado inicial
    grafo.node(str(afd.estadosIniciales[0]), shape='circle', style='bold')

    # Agregamos la flecha de inicio
    grafo.node('Inicio', shape='point')

    # Conectamos el estado inicial con la flecha de inicio
    grafo.edge('Inicio', str(afd.estadosIniciales[0]))

    # Agregamos los estados de aceptacion
    for estado in afd.estadosAceptacion:

        grafo.node(str(estado), shape='doublecircle', style='bold')

    # Guardamos el grafo
    grafo.render(titulo, view=True)
