import os


def get_file_contents(path):
    lines = open(path).readlines()
    string = ""
    for line in lines:
        string += line
    return string


def comma_separate(stuff):
    string = ""
    for item in stuff:
        if string != "":
            string += ", "
        string += item
    return string


def get_module_section(module, section):
    path = os.path.join(os.getcwd(), "brand_" + module, section + ".txt")
    if os.path.isfile(path):
        return get_file_contents(path)
    return ""


def get_available_modules():
    available_modules = []
    cwd = os.getcwd()

    for item in os.listdir(cwd):
        path = os.path.join(cwd, item)
        if os.path.isdir(path):
            if item.startswith("brand_"):
                available_modules.append(item[6:])
    available_modules.sort()

    return available_modules



def compile():
    available_modules = get_available_modules()

    print("The following brand modules are available:", comma_separate(available_modules))

    module_name = ""
    while True:
        module_name = input("Enter the desired module: ")
        if module_name in available_modules:
            break
        elif module_name == "":
            print("compiling core module")
            break
        else:
            print("That is not a valid module name.")


    modules_to_compile = ["core"]
    if module_name != "core":
        modules_to_compile.append(module_name)


    brand_file = open("brand.py", "w")
    # compile module imports
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "imports"))
    # add a line of empty space
    brand_file.write("\n\n")
    # compile module global variables
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "globals"))
    # add two empty lines
    brand_file.write("\n\n\n")
    # compile module bodies
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "body"))
    
    brand_file.write("\n\n# using modules ")
    for module in modules_to_compile:
        brand_file.write(module + " " + get_module_section(module, "version"))
        if module != modules_to_compile[-1]:
            brand_file.write(", ")


compile()