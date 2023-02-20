
def convertirAPostfix(expresion):
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
