from Directo import Directo
from Thompson import Thompson
from Ilustrador import Ilustrador
from Subconjuntos import Subconjuntos

from Minimizacion import minimizarAFD
from Simulacion import simularAFN, simularAFD
from Postfix import convertirAPostfix, formatearExpresionRegular, transformarAIdentidad
from Graficador import graficarAutomataFinitoNoDeterminista, graficarAutomataFinitoDeterminista

listaExpresiones = [
    "(a|b)*abb",
    "a+",
    "a(a|b)*b",
    "0?(1?)?0",
    "a(b*|a)bc*(a|b)*",
    "aa(a|b)+(b|a)bbb",
    "a(b*|a)b?c+(a|b)*",
    "((a|b)*)?c+",
    "a?(b?)?a+",
    "0?(1?)?0+",
    "(a|b)*((a|b)|ε)*",
    "(a|b)*((a|(bb)*)ε)",
    "(a|ε)b(a+)c?",
    "(b|b)*abb(a|b)*",
    "(a|b)*a(a|b)(a|b)",
    "(ab)?a|b",
    "(a|b)a"
]


def crearAFNconThompson(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Graficamos el automata finito no determinista

    graficarAutomataFinitoNoDeterminista(AFN_Thompson)

    # Retornamos el automata finito no determinista

    return AFN_Thompson


def crearAFDdesdeAFN(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Creamos el automata finito determinista utilizando Subconjuntos

    AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

    # Graficamos el automata finito determinista

    graficarAutomataFinitoDeterminista(AFD_Subconjuntos, "AFD_Subconjuntos")

    # Retornamos el automata finito determinista

    return AFD_Subconjuntos


def afdDesdeafn(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Creamos el automata finito determinista utilizando Subconjuntos

    AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

    # Retornamos el automata finito determinista

    return AFD_Subconjuntos


def crearAFDmetodoDirecto(expresion):

    # Para elaborar el AFD directo, se debe expandir la expresion regular

    def expandirRegex(regex):

        return regex + "#."

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(expresion)

    # Convertimos la expresion regular a su forma identidad

    regex = transformarAIdentidad(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    regexExpandida = expandirRegex(regex)

    directo = Directo(regexExpandida)

    # Obtenemos el afd directo

    AFD_Directo = directo.afd

    # Graficamos el automata finito determinista

    graficarAutomataFinitoDeterminista(AFD_Directo, "AFD_Directo")

    # Retornamos el automata finito determinista

    return AFD_Directo


def crearAFDMinimizado(afd):

    # Minimizamos el AFD

    afd_minimizado = minimizarAFD(afd)

    # Graficamos el automata finito determinista minimizado

    graficarAutomataFinitoDeterminista(afd_minimizado, "AFD Minimizado")

    # Retornamos el automata finito determinista minimizado

    return afd_minimizado


if __name__ == "__main__":

    expresionAUtilizar = listaExpresiones[6]

    cadena = "abababbbbabb"

    # ---------------------------------------------------------------------------------------
    # Crear un AFN utilizando Thompson

    # afn = crearAFNconThompson(expresionAUtilizar)

    # Simularlo con una cadena

    # resultadoSimulacion = simularAFN(afn.transiciones, cadena)

    # if resultadoSimulacion:

    #     print("\nLa cadena '" + cadena + "' es aceptada por el AFN propuesto.\n")

    # ---------------------------------------------------------------------------------------
    # Crear un AFD utilizando el metodo directo:

    # afd = crearAFDmetodoDirecto(expresionAUtilizar)

    # ---------------------------------------------------------------------------------------
    # Crear un AFD utilizando Thompson luego utilizando Subconjuntos:

    # afd = crearAFDdesdeAFN(expresionAUtilizar)

    # ---------------------------------------------------------------------------------------
    # Minimizar un AFD generado con Subconjuntos o Directo:

    # afd_minimizado = crearAFDMinimizado(afdDesdeafn(expresionAUtilizar).afd)

    # resultadoSimulacion = simularAFD(afd_minimizado.transiciones, cadena)
    # ---------------------------------------------------------------------------------------

    # for expresion in listaExpresiones:

    #     print("\nLa expresion regular a utilizar es: " + expresion + "\n")

    #     # + Por medio de Thompson:

    #     # afn = crearAFNconThompson(expresion)

    #     # + Por medio de Subconjuntos:

    #     # afd = crearAFDdesdeAFN(expresion)

    #     # + Por medio de Directo:

    #     afd = crearAFDmetodoDirecto(expresion)

    #     input("Presiona enter para continuar...")

    #     # + Minimizar AFD generado con Subconjuntos:

    #     # afd = crearAFDMinimizado(afdDesdeafn(expresion).afd)

    afd = crearAFDmetodoDirecto(expresionAUtilizar)
