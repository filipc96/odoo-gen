import os



directroy_list = os.listdir()
main_directory = os.getcwd()

generateOptions = {}



while True:
    tehnical_name = str(input("Enter the tehnical name of your module: "))

    if tehnical_name not in directroy_list:
        generateOptions["technical_name"] = tehnical_name 

        while True:
            models_answer = input("Do you want to create a Models folder (Y/N): ")
            if models_answer.lower() == "y":
                generateOptions["models"] = True
                break
            elif models_answer.lower() == "n":
                print("Skipping Models creation")
                generateOptions["models"] = False
                break
            else:
                print("Please enter a valid answer Y - yes or N - no!")
        break
    else:
        print("A module with this name already exists!")


os.mkdir(generateOptions.get("technical_name"))
os.chdir(os.path.join(main_directory, generateOptions.get("technical_name")))
if generateOptions["models"] : os.mkdir("models")
