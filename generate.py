import os
import inquirer
import re

from jinja2 import Environment, PackageLoader


def enter_addons_dir():
    directroy_list = os.listdir()

    if "addons" not in directroy_list:
        os.mkdir("addons")

    main_directory = os.getcwd()
    os.chdir(os.path.join(main_directory, "addons"))


# Validation functions
def validate_file_name(answers, current):

    pattern = re.compile(r"^[a-zA-Z0-9_]+$")
    return bool(pattern.match(current))


def validate_module_name(answers, current):

    directroy_list = os.listdir()

    if not validate_file_name(answers, current):
        raise inquirer.errors.ValidationError(
            "",
            reason="Invalid name: Whitespaces and symbols are not allowed except '_'",
        )

    if current in directroy_list:
        raise inquirer.errors.ValidationError(
            "", reason="Module already exists, enter a different name"
        )

    return True


# Genaration functions
def generate_files(file_list, type):

    env = Environment(loader=PackageLoader("generate"))

    match type:
        case "models":
            file_template = env.get_template("model_template.py.jinja2")
        case "controllers":
            file_template = env.get_template("controller_template.py.jinja2")

    os.chdir(type)
    for file in file_list:
        class_name = "".join(word.capitalize() for word in file.split("_"))

        file_options = {"class_name": class_name, "name": file}
        output_content = file_template.render(**file_options)

        with open(f"{file}.py", "w") as file:
            file.write(output_content)
    os.chdir("..")


def generate_module(generate_options, advanced_options):

    env = Environment(loader=PackageLoader("generate"))
    manifest_template = env.get_template("manifest_template.py.jinja2")
    current_directory = os.getcwd()

    os.mkdir(generate_options.get("technical_name"))
    os.chdir(os.path.join(current_directory, generate_options.get("technical_name")))

    manifest_options = {
        "module_name": generate_options.get("name"),
        "module_version": generate_options.get("version"),
        "module_author": generate_options.get("author"),
        "module_license": generate_options.get("license"),
    }
    output_content = manifest_template.render(**manifest_options)

    with open("__manifest__.py", "w") as file:
        file.write(output_content)

    for folder in generate_options.get("folders"):
        os.mkdir(folder.lower())

        if folder.lower() in ["models", "controllers", "reports"]:
            init_file_path = os.path.join(folder.lower(), "__init__.py")

            with open(init_file_path, "w") as file:
                file.write("")

    if generate_options.get("advanced_options"):

        if "Models" in generate_options.get("folders"):
            generate_files(advanced_options.get("models"), "models")

        if "Controllers" in generate_options.get("folders"):
            generate_files(advanced_options.get("controllers"), "controllers")

    with open("__init__.py", "w") as file:
        filtered_folders = filter(
            lambda item: item.lower() in ["models", "controllers", "reports"],
            generate_options.get("folders"),
        )
        imports = ", ".join(filtered_folders).lower()
        file.write(f"from . import {imports}")


def get_advanced_values(type):
    answers = []
    state = inquirer.prompt(
        [inquirer.Confirm("confirm", message=f"Would you like to create a {type}")]
    )

    while state.get("confirm"):
        prompt = inquirer.prompt(
            [
                inquirer.Text(
                    "name",
                    message=f"Enter {type} name",
                    validate=validate_file_name,
                )
            ]
        )
        answers.append(prompt.get("name"))

        state = inquirer.prompt(
            [
                inquirer.Confirm(
                    "confirm",
                    message=f"Would you like to create a {type}",
                )
            ]
        )

    return answers


def main():
    enter_addons_dir()

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

    generate_options = inquirer.prompt(prompts)
    advanced_options = None

    # TODO: Add advanced options - generate model, controller, menu, view
    if generate_options.get("advanced_options"):
        models = (
            get_advanced_values("model")
            if "Models" in generate_options.get("folders")
            else None
        )
        controllers = (
            get_advanced_values("controllers")
            if "Controllers" in generate_options.get("folders")
            else None
        )
        advanced_options = {"models": models, "controllers": controllers}

    generate_module(generate_options, advanced_options)


if __name__ == "__main__":
    main()
