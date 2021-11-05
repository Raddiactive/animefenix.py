import animefenix as fenix
import json
import os
import requests
import sys

''' By Raddiactive#1886 '''

def main(username:str, password:str):
    client = fenix.Client()
    client.login(username=username,password=password,remember="Yes")
    i=0
    c = 0
    add = {}
    exit = False
    if os.path.exists(".big_lista_links.json") == True:
        with open(".big_lista_links.json","r") as file:
            dowload = json.loads(file.read())
    else:
        dowload = {}
        
    with open(".big_lista.json","r") as animes:
        animes = json.loads(animes.read())
        lista_keys = list(animes.keys())
        lista_values = list(animes.values())

    for name in lista_keys:

        print(f"\n\033[1;36;40m ❮ {name} ❯ \033[0;0m")
        chapter = lista_values[c]
        cap = client.anime_last_chapter(name)
        
        if chapter != cap:
            while chapter <= cap:
                if exit == False:   
                    urls = client.download_links(name,chapter)
                    print(f"\n\033[1;36;40m Here is the dowload links from chapter {chapter} ❯ \033[0;0m")
                    
                    try:
                        values = urls.values()
                        keys = urls.keys()
                        for i,url in enumerate (values):
                            response = requests.get(url).status_code
                            if response == 200:
                                color = "\033[1;32;40m"
                                link_color = "\033[0;30;47m"

                            else:
                                color = "\033[1;31;40m"
                                link_color = "\033[0;37;40m"

                            server = list(keys)[i]
                            i += 1
                            print(f"\n\033[0;30;46m ❮ {server} ❯ \033[0;0m " + f"{link_color} {url} \033[0;0m" + f" {color} RESPONSE ❯ {response} \033[0;0m")
                        
                        option = input("\n\033[1;36;40m Choose the option ❯\033[0;0m ")
                        
                        if option != "0" and option != "e" and option != "n":
                            if  int(option) < len(list(keys)):
                                url = (list(values)[int(option)-1])
                                add[f" {chapter} -> {[list(keys)[int(option)-1]]} "] = url
                                dowload[name] = add               
                                animes[name] = chapter
                                
                                with open(".big_lista.json","w") as new:
                                    json.dump(animes, new, indent=4)
                                    
                                with open(".big_lista_links.json","w") as new:
                                    json.dump(dowload, new, indent=4)

                                
                        elif option == "n":
                            break
                        elif option == "e":
                            exit = True
                        chapter += 1
                        
                    except:
                        chapter += 1
                else:
                    print("\n\033[1;32;40m ❮ Successfully completed, no more animes to download! ❯ \033[0;0m\n")
                    sys.exit(0)            
            c += 1
        
            
    print("\n\033[1;32;40m ❮ Successfully completed, no more animes to download! ❯ \033[0;0m\n")
    
if __name__ == '__main__':
    if os.path.exists(".config.json") != True:
        user = input("\n\033[1;36;40m Write the username ❯\033[0;0m ")
        password = input("\033[1;36;40m Write the password ❯\033[0;0m ")
        data = {"user":user, "pass":password}

        with open('.config.json','w') as file:
            json.dump(data, file, indent=4)

    with open('.config.json','r') as file:
        config = json.load(file)
        username = config["user"]
        password = config["pass"]
        
    main(username,password)
    