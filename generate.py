import os
import inquirer

# Validation functions
def validate_module_name(answers,current):
    directroy_list = os.listdir()

    if current in directroy_list:
      raise inquirer.errors.ValidationError('', reason='Module already exists, enter a different name')

    return True

# TODO: Add a function that writes a jinja2 template to a file

# Genaration functions
def generateModule(generateOptions):
    main_directory = os.getcwd()

    os.mkdir(generateOptions.get("technical_name"))
    os.chdir(os.path.join(main_directory, generateOptions.get("technical_name")))

    for folder in generateOptions.get("folders"):
        os.mkdir(folder.lower())




if __name__ == "__main__":

    # TODO: Add prompts for manifest file
    prompts = [inquirer.Text('technical_name',message="Enter the name of your module", validate=validate_module_name),
            inquirer.Checkbox(
                    "folders",
                    message="Select which folders you wish to generate",
                    choices=["Models","Views","Controllers","Security","Reports"]
                ),
                inquirer.List(
                                    "advanced_options",
                                    message="Do you want to go to advanced options? (create model, controller etc. files)",
                                    choices=[("Yes", True),("No", False)]
                                ),                
    ]

    generateOptions = inquirer.prompt(prompts)  

    if generateOptions.get("advanced_options"):
        print(generateOptions.get("advanced_options"))

    generateModule(generateOptions)                         


