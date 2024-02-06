import os
import inquirer







if __name__ == "__main__":

    directroy_list = os.listdir()


    questions = [
        inquirer.Checkbox(
            "folders",
            message="What size do you need?",
            choices=["Models","Views","Controllers","Security","Reports"]
        ),
    ]

    generateOptions = inquirer.prompt(questions)

    print(generateOptions)



# while True:
#     tehnical_name = str(input("Enter the tehnical name of your module: "))

#     if tehnical_name not in directroy_list:
#         generateOptions["technical_name"] = tehnical_name  

#         while True:
#             models_answer = input("Do you want to create a Models folder (Y/N): ")
#             if models_answer.lower() == "y":
#                 generateOptions["models"] = True
#                 break
#             elif models_answer.lower() == "n":
#                 print("Skipping Models creation")
#                 generateOptions["models"] = False
#                 break
#             else:
#                 print("Please enter a valid answer Y - yes or N - no!")
#         break
#     else:
#         print("A module with this name already exists!")


def generateModule(generateOptions):
    main_directory = os.getcwd()

    os.mkdir(generateOptions.get("technical_name"))
    os.chdir(os.path.join(main_directory, generateOptions.get("technical_name")))
    if "Models" in generateOptions.get("folders") : os.mkdir('models')

