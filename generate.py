import os
import inquirer

from jinja2 import Environment, PackageLoader


def enterAddonsDir():
    directroy_list = os.listdir()

    if "addons" not in directroy_list:
        os.mkdir("addons")

    main_directory = os.getcwd()
    os.chdir(os.path.join(main_directory, "addons"))


def validate_module_name(answers, current):

    directroy_list = os.listdir()

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
    }
    output_content = manifest_template.render(**manifest_options)

    with open("__manifest__.py", "w") as file:
        file.write(output_content)

    for folder in generateOptions.get("folders"):
        os.mkdir(folder.lower())


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

    if generateOptions.get("advanced_options"):
        print(generateOptions.get("advanced_options"))

    generateModule(generateOptions, env)
