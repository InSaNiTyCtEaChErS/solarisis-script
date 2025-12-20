def set(expressions):
    
    precedence = {'+': 1, '-': 1, '<<': 1,'>>': 1, '*': 2, '/': 2, '^': 3}
    output = []
    output2 = []
    operator_stack = []
    expression = ""
    i = 0


    for character in expressions:
        expression += character
        if character != " ":
            expression += " "

    tokens = expression.split()

    for token in tokens:
        i += 1
        print("token = "+token)
        
        if token == "=":
            output.append(output[0])
        elif token in variables:
            c_a("load_16 r"+str(i)+" ["+str(variables.index(token)*4)+"]") #handle variables
            output.append("r"+str(i))
        elif token.isnumeric() or (token.startswith('-') and token[1:].isnumeric()):  # Handle numbers (including negative)
            c_a("mov r"+str(i)+" "+str(token))
            output.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Pop the '('
        elif token in precedence:
            while (operator_stack and operator_stack[-1] != '(' and
                    precedence.get(operator_stack[-1], 0) >= precedence[token]):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            raise ValueError(f"Invalid token: {token}")

    c_a("mov r"+str(i)+",r13")
    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Mismatched parentheses in expression")
        output.append(operator_stack.pop())

    return " ".join(output2)+' '.join(output) #returns RPN of the inputted expression or expressionlet

def if_logic(line):
  print("fuck")
