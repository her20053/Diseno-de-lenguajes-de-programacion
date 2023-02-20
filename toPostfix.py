def convertirAPostfix(expresion):
    # Validar que la expresión no esté vacía
    if not expresion:
        raise ValueError("La expresión está vacía")

    # Validar que la expresión no comience ni termine con un operador
    operadores = set(["|", "*", '.'])
    if expresion[0] in operadores:
        raise ValueError(
            "La expresión no puede comenzar o terminar con un operador")

    # Validar que no haya paréntesis sin cerrar o sin abrir
    stack = []
    for c in expresion:
        if c == "(":
            stack.append(c)
        elif c == ")":
            if not stack:
                raise ValueError("La expresión tiene un paréntesis sin abrir")
            stack.pop()
    if stack:
        raise ValueError("La expresión tiene un paréntesis sin cerrar")

    # Convertir la expresión de infix a postfix
    precedence = {"|": 1, ".": 2, "*": 3}
    stack = []
    postfix = []
    for c in expresion:
        if c == "(":
            stack.append(c)
        elif c == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        elif c in precedence:
            while stack and stack[-1] != "(" and precedence[c] <= precedence[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(c)
        else:
            postfix.append(c)

    while stack:
        postfix.append(stack.pop())

    return "".join(postfix)
