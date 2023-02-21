from Thompson import Thompson
from toPostfix import convertirAPostfix, formatearExpresionRegular

# expresionRegular = "a.(b*|a).b?.c+.(a|b)*"
# expresionRegular = "((a|b)*)?.c+"
# expresionRegular = "a?.(b?)?.a*"

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

for expresion in listaExpresiones:

    print("\nPara la expresion", expresion, " es: \n",
          formatearExpresionRegular(expresion) + "\n")


# thompson = Thompson(convertirAPostfix(expresionRegular)).crearGrafoNeo4J()
