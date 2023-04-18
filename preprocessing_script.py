import re

names_list = []

with open("town_names.txt", "r") as file:
    for line in file:
        name = re.split('[0-9]', line)[0].rstrip()
        print(name)
        names_list.append(name)

with open("town_names.txt", "w") as file:
    for name in names_list:
        file.write(name + "\n")