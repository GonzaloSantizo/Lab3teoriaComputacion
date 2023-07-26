# Define the precedence of operators
precedence = {
    '|': 1,
    '*': 2,
    '?': 2,  # Lower precedence than '*' and '|'
    '(': 3,
    ')': 4,
    '+': 5,
}

# Update get_precedence function
def get_precedence(char):
    return precedence.get(char, 0)




class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_operator(char):
    return char in {'*', '?', '+', 'a', 'b', '|'}



def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        if expression[i].isalnum():
            token = ""
            while i < len(expression) and expression[i].isalnum():
                token += expression[i]
                i += 1
            tokens.append(token)
        elif expression[i] in {'*', '?', '+', '|', '(', ')'}:
            tokens.append(expression[i])
            i += 1
        else:
            i += 1
    return tokens

def shunting_yard(expression):
    def remove_spaces(expression):
        return "".join(expression.split())

    output_queue = []
    operator_stack = []

    expression = remove_spaces(expression)
    tokens = tokenize(expression)

    for idx, token in enumerate(tokens):
        if token.isalnum():
            output_queue.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  # Remove '(' from the stack
        elif is_operator(token):
            if token in {'*', '?', '+'}:
                # Convert the unary operator to a separate token
                prev_token = tokens[idx - 1] if idx > 0 else None
                if prev_token is None or prev_token in {'(', '|', '?', '*'}:
                    output_queue.append(f"u_{token}")
                else:
                    output_queue.append(token)
            else:
                while operator_stack and is_operator(operator_stack[-1]) and get_precedence(operator_stack[-1]) >= get_precedence(token):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue



def create_ast(postfix_expression):
    stack = []

    for token in postfix_expression:
        if token.isalnum():
            stack.append(Node(token))
        elif token.startswith('u_'):
            # Handle unary operator token
            operator = token[2:]  # Get the operator symbol without the 'u_' prefix
            if not stack:
                raise ValueError("Error: Insufficient operands for operator")
            operand = stack.pop()
            node = Node(f"{operand.value}{operator}")  # Combine operand with the operator
            node.left = operand
            stack.append(node)
        elif token in {'|', '*', '?', '+'}:
            if token in {'*', '?', '+'}:
                # Handle unary operator token
                if not stack:
                    raise ValueError("Error: Insufficient operands for operator")
                operand = stack.pop()
                node = Node(f"{operand.value}{token}")
                node.left = operand
            else:
                # Handle binary operator token
                if len(stack) < 2:
                    raise ValueError("Error: Insufficient operands for operator")
                right_node = stack.pop()
                left_node = stack.pop()
                node = Node(token)
                node.left = left_node
                node.right = right_node
            stack.append(node)
        else:
            raise ValueError(f"Error: Unknown token '{token}'")

    if len(stack) != 1:
        raise ValueError("Error: Too many operands")

    return stack[0]


def inorder_traversal(node):
    if node:
        inorder_traversal(node.left)
        print(node.value, end=" ")
        inorder_traversal(node.right)


def process_expressions(expressions):
    for idx, expression in enumerate(expressions, 1):
        print(f"Expression {idx}: {expression}")
        postfix_expression = shunting_yard(expression)
        print("Postfix:", " ".join(postfix_expression))
        try:
            ast_root = create_ast(postfix_expression)
            print("\nAbstract Syntax Tree:")
            inorder_traversal(ast_root)
        except ValueError as e:
            print(e)
        print("\n")


def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        expressions = [line.strip() for line in file]
    return expressions

if __name__ == "__main__":
    input_file = "dataEjercicio1.txt"
    input_expressions = read_input_file(input_file)
    process_expressions(input_expressions)