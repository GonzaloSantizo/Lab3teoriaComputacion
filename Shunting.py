# Define operator precedence dictionary
precedence = {
    '(': 1,
    '|': 2,
    '.': 3,
    '?': 4,
    '*': 4,
    '+': 4,
    '^': 5
}

# Function to perform the Shunting Yard algorithm
def shunting_yard(expression):
    output_queue = []
    operator_stack = []

    # Function to check precedence of operators
    def has_higher_precedence(op1, op2):
        return precedence[op1] >= precedence[op2]

    # Function to process operators in the operator stack
    def process_operator_stack(token):
        while operator_stack and operator_stack[-1] != '(' and has_higher_precedence(operator_stack[-1], token):
            output_queue.append(operator_stack.pop())
        operator_stack.append(token)

    # Read the input expression token by token
    for token in expression:
        if token.isdigit():
            output_queue.append(token)
        elif token in precedence:
            process_operator_stack(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()

    # Process any remaining operators in the stack
    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


file_path = "./dataEjercicio3.txt"  # Path to the text file
# Read the lines from the data.txt file
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Apply the Shunting Yard algorithm to each line
for line in lines:
    line = line.strip()
    postfix_expression = shunting_yard(line)
    print("Infix:", line)
    print("Postfix:", ' '.join(postfix_expression))
    print()

