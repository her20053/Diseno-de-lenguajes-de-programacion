from Thompson import Thompson
from toPostfix import convertirAPostfix

expresionRegular = "a.b.b.c*.(a|b)*"
expresionRegular = "a.b.c*"

thompson = Thompson(convertirAPostfix(expresionRegular)).crearGrafoNeo4J()
