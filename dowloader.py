import animefenix as fenix
import json
import os
import requests
import webbrowser

''' By Raddiactive#1886 '''

def main(username:str, password:str):
    client = fenix.Client()
    name = input("\n\033[1;36;40m Anime name ❯ \033[0;0m")

    with client.login(username=username,password=password,remember="Yes") as login:
        cap = client.anime_last_chapter(name)
        urls = client.download_links(name,cap)

        print(f"\n\033[1;36;40m {name} dowload links from chapter {cap} ❯ \033[0;0m")
        for i, url in enumerate (urls.values()):
            response = requests.get(url).status_code
            if response == 200:
                color = "\033[1;32;40m"
                link_color = "\033[0;30;47m"

            else:
                color = "\033[1;31;40m"
                link_color = "\033[0;37;40m"

            server = list(urls.keys())[i]
            print(f"\n\033[0;30;46m ❮ {server} ❯ \033[0;0m " + f"{link_color} {url} \033[0;0m" + f" {color} RESPONSE ❯ {response} \033[0;0m")
        
        option = input("\n\033[1;36;40m Choose the option ❯ \033[0;0m")
        if opTion != 0:
            url = (list(urls.values())[int(option)-1])
            webbrowser.get('google-chrome %s --incognito').open_new(url)


if __name__ == '__main__':
    exists = False
    if os.path.exists("config.json"):
        exists = True

    if exists == False:
        user = input("\n\033[1;36;40m Write the username ❯ \033[0;0m")
        password = input("\033[1;36;40m Write the password ❯ \033[0;0m")
        data = {"user":user, "pass":password}

        with open('config.json','w') as file:
            json.dump(data, file, indent=4)

    with open('config.json','r') as file:
        config = json.load(file)
        username = config["user"]
        password = config["pass"]
    main(username,password)
    
    