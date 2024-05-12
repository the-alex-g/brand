import os


def get_file_contents(filename):
    lines = open(filename).readlines()
    string = ""
    for line in lines:
        string += line
    return string


def compile():
    available_modules = []

    cwd = os.getcwd()
    for item in os.listdir(cwd):
        path = os.path.join(cwd, item)
        if os.path.isdir(path):
            if item.startswith("brand_"):
                available_modules.append(item[6:])
    available_modules.sort()

    module_string = ""
    for module in available_modules:
        if module_string != "":
            module_string += ", "
        module_string += module

    print("The following brand modules are available:", module_string)

    module_name = ""
    while True:
        module_name = input("Enter the desired module: ")
        if module_name in available_modules:
            break
        else:
            print("That is not a valid module name.")


    modules_to_compile = ["core"]
    if module_name != "core":
        modules_to_compile.append(module_name)


    brand_file = open("brand.py", "w")
    for module in modules_to_compile:
        brand_file.write(get_file_contents(os.path.join(cwd, "brand_" + module, "imports.txt")))
    brand_file.write("\n\n")
    for module in modules_to_compile:
        brand_file.write(get_file_contents(os.path.join(cwd, "brand_" + module, "consts.txt")))
    brand_file.write("\n\n\n")
    for module in modules_to_compile:
        brand_file.write(get_file_contents(os.path.join(cwd, "brand_" + module, "body.txt")))


compile()