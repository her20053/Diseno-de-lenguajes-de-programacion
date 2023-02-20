from Thompson import Thompson

postfix = 'ab.'
postfix = 'ab|*a.b.b.'
postfix = 'aa.ab|*.ba|.b.b.b.'

thompson = Thompson(postfix)

thompson.crearGrafoNeo4J()
