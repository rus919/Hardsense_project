import ast
import os
import secrets
import string

def random_string(length=10):
    return ''.join(secrets.choice(string.ascii_lowercase) for _ in range(length))

def rename_functions(node):
    if isinstance(node, ast.FunctionDef):
        node.name = random_string()

def process_file(filepath):
    with open(filepath, 'r') as f:
        contents = f.read()
        tree = ast.parse(contents)

        for node in ast.walk(tree):
            rename_functions(node)

        return tree

def main():
    file_path = 'minified.py'

    combined_ast = process_file(file_path)

    modified_code = ast.unparse(combined_ast)
    with open('output.py', 'w') as f:
        f.write(modified_code)

if __name__ == '__main__':
    main()