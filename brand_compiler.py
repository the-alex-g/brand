import os


class ReplacementLine:
    name = ""
    text = ""

    def __init__(self, string):
        for char in string:
            if char == " ":
                break
            self.name += char
        self.text = string


def get_file_contents(path):
    lines = open(path).readlines()
    string = ""
    for line in lines:
        string += line
    return string


def separate(stuff, spacer):
    string = ""
    for item in stuff:
        if string != "":
            string += spacer
        string += item
    return string


def get_module_lines(module, section):
    path = os.path.join(os.getcwd(), "brand_" + module, section + ".txt")
    if os.path.isfile(path):
        return open(path).readlines()
    return []


def get_module_section(module, section):
    return separate(get_module_lines(module, section), "")


def get_module_value_assignments(module):
    replacement_lines = []
    for line in get_module_lines(module, "new_values"):
        replacement_lines.append(ReplacementLine(line))
    return replacement_lines


def get_module_section_with_replacements(module, section, replacements):
    section_text = ""
    for line in get_module_lines(module, section):
        was_replaced = False
        for replacement in replacements:
            if line.startswith(replacement.name):
                if section_text != "":
                    section_text += "\n"
                section_text += replacement.text
                was_replaced = True
                break
        if not was_replaced:
            section_text += line
    return section_text


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

    print("The following brand modules are available:", separate(available_modules, ", "))

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
    
    value_assignments = []
    for module in modules_to_compile:
        for assignment in get_module_value_assignments(module):
            value_assignments.append(assignment)

    brand_file = open(file_name + ".py", "w")

    # get version information
    brand_file.write("# BRAND CORE v.")
    brand_file.write(get_module_section("core", "version"))
    if module_name != "core":
        brand_file.write("\n# additional module: " + module_name + " v." + get_module_section(module_name, "version") + "\n")
    
    # compile module imports
    for module in modules_to_compile:
        brand_file.write("\n" + get_module_section(module, "imports"))
    # compile module global variables
    for module in modules_to_compile:
        brand_file.write("\n" + get_module_section_with_replacements(module, "globals", value_assignments))
    # compile module bodies
    for module in modules_to_compile:
        brand_file.write("\n\n\n" + get_module_section(module, "body"))
    
    brand_file.close()


compile()