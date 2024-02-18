import os
import inquirer
import re

from jinja2 import Environment, PackageLoader


def enterAddonsDir():
    directroy_list = os.listdir()

    if "addons" not in directroy_list:
        os.mkdir("addons")

    main_directory = os.getcwd()
    os.chdir(os.path.join(main_directory, "addons"))


def validate_module_name(answers, current):

    directroy_list = os.listdir()

    pattern = re.compile(r"^[a-zA-Z0-9_-]+$")

    is_match = bool(pattern.match(current))

    if not is_match:
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid name: Whitespaces and symbols that are not '_' or '-' are not allowed",
        )

    if current in directroy_list:
        raise inquirer.errors.ValidationError(
            "", reason="Module already exists, enter a different name"
        )

    return True


# Genaration functions
def generateModule(generateOptions, env):

    manifest_template = env.get_template("manifest_template.py.jinja2")

    current_directory = os.getcwd()

    os.mkdir(generateOptions.get("technical_name"))
    os.chdir(os.path.join(current_directory, generateOptions.get("technical_name")))

    manifest_options = {
        "module_name": generateOptions.get("name"),
        "module_version": generateOptions.get("author"),
        "module_author": generateOptions.get("version"),
        "module_license": generateOptions.get("license"),
    }
    output_content = manifest_template.render(**manifest_options)

    with open("__manifest__.py", "w") as file:
        file.write(output_content)

    for folder in generateOptions.get("folders"):
        os.mkdir(folder.lower())

        if folder.lower() in ["models", "controllers", "reports"]:
            init_file_path = os.path.join(folder.lower(), "__init__.py")

            with open(init_file_path, "w") as file:
                file.write("")

    with open("__init__.py", "w") as file:
        filtered_folders = filter(
            lambda item: item.lower() in ["models", "controllers", "reports"],
            generateOptions.get("folders"),
        )
        imports = ", ".join(filtered_folders).lower()
        file.write(f"from . import {imports}")


def get_advanced_values(type):
    answers = []
    state = inquirer.prompt(
        [inquirer.Confirm("confirm", message=f"Would you like to create a {type}")]
    )

    while state.get("confirm"):
        prompt = inquirer.prompt([inquirer.Text("name", message=f"Enter {type} name")])
        answers.append(prompt.get("name"))

        state = inquirer.prompt(
            [inquirer.Confirm("confirm", message=f"Would you like to create a {type}")]
        )

    return answers


if __name__ == "__main__":

    env = Environment(loader=PackageLoader("generate"))

    enterAddonsDir()

    # TODO: Add more prompts for manifest file
    prompts = [
        inquirer.Text(
            "technical_name",
            message="Enter the technical name of your module",
            validate=validate_module_name,
        ),
        inquirer.Text(
            "name",
            message="Enter the name of your module",
        ),
        inquirer.Text(
            "author",
            message="Enter your name (or company)",
        ),
        inquirer.Text(
            "version",
            message="Enter version",
        ),
        inquirer.List(
            "license",
            message="Choose a license for your module",
            choices=[
                "GPL-2",
                "GPL-2 or any later version",
                "GPL-3",
                "GPL-3 or any later version",
                "AGPL-3",
                "LGPL-3",
                "Other OSI approved licence",
                "OEEL-1",
                "OPL-1",
                "Other proprietary",
            ],
        ),
        inquirer.Checkbox(
            "folders",
            message="Select which folders you wish to generate",
            choices=["Models", "Views", "Controllers", "Security", "Reports"],
        ),
        inquirer.List(
            "advanced_options",
            message="Do you want to go to advanced options? (create model, controller etc. files)",
            choices=[("Yes", True), ("No", False)],
        ),
    ]

    generateOptions = inquirer.prompt(prompts)
    advanced_options = None

    # TODO: Add advanced options - generate model, controller, menu, view
    if generateOptions.get("advanced_options"):
        models = get_advanced_values("model")
        controllers = get_advanced_values("controllers")
        advanced_options = {"models": models, "controllers": controllers}
        print(advanced_options)

    generateModule(generateOptions, env)
