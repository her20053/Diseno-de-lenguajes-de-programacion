def simularAFN(transiciones, cadena):
    estados_actuales = epsilon_closure(transiciones, [transiciones[0].origen])
    for simbolo in cadena:
        nuevos_estados = []
        for estado in estados_actuales:
            for transicion in transiciones:
                if transicion.origen == estado and transicion.simbolo == simbolo:
                    nuevos_estados.extend(epsilon_closure(
                        transiciones, [transicion.destino]))
        estados_actuales = nuevos_estados
    return any(estado == transiciones[-1].destino for estado in estados_actuales)


def epsilon_closure(transiciones, estados):
    resultado = set(estados)
    for estado in estados:
        for transicion in transiciones:
            if transicion.origen == estado and transicion.simbolo == "ε":
                resultado.add(transicion.destino)
                resultado = resultado.union(
                    epsilon_closure(transiciones, [transicion.destino]))
    return list(resultado)


def simularAFD(transiciones, cadena):

    print(transiciones)
