import os

tehnical_name = str(input("Enter the tehnical name of your module: "))
directroy_list = os.listdir()





if tehnical_name not in directroy_list:
    os.mkdir(f"{tehnical_name}")
else:
    print("A module with this name already exists!")


