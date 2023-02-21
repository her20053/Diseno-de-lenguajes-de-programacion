from Thompson import Thompson
from toPostfix import convertirAPostfix, formatearExpresionRegular

listaExpresiones = [
    "a+",
    "a(a|b)*b",
    "0?(1?)?0",
    "(a|b)*abb",
    "a(b*|a)bc*(a|b)*",
    "aa(a|b)+(b|a)bbb",
    "a(b*|a)b?c+(a|b)*",
    "((a|b)*)?c+",
    "a?(b?)?a*"
]


thompson = Thompson(
    convertirAPostfix(
        formatearExpresionRegular(listaExpresiones[6])
    )
).crearGrafoNeo4J()
