from Thompson import Thompson
from toPostfix import convertirAPostfix

expresionRegular = "a.(b*|a).b.c*.(a|b)*"

thompson = Thompson(convertirAPostfix(expresionRegular)).crearGrafoNeo4J()
