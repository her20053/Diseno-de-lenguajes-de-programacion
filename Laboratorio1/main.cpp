#include <iostream>
#include <stack>
#include <string>

using namespace std;

// Función para determinar la precedencia de los operadores
int precedence(char op) {
    if (op == '*' || op == '+') {
        return 2;
    }
    else if (op == '|' || op == ')') {
        return 1;
    }
    else {
        return 0;
    }
}

// Función para convertir la expresión regular a postfix
string toPostfix(string infix) {
    stack<char> opStack;
    string postfix = "";

    for (int i = 0; i < infix.length(); i++) {
        char c = infix[i];

        if (c == '(') {
            opStack.push(c);
        }
        else if (c == ')') {
            while (opStack.top() != '(') {
                postfix += opStack.top();
                opStack.pop();
            }
            opStack.pop();
        }
        else if (c == '|' || c == '*' || c == '+') {
            while (!opStack.empty() && precedence(c) <= precedence(opStack.top())) {
                postfix += opStack.top();
                opStack.pop();
            }
            opStack.push(c);
        }
        else {
            postfix += c;
        }
    }

    while (!opStack.empty()) {
        postfix += opStack.top();
        opStack.pop();
    }

    return postfix;
}

int main() {
    string regex1 = "abb*ab+";
    string regex2 = "(0|1)*001+00";

    cout << "Postfix de " << regex1 << ": " << toPostfix(regex1) << endl;
    cout << "Postfix de " << regex2 << ": " << toPostfix(regex2) << endl;

    return 0;
}