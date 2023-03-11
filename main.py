from Directo import Directo
from Thompson import Thompson
from Ilustrador import Ilustrador
from Subconjuntos import Subconjuntos

from Minimizacion import minimizarAFD
from Simulacion import simularAFN, simularAFD
from Postfix import convertirAPostfix, formatearExpresionRegular
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
    "((ab)+|c)?"
]


def crearAFNconThompson(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    # AFN_Thompson = Thompson(regex).crearGrafoNeo4J()

    AFN_Thompson = Thompson(regex).afn

    graficarAutomataFinitoNoDeterminista(AFN_Thompson)

    return AFN_Thompson


def crearAFDdesdeAFN(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # print(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Creamos el automata finito determinista utilizando Subconjuntos

    AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

    # if mostrarTablaAFD:

    # AFD_Subconjuntos.mostrarTablaAFD()

    # if ilustrarAFD:

    #     Ilustrador.dibujarAFD(AFD_Subconjuntos)

    graficarAutomataFinitoDeterminista(AFD_Subconjuntos, "AFD_Subconjuntos")

    return AFD_Subconjuntos


def afdDesdeafn(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # print(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Creamos el automata finito determinista utilizando Subconjuntos

    AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

    # AFD_Subconjuntos.mostrarTablaAFD()

    return AFD_Subconjuntos


def crearAFDmetodoDirecto(expresion):

    def expandirRegex(regex):

        return regex + "#."

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(expresion)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    regexExpandida = expandirRegex(regex)

    directo = Directo(expresionRegularExpandida=regexExpandida)

    # Obtenemos el arbol sintactico de la expresion regular para poder ilustrarlo

    arbol = directo.arbol

    Ilustrador.IlustrarArbolPostOrder(arbol, arbol.numeroUnicoIdentificacion)


def crearAFDMinimizado(afd):

    afd_minimizado = minimizarAFD(afd)

    graficarAutomataFinitoDeterminista(afd_minimizado, "AFD Minimizado")

    return afd_minimizado


if __name__ == "__main__":

    expresionAUtilizar = listaExpresiones[0]

    cadena = "abababbbbabb"

    # ---------------------------------------------------------------------------------------
    # Crear un AFN utilizando Thompson

    # afn = crearAFNconThompson(expresionAUtilizar)

    # # Simularlo con una cadena

    # resultadoSimulacion = simularAFN(afn.transiciones, cadena)

    # if resultadoSimulacion:

    #     print("\nLa cadena '" + cadena + "' es aceptada por el AFN propuesto.\n")

    # ---------------------------------------------------------------------------------------
    # Crear un AFD utilizando Thompson luego utilizando Subconjuntos:

    # afd = crearAFDdesdeAFN(expresionAUtilizar)

    # Simularlo con una cadena

    # resultadoSimulacion = simularAFD(afd.transiciones, cadena)

    # ---------------------------------------------------------------------------------------
    # Crear un AFD utilizando el metodo directo:

    # crearAFDmetodoDirecto(expresionAUtilizar)
    # ---------------------------------------------------------------------------------------
    # Minimizar un AFD generado con Subconjuntos:

    afd_minimizado = crearAFDMinimizado(afdDesdeafn(expresionAUtilizar).afd)

    resultadoSimulacion = simularAFD(afd_minimizado.transiciones, cadena)
    # ---------------------------------------------------------------------------------------
