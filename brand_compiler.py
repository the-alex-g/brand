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


def get_module_name():
    available_modules = get_available_modules()

    print("The following brand modules are available:", comma_separate(available_modules))

    while True:
        module_name = input("Enter the desired module: ")
        if module_name in available_modules or module_name == "all":
            return module_name
        elif module_name == "":
            print("compiling core module")
            return module_name
        else:
            print("That is not a valid module name.")



def compile(module_name="", file_name="brand"):
    if module_name == "":
        module_name = get_module_name()
    if module_name == "all":
        for module in get_available_modules():
            compile(module_name=module, file_name="brand_" + module)
        return

    modules_to_compile = ["core"]
    if module_name != "core":
        modules_to_compile.append(module_name)

    brand_file = open(file_name + ".py", "w")
    # compile module imports
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "imports") + "\n")
    # add a line of empty space
    brand_file.write("\n")
    # compile module global variables
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "globals") + "\n")
    # add two empty lines
    brand_file.write("\n\n")
    # compile module bodies
    for module in modules_to_compile:
        brand_file.write(get_module_section(module, "body") + "\n\n\n")
    
    brand_file.write("# using modules: ")
    for module in modules_to_compile:
        brand_file.write(module + " " + get_module_section(module, "version"))
        if module != modules_to_compile[-1]:
            brand_file.write(", ")
    
    brand_file.close()


compile()