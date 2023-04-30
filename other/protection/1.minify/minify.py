import os
from glob import glob
from python_minifier import minify


# Get the names of all .py files in the project
py_files = [f for f in glob("**/*.py", recursive=True)]

# Dictionary to store the minified code for each file
minified_code = {}

# Minify each file and store the result
for file_path in py_files:
    with open(file_path, "r") as f:
        code = f.read()

    # Minify the code and store it in the dictionary
    minified_code[file_path] = minify(
        code,
        remove_annotations=True,
        remove_pass=True,
        remove_literal_statements=True,
        combine_imports=True,
        hoist_literals=True,
        rename_locals=True,
        rename_globals=True,
        remove_object_base=True,
        remove_asserts=True,
        remove_debug=True,
    )

# Concatenate the minified code for all the files
final_code = ""
for file_path in py_files:
    # Extract the module name from the file path
    module_name = os.path.splitext(file_path)[0].replace(os.sep, ".")

    # Replace the import statements in the code with the minified code of the imported modules
    for imported_module in minified_code:
        imported_module_name = os.path.splitext(imported_module)[0].replace(os.sep, ".")
        minified_imported_module = minified_code[imported_module]
        minified_imported_module = minified_imported_module.replace("from " + imported_module_name, "from " + imported_module_name.replace(".", "") + " as _")
        minified_imported_module = minified_imported_module.replace("import " + imported_module_name.split(".")[-1], "import " + imported_module_name.replace(".", "") + " as _")
        minified_code[imported_module] = minified_imported_module

    # Replace the import statements in the code with the minified code of the imported modules
    module_code = minified_code[file_path]
    module_code = module_code.replace("import " + module_name.split(".")[-1], "import " + module_name.replace(".", "") + " as _")
    module_code = module_code.replace("from " + module_name, "from " + module_name.replace(".", "") + " as _")
    final_code += module_code + "\n"

# Save the final code to a file
with open("minified.py", "w") as f:
    f.write(final_code)