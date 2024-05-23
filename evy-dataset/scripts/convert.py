import ast
import os
import subprocess
import tempfile
import astunparse
import pyrefact
from pyrefact import pattern_matching

scope = None

def translate_assign(node):
    targets = [translate_ast_node(target) for target in node.targets]
    if isinstance(node.value, ast.IfExp):
        code = " ".join(targets) + " := " + "None"
        return translate_ifexp_statement(node.value)
    value = translate_ast_node(node.value)
    assignOp = " = "
    for target in targets:
        if target not in scope:
            assignOp = " := "
            scope.add(target)
    return " ".join(targets) + assignOp + value + "\n"


def translate_subscript(node):
    """
    Translate a subscript node into a Python expression.

    :param node: An AST node representing a subscript expression
    :return: A Python expression as a string
    """
    # Get the node's children (the value and slice expressions)
    value, slice = node.value, node.slice

    # Recursively translate the value and slice expressions
    value_expr = translate_ast_node(value)
    slice_expr = translate_ast_node(slice)

    # Construct the subscript expression as a string
    return f"{value_expr}{slice_expr}"


def translate_slice(node):
    """Translate an ast.Slice node into Evy slice notation."""
    lower = translate_ast_node(node.lower) if node.lower else "0"  # Default to start
    upper = translate_ast_node(node.upper) if node.upper else ""  # Empty means to the end
    step = translate_ast_node(node.step) if node.step else ""

    # Handle potential empty elements if Evy's syntax allows it
    return f"[{lower}:{upper}]"  # Assuming Evy uses a similar notation


def translate_unary_operation(node):
    operand = translate_ast_node(node.operand)
    operator = translate_operator(node.op)
    EvyUnaryOpMapping = {
        ast.UAdd: "+",  # Unary plus (likely redundant)
        ast.USub: "-",  # Unary minus
        ast.Not: "!"  # Assuming Evy uses 'not'
    }

    # Use prefix notation for unary operators if Evy requires it
    if isinstance(EvyUnaryOpMapping, dict):
        return EvyUnaryOpMapping[type(node.op)] + operand
    else:
        return operator + operand  # Assuming Evy also accepts unary operators before the operand


def translate_name(name):
    keywords = {
        "func",
        "end",
        "on",
        "num",
        "string",
        "on",
        "input",
        "key",
    }
    return name + "_" if name in keywords else name



def translate_ast_node(node):
    """Recursively translates an AST node"""
    val = translate_operator(node)
    if val != None:
        return val
    elif isinstance(node, ast.Name):  # Variable names
        return translate_name(node.id)
    elif isinstance(node, ast.BinOp):  # Binary operations (+, -, *, etc.)
        return translate_binary_operation(node)
    elif isinstance(node, ast.UnaryOp):  # Binary operations (+, -, *, etc.)
        return translate_unary_operation(node)
    elif isinstance(node, ast.Compare):  # Comparisons (>, <, ==, etc.)
        return translate_comparison(node)
    elif isinstance(node, ast.BoolOp):  # Boolean operations (and, or, not)
        return translate_boolean_operation(node)
    elif isinstance(node, ast.Constant):  # Boolean operations (and, or, not)
        return translate_constant(node)
    elif isinstance(node, ast.Call):  # Function calls
        return translate_function_call(node)
    elif isinstance(node, ast.FunctionDef):
        return translate_function_def(node)
    elif isinstance(node, ast.If):
        return translate_if_statement(node)
    elif isinstance(node, ast.IfExp):
        return translate_ifexp_statement(node)
    elif isinstance(node, ast.Expr):
        return translate_ast_node(node.value)
    elif isinstance(node, ast.Module):
        return "".join([translate_ast_node(x) for x in node.body])
    elif isinstance(node, ast.Assign):
        return translate_assign(node)
    elif isinstance(node, ast.Subscript):
        return translate_subscript(node)
    elif isinstance(node, ast.Slice):
        return translate_slice(node)

    else:
        raise NotImplementedError(f"Translation for {type(node)} not supported yet")

def translate_function_def(node):
    evy_code = "func " + node.name   # Start the Evy function

    # Parameters
    params = []
    for arg in node.args.args:
        params.append(arg.arg + ":num")  # Assuming all parameters are numeric for now
    evy_code += "(" + ", ".join(params) + ") "

    # Return Type (if specified in Python)
    if node.returns:
        return_type = translate_ast_node(node.returns)  # Recurse to handle the type
        evy_code += ":" + return_type + " "

    # Function Body
    body_statements = [translate_ast_node(child_node) for child_node in node.body]
    evy_code += "\n" + "\n".join(body_statements) + "\nend"

    return evy_code

def translate_if_statement(node):
    evy_code = "if " + translate_ast_node(node.test) + "\n"

    # Body of 'if'
    for child_node in node.body:
        evy_code += "    " + translate_ast_node(child_node)

    # 'else if' clauses
    for elif_clause in node.orelse:
        evy_code += "else if " + translate_ast_node(elif_clause.test) + "\n"
        for child_node in elif_clause.body:
            evy_code += translate_ast_node(child_node) + "\n"

    # 'else' clause
    if node.orelse:
        evy_code += "else\n"
        for child_node in node.orelse:
            evy_code += translate_ast_node(child_node) + "\n"

    evy_code += "end"  # Assuming 'end' marks the end of the if block
    return evy_code

def translate_ifexp_statement(node):
    # ast.Assign
    # ifExp
    evy_code = "if " + translate_ast_node(node.test) + "\n"

    # Body of 'if'
    evy_code += "    " + translate_ast_node(node.body.left) +" = " + translate_ast_node(node.body) + "\n"

    # 'else if' clauses
    if node.orelse:
        evy_code += "else \n    " + translate_ast_node(node.orelse) + "\n"
        evy_code += "end"  # Assuming 'end' marks the end of the if block
    return evy_code

# def translate_ifexp_statement(node):
#     evy_code = "if " + translate_ast_node(node.test) + "\n"
#
#     # Body of 'if'
#     evy_code += "    " + translate_ast_node(node.body)
#
#     # 'else if' clauses
#     if node.orelse:
#         evy_code += "else if " + translate_ast_node(node.test) + "\n"
#         evy_code += translate_ast_node(node.orelse.body) + "\n"
#         evy_code += "end"  # Assuming 'end' marks the end of the if block
#     return evy_code


def translate_constant(node):
    if isinstance(node.value, bool):  # Booleans
        return "true" if node.value else "false"
    elif isinstance(node.value, (int, float)):  # Numbers
        return str(node.value)
    elif isinstance(node.value, str): # String
        return '"' + node.value + '"'  # Add quotes assuming Evy uses them

    # Handle other constant types if needed (None, complex numbers, etc.)
    else:
        raise NotImplementedError(f"Translation for constant type {type(node.value)} is not supported yet")



# def translate_expression(node):
#     # ... add cases if needed
#
#     else:
#         raise NotImplementedError(f"Translation for expression type {type(node)} not supported yet")

def translate_operator(operator):
    operator_mappings = {
        ast.Add: "+",
        ast.Sub: "-",
        ast.Mult: "*",
        ast.Div: "/",
        ast.Eq: "==",
        ast.NotEq: "!=",
        ast.Lt: "<",
        ast.Gt: ">",
        ast.LtE: "<=",
        ast.GtE: ">=",
        ast.And: "and",
        ast.Or: "or",
        ast.Mod: "%",
    }

    if type(operator) in operator_mappings:
        return operator_mappings[type(operator)]
    else:
        return None


def translate_binary_operation(node):
    left = translate_comparison(node.left)
    right = translate_comparison(node.right)
    operator = translate_operator(node.op)
    return left + " " + operator + " " + right


def translate_binary_operation(node):
    left = translate_ast_node(node.left)
    right = translate_ast_node(node.right)
    operator = translate_operator(node.op)
    return left + " " + operator + " " + right

def translate_comparison(node):
    left = translate_ast_node(node.left)
    right = translate_ast_node(node.comparators[0])
    operator = translate_ast_node(node.ops[0])
    return left + " " + operator + " " + right

def translate_boolean_operation(node):
    parts = [translate_ast_node(value) for value in node.values]
    operator = translate_ast_node(node.op)
    return " ".join(parts) + " " + operator

def translate_function_call(node):
    function_name = node.func.id
    args = [translate_ast_node(arg) for arg in node.args]
    return function_name + "(" + ", ".join(args) + ")"


def translate_python_code(python_code):
    """Translates a Python code snippet into Evy"""
    global scope
    scope = set()
    tree = ast.parse(python_code)

    # Check if it's a module node and translate its body
    if isinstance(tree, ast.Module):
        return translate_ast_node(tree)
    # Raise an error if it's not a module
    else:
        raise NotImplementedError(f"Input must be Python code as a string")

def run_from_string(command, code_string, filename="tmp_script.py"):
    """Executes 'evy run' on code provided as a string.

    Args:
        code_string (str): The Python code to execute.
        filename (str, optional): Name of the temporary file.
                                  Defaults to "tmp_script.py".

    Returns:
        tuple: A tuple containing (stdout, stderr) from the evy command.
    """

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = os.path.join(tmp_dir, filename)

        with open(tmp_file_path, 'w') as f:
            f.write(code_string)

        command = f"{command} {tmp_file_path}"

        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return None, e.stderr


import ast
from pyrefact import pattern_matching

code = """
total = price * 1.15 if in_province else price  # Include tax if in province
"""


from pyrefact import pattern_matching

pattern = """
result = (___) if (___) else (___) 
"""

replacement = """
if (___):
    result = (___) 
else:
    result = (___) 
"""

def transform_ternary(code):
    for match in pattern_matching.finditer(pattern, code):
        condition, on_true, on_false = match.groups()
        new_code = replacement.replace('___', condition).replace('___', on_true).replace('___', on_false)
        code = code.replace(match.source, new_code)
    return code

new_code = transform_ternary(code)
print(new_code)



if __name__ == "__main__":
    # Example Usage
    python_snippets = ["""
a = False
if "a" == "b":
    a = "a" == "b"
""",
"""print("Hello, World!")""",
# """CODE""",
"""celsius = 37
fahrenheit = (celsius * 9/5) + 32
print(fahrenheit)
""",
"""string = "radar"
print(string == string[::-1])
""",
"""num1 = 5
num2 = 10
print(num1 + num2)
""",
"""string = "Hello"
print(len(string))
""",
"""num = 4
print(num % 2 == 0)
""",
"""string = "Hello"
print(string[::-1])
""",

                       """def custom_slice(obj, start, stop, step=1):
    obj_len = len(obj)

    # Adjust indices to handle negative values
    start = start + obj_len if start < 0 else start
    stop = stop + obj_len if stop < 0 else stop

    # Ensure indices are within bounds
    start = max(0, min(start, obj_len))
    stop = max(0, min(stop, obj_len))

    # Handle negative step
    if step < 0:
        start, stop = stop - 1, start -1 

    # Calculate indices and build result with appropriate direction
    result = [] 
    if step > 0: 
        for i in range(start, stop, step):
            result.append(obj[i])
    else:
        for i in range(start, stop, step):
            result.append(obj[i])        
        result.reverse()

    return result 
                       """



                       ]
    translated = []
    for snippet in python_snippets[-1:]:
        if 'string = "Hello"' in snippet:
            pass
        print("Python code:\n", snippet)

        snippet = transform_ternary(snippet)
        snippet = pyrefact.format_code(snippet, preserve=set(["custom_slice"]))
        print("Simplified Python code:\n", snippet)
        val, err = run_from_string("python", snippet)
        if val is None: print("Python error:", err)
        print("Python output:\n", val)
        evy_code = translate_python_code(snippet)
        val, err = run_from_string("evy run", evy_code)
        print("Evy code:\n")
        print(evy_code)
        if val is None: print("Evy error:", err)
        print("Evy output:\n", val)
    print(translated)


