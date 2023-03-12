# Algoritmo 3.39: Minimización del número de estados de un AFD.
# Pagina 207 PDF

# ENTRADA: Un AFD D con un conjunto de estados S, el alfabeto de entrada Σ, el estado inicial s0 y el conjunto de estados de aceptación F.

# La tabla de transiciones de D que representa al AFD tiene la siguiente forma para una expresion regular (a|b)*abb.

# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+
# | Primitivo   | Conjunto de estados AFN             | Estado del AFD   | Aceptacion   | Inicial   | Transicion con a   | Transicion con b   |
# +=============+=====================================+==================+==============+===========+====================+====================+
# | ['A']       | ['A', 'B', 'C', 'D', 'H']           | A                | False        | True      | ['E', 'I']         | ['F']              |
# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+
# | ['E', 'I']  | ['B', 'C', 'D', 'E', 'G', 'H', 'I'] | B                | False        | False     | ['E', 'I']         | ['F', 'J']         |
# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+
# | ['F', 'J']  | ['B', 'C', 'D', 'F', 'G', 'H', 'J'] | C                | False        | False     | ['E', 'I']         | ['F', 'K']         |
# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+
# | ['F', 'K']  | ['B', 'C', 'D', 'F', 'G', 'H', 'K'] | D                | True         | False     | ['E', 'I']         | ['F']              |
# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+
# | ['F']       | ['B', 'C', 'D', 'F', 'G', 'H']      | E                | False        | False     | ['E', 'I']         | ['F']              |
# +-------------+-------------------------------------+------------------+--------------+-----------+--------------------+--------------------+

import itertools


particionGlobal = []
afd_original = None


def minimizarAFD(afd_parametro):

    global afd_original

    afd_original = afd_parametro

    # [ 1 ] Empezar con una partición inicial Π con dos grupos, F y S – F, los estados de aceptación [0] y de no aceptación [1]

    Π_Inicial = [[], []]

    for fila in afd_original:

        if fila.estadoAceptacion:

            Π_Inicial[0].append(fila)

        else:

            Π_Inicial[1].append(fila)

    particionar(Π_Inicial)

    # Elegir un estado en cada grupo de Πfinal como el representante para ese grupo.
    # Los representantes serán los estados del AFD D' con el mínimo número de estados.

    representantes = []

    diccionarioRepresentantes = {}

    if [] in particionGlobal:
        particionGlobal.remove([])

    for cluster in particionGlobal:

        representantes.append(cluster[0].estadoDelAFD)

        for filaD in cluster:

            diccionarioRepresentantes[str(
                filaD.primitivo)] = cluster[0].estadoDelAFD

    # print(diccionarioRepresentantes)

    # print(representantes)

    nuevoAFD = AutomataFinitoDeterminista()

    # Determinamos el estado inicial del nuevo AFD

    estadosIniciales = []

    for i in range(len(particionGlobal)):

        grupoAceptacion = False

        for filaD in particionGlobal[i]:

            if filaD.estadoInicial:

                grupoAceptacion = True

                break

        if grupoAceptacion:

            estadosIniciales.append(particionGlobal[i][0].estadoDelAFD)

    nuevoAFD.estadosIniciales = estadosIniciales

    # Determinamos los estados de aceptacion del nuevo AFD

    estadosAceptacion = []

    for i in range(len(particionGlobal)):

        grupoAceptacion = False

        for filaD in particionGlobal[i]:

            if filaD.estadoAceptacion:

                grupoAceptacion = True

                break

        if grupoAceptacion:

            estadosAceptacion.append(particionGlobal[i][0].estadoDelAFD)

    nuevoAFD.estadosAceptacion = estadosAceptacion

    # Determinamos las transiciones del nuevo AFD

    transiciones = []

    for i in range(len(particionGlobal)):

        representanteDelGrupo = particionGlobal[i][0].estadoDelAFD

        for filaD in particionGlobal[i]:

            for simbolo, estado in filaD.transiciones.items():

                transicionTemp = []
                transicionTemp.append(representanteDelGrupo)
                transicionTemp.append(simbolo)
                transicionTemp.append(diccionarioRepresentantes[str(estado)])

                if transicionTemp not in transiciones:
                    transiciones.append(transicionTemp)

    nuevoAFD.transiciones = transiciones

    nuevoAFD.estados = representantes

    return nuevoAFD


def obtenerSimbolos(afd):

    simbolos = []

    for fila in afd:

        for simbolo, estado in fila.transiciones.items():

            if simbolo not in simbolos:

                simbolos.append(simbolo)

    return simbolos


def obtenerIndiceEstado(estado):

    for indice, fila in enumerate(particionGlobal):

        for sublista in fila:

            if estado == sublista.primitivo:

                return indice


def create_combination_lists(dictionary):
    result = {}
    print(dictionary)
    for key, values in dictionary.items():
        value_lists = []
        for value in values.values():
            if isinstance(value, int):
                value_lists.append((value,))
            else:
                value_lists.append(value)
        for val_comb in itertools.product(*value_lists):
            val_tuple = tuple(val_comb)
            if val_tuple in result:
                result[val_tuple].append(key)
            else:
                result[val_tuple] = [key]
    return list(result.values())


def particionar(Π_Inicial):

    # Aplicar el procedimiento siguiente para construir una nueva partición Πnueva.

    global particionGlobal

    Π_Nueva = Π_Inicial.copy()

    particionGlobal = Π_Inicial.copy()

    # for (cada grupo G de Π )

    for grupo in particionGlobal:

        # particionar G en subgrupos, de forma que dos estados s y t
        # se encuentren en el mismo subgrupo, si y sólo si para todos
        # los símbolos de entrada a, los estados s y t tienen transiciones
        # sobre a hacia estados en el mismo grupo de Π

        if len(grupo) > 1:

            # Definimos un diccionario para mantener los estados que se van a unir en un mismo grupo

            diccionarioTemporal = {}

            # Recorremos todos los estados (FilaTablaD) presentes en el grupo

            for estado in grupo:

                # Establecemos un diccionario para cada simbolo del alfabeto

                diccionarioSimbolos = {}

                for simbolo_transicion, estado_destino in estado.transiciones.items():

                    # Vemos a que grupo de la particion global se va con la transicion actual:

                    diccionarioSimbolos[simbolo_transicion] = obtenerIndiceEstado(
                        estado_destino)

                # diccionarioSimbolos:
                # {A}
                # {'a': 1, 'b': 1}
                # {B}
                # {'a': 1, 'b': 1}
                # {C}
                # {'a': 1, 'b': 0}
                # {E}
                # {'a': 1, 'b': 1}

                diccionarioTemporal[str(
                    estado.estadoDelAFD)] = diccionarioSimbolos

            # diccionarioTemporal:
            # {
            #     'A': {'a': 1, 'b': 1},
            #     'B': {'a': 1, 'b': 1},
            #     'C': {'a': 1, 'b': 0},
            #     'E': {'a': 1, 'b': 1}
            # }

            # Eliminamos el grupo de la particion global

            # Particion antes: [['A', 'B', 'C', 'E'], ['D']]

            indice = Π_Nueva.index(grupo)
            Π_Nueva.pop(indice)

            # Particion despues: [['D']]

            for iterador, lista in enumerate(create_combination_lists(diccionarioTemporal)):
                Π_Nueva.insert(indice + iterador, lista)

            # Particion despues: [['D'], ['A', 'B', 'E'], ['C']]

            # NOTA: De la nueva particion Π_Nueva, solamente D sigue siendo un objecto de tipo FilaTablaD, los demas son listas de strings

            # Para arreglar esto, creamos una nueva particion Π_Nueva2 y una lista ejemplo para corroborar

            Π_Nueva2 = []
            Π_NuevaE = []

            for cluster in Π_Nueva:

                lista_grupo = []
                lista_grupo_ejemplo = []

                for estado in cluster:

                    if isinstance(estado, str):

                        for fila in afd_original:

                            if fila.estadoDelAFD == estado:

                                lista_grupo.append(fila)
                                lista_grupo_ejemplo.append(estado)

                    else:

                        lista_grupo.append(estado)
                        lista_grupo_ejemplo.append(estado.estadoDelAFD)

                Π_Nueva2.append(lista_grupo)
                Π_NuevaE.append(lista_grupo_ejemplo)

            # Π_Nueva2:
            # [
            #     [ < Subconjuntos.FilaTablaD object at 0x000002238404B190 > ],
            #     [ < Subconjuntos.FilaTablaD object at 0x000002238404A810 > , < Subconjuntos.FilaTablaD object at 0x000002238404AE90 > , < Subconjuntos.FilaTablaD object at 0x000002238404B310 > ],
            #     [ < Subconjuntos.FilaTablaD object at 0x000002238404B010 > ]
            # ]

            # particionGlobal:
            # [
            #     [< Subconjuntos.FilaTablaD object at 0x000002238404B190 > ],
            #     [ < Subconjuntos.FilaTablaD object at 0x000002238404A810 > , < Subconjuntos.FilaTablaD object at 0x000002238404AE90 > , < Subconjuntos.FilaTablaD object at 0x000002238404B010 > , < Subconjuntos.FilaTablaD object at 0x000002238404B310 > ]
            # ]

            # Si Πnueva = Π, dejar que Πfinal = Π y continuar
            if Π_Nueva2 == particionGlobal:

                return Π_Nueva2

            # De no ser así, repetir el paso (2) con Πnueva en vez de Π
            particionar(Π_Nueva2)


class AutomataFinitoDeterminista:

    def __init__(self):

        self.estadosIniciales = []

        self.estadosAceptacion = []

        self.transiciones = []

        self.estados = []
