import os

tehnical_name = str(input("Enter the tehnical name of your module: "))
directroy_list = os.listdir()
main_directory = os.getcwd()

if tehnical_name not in directroy_list:
    os.mkdir(f"{tehnical_name}")
    os.chdir(f"{main_directory}\{tehnical_name}")
    
    while True:
        models_answer = input("Do you want to create a Models folder (Y/N): ")

        if models_answer.lower() == "y":
            os.mkdir("models")
            break
        elif models_answer.lower() == "n":
            print("Skipping Models creation")
            break
        else:
            print("Please enter a valid answer Y - yes or N - no!")
else:
    print("A module with this name already exists!")


