from Directo import Directo
from Thompson import Thompson
from Ilustrador import Ilustrador
from Subconjuntos import Subconjuntos
from Postfix import convertirAPostfix, formatearExpresionRegular

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
    "(a|b)*((a|(bb)*)ε)"
]


def crearAFNconThompson(expresion):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).crearGrafoNeo4J()


def crearAFDdesdeAFN(expresion, mostrarPrimitivos=False):

    regex = expresion

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(regex)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    # Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

    AFN_Thompson = Thompson(regex).afn

    # Creamos el automata finito determinista utilizando Subconjuntos

    AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

    AFD_Subconjuntos.mostrarTablaAFD()

    Ilustrador.dibujarAFD(AFD_Subconjuntos, mostrarPrimitivos)


def crearAFDmetodoDirecto(expresion):

    def expandirRegex(regex):

        return regex + "#."

    # Formateamos la expresion regular para que sea valida

    regex = formatearExpresionRegular(expresion)

    # Convertimos la expresion regular de infix a postfix

    regex = convertirAPostfix(regex)

    regexExpandida = expandirRegex(regex)

    directo = Directo(expresionRegularExpandida=regexExpandida)

    afd = directo.afd

    arbol = directo.arbol

    Ilustrador.IlustrarArbolPostOrder(arbol, arbol.numeroUnicoIdentificacion)


if __name__ == "__main__":

    expresionAUtilizar = listaExpresiones[3]

    # Crear un AFN utilizando Thompson e ilustrarlo con Neo4J:

    # crearAFNconThompson(expresionAUtilizar)

    # Crear un AFD utilizando Thompson luego utilizando Subconjuntos e ilustrarlo con Neo4J:

    # crearAFDdesdeAFN(expresionAUtilizar)

    # Crear un AFD utilizando el metodo directo e ilustrarlo con Neo4J:

    # for ex in listaExpresiones:

    #     crearAFDmetodoDirecto(ex)

    crearAFDmetodoDirecto(expresionAUtilizar)
