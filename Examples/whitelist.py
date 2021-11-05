import json
import os

''' By Raddiactive#1886 '''

n = 0
diccionario = {}

def entero(name:str):
    while n < 1:

        anime = input("\033[1;36;40m Write the anime name ❯\033[0;0m")
        
        if anime == "exit":
            break
        chapter = input("\033[1;36;40m Choose the last chapter ❯\033[0;0m")
        diccionario[anime] = int(chapter)

    with open(f".{name}.json","w") as file:
        json.dump(diccionario, file, indent=4)

def añadir(name:str):
    with open(".big_lista.json","r") as file:
        read = json.load(file)
        
    while n < 1:
        add = input("\033[1;36;40m Write the anime name ❯\033[0;0m")
        if add == "exit":
            break
        chapter = input("\033[1;36;40m Choose the last chapter ❯\033[0;0m")
        read[add] = int(chapter)
        
    with open(f".{name}.json","w") as file:
        json.dump(read, file, indent=4)
        
def customize(name:str):
    with open(".big_lista.json","r") as file:
        read = json.load(file)
        keys = list(read.keys())
        
    for anime in keys:
        select = input(f"\033[1;36;40m Do you want {anime} in the list? Y to choose, else print other word ❯\033[0;0m")
        
        if select == "Y":
            chapter = input("\033[1;36;40m Choose the last chapter ❯\033[0;0m")
            diccionario[anime] = int(chapter)
        elif select == "exit":
            break
        
    select = input("\033[1;36;40m Do you want add more animes? Choose Y if you want it, if not print other word ❯\033[0;0m")
    
    if select == "Y":
        while n < 1:
            add = input("\033[1;36;40m Write the anime name ❯\033[0;0m")
            
            if add == "exit":
                break
            chapter = input("\033[1;36;40m Choose the last chapter ❯\033[0;0m")
            diccionario[add] = 0
        
    with open(f".{name}.json","w") as file:
        json.dump(diccionario, file, indent=4)
    


def main():
    c = 0
    while c < 1:
        name = input("\033[1;36;40m Choose to big list (1) or list (2) ❯ \033[0;0m")
        if name == "1":
            c = 1
            name = "big_lista"
        elif name == "2":
            c = 1
            name = "lista"
    if os.path.exists(f".{name}.json"):
        print("\n\033[1;31;40m ❮ Choose exit in every selection to exit the loop or the program ❯ \033[0;0m")
        print("\n\033[1;36;40m 1❯ New whitelist. \033[0;0m")
        print("\033[1;36;40m 2❯ Add to existing whitelist. \033[0;0m")
        print("\033[1;36;40m 3❯ Customize existing whitelist. \033[0;0m")
        print("\033[1;36;40m Other❯ Exit. \033[0;0m")
        
        select = input("\033[1;36;40m Choose the option ❯\033[0;0m")
        
        if select == "1":
            print("\n\033[1;32;40m  ❮ New whitelist ❯ \033[0;0m\n")
            entero(name)
            
        elif select == "2":
            print("\n\033[1;32;40m ❮ Add to existing whitelist ❯ \033[0;0m\n")
            añadir(name)
            
        elif select == "3":
            print("\n\033[1;32;40m ❮ Customize existing whitelist ❯ \033[0;0m\n")
            customize(name)

    else:
        print("\n\033[1;36;40m ❮ New whitelist ❯ \033[0;0m\n")
        entero(name)
        
        
        
if __name__ == "__main__":
    main()