from Thompson import Thompson
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

# Elegimos una expresion regular de la lista

regex = listaExpresiones[-1]

# Formateamos la expresion regular para que sea valida

regex = formatearExpresionRegular(regex)

# Convertimos la expresion regular de infix a postfix

regex = convertirAPostfix(regex)

# Creamos el automata finito no determinista utilizando Thompson, posteriormente lo convertimos a grafo con Neo4J

AFN_Thompson = Thompson(regex).afn

print(AFN_Thompson)

# Creamos el automata finito determinista utilizando Subconjuntos

AFD_Subconjuntos = Subconjuntos(AFN_Thompson).afd

AFD_Subconjuntos.mostrarTablaAFD()
# AFD_Subconjuntos.crearGrafoNeo4j()
