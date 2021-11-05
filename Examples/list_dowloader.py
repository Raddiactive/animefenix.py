import animefenix as fenix
import json
import os
import requests
import sys
import webbrowser

''' By Raddiactive#1886 '''

def main(username:str, password:str):
    client = fenix.Client()
    client.login(username=username,password=password,remember="Yes")
    c = 0
    exit = False
    with open(".lista.json","r") as animes:
        animes = json.loads(animes.read())
        lista_keys = list(animes.keys())
        lista_values = list(animes.values())    
    for name in lista_keys:
        if exit == False:
            chapter = lista_values[c]
            cap = client.anime_last_chapter(name)
            while chapter <= cap:
                urls = client.download_links(name,cap)
                print(f"\n\033[1;36;40m There is a new chapter of {name}! Here is the dowload links from chapter {chapter} ❯ \033[0;0m")
                try:
                    values = urls.values()
                    keys = urls.keys()
                    for i, url in enumerate (values):
                        response = requests.get(url).status_code
                        if response == 200:
                            color = "\033[1;32;40m"
                            link_color = "\033[0;30;47m"
                        else:
                            color = "\033[1;31;40m"
                            link_color = "\033[0;37;40m"
                        server = list(keys)[i]
                        print(f"\n\033[0;30;46m ❮ {server} ❯ \033[0;0m " + f"{link_color} {url} \033[0;0m" + f" {color} RESPONSE ❯ {response} \033[0;0m")
                    option = input("\n\033[1;36;40m Choose the option ❯\033[0;0m ")
                    if option != "0" and option != "n" and option != "e":
                        if int(option) < len(list(keys)):
                            url = (list(values)[int(option)-1])
                            animes[name] = chapter
                            with open(".lista.json","w") as new:
                                json.dump(animes, new, indent=4)
                            webbrowser.get('google-chrome %s --incognito').open_new(url)        
                    elif option == "n":
                        break 
                    elif option == "e":
                        exit = True
                    chapter += 1   
                except:
                    chapter += 1
            c += 1
        else:
            print("\n\033[1;32;40m ❮ Successfully completed, no more animes to download! ❯ \033[0;0m\n")
            sys.exit(0)
            
if __name__ == '__main__':
    if os.path.exists(".config.json") != True:
        user = input("\n\033[1;36;40m Write the username ❯\033[0;0m ")
        password = input("\033[1;36;40m Write the password ❯\033[0;0m ")
        data = {"user": user, "pass": password}
        with open('.config.json','w') as file:
            json.dump(data, file, indent=4)
    with open('.config.json','r') as file:
        config = json.load(file)
        username = config["user"]
        password = config["pass"]
        
    main(username, password)
    
    