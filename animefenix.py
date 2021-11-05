import re
from bs4 import BeautifulSoup
import requests

'''By Raddiactive#1886'''

session = requests.Session()
class Client(): 
    def __init__(self):
        self.api = "https://animefenix.com/"
        self.api_2 = "https://animefenix.com/animes?"
        self.login_ = None
        self.serie_id_ = None
        self.user_id_ = None
        self.episode_id_ = None
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
            } 
        
    #String transform function
    def transform(self,serie:str): 
        serie = serie.lower()
        serie = serie.strip()
        serie = serie.replace(",", "").replace(".", "-")
        serie = serie.replace("!", "").replace(":", "")
        serie = serie.replace("&", "and").replace(" ", "-")
        serie = serie.replace("/", "-").replace("?", "")
        serie = serie.replace("'", "").replace("+", "")
        if "-" == serie[len(serie)-1:]:
            serie = serie[:-1]
        return serie
        
    #Login function
    def login(self, username: str, password: str, remember: str):
        """[summary]

        Args:
            username (str): [Username to login]
            password (str): [Account password]
            remember (str): [Yes/No]

        Returns:
            [Response]: [The response of the login request]
        """
        self.login_ = session.post(f"{self.api}/user/login",data={
            'username': username,
            'password': password,
            'remember': remember
            })
        return self.login_
        
    #Search animes   
    def search(self,serie:str):
        """[summary]

        Args:
            serie (str): [Anime name]

        Returns:
            [list]: [A list of search results]
        """     
        serie = self.transform(serie)
        i = 0
        count = 1
        series = []
        page = 1
        while i == 0:
            try:
                response = session.get(f"{self.api_2}q={serie}=1&page={self.count}")
                count += 1
                if response.status_code == 200:
                    i = 1
            except Exception as error:
                print(error)
        while page < count+2:
            request = session.get(f"{self.api_2}q={serie}&page={page}")
            soup = BeautifulSoup(request.text, "html.parser")
            entradas = soup.find_all('figure', {'class': 'image'})
            for entrada in enumerate(entradas):
                imgs = entrada[1].find_all('img')
                for img in enumerate(imgs):
                    cadena = str(img[1])
                    img = cadena.find('alt="')
                    img = str(cadena[img:cadena.find('" ')])
                    series.append(img)
            page += 1
        return series
    
    #Get user id
    def user_id(self):
        """[summary]

        Returns:
            [str]: [User id]
        """
        headers = self.login_.headers
        cookie = str(headers.get('set-cookie'))
        inicio = cookie.find('user_id=')
        cookie = cookie[inicio:inicio + (cookie.find(';'))]
        user_id = cookie.split('=')
        self.user_id_ = user_id[1]
        return self.user_id_
    
    #Get serie id
    def serie_id(self,name:str):
        """[summary]

        Args:
            name (str): [Name of the anime]

        Returns:
            [str]: [Anime id]
        """
        name = self.transform(name)
        req = session.get(self.api+name)
        if req.status_code == 200:
            req = req.text
            inicio = req.find('serie_id')
            string = str(req[inicio: inicio + (req.find('";'))])
            content = string[: string.find(';')]
            content = content.replace('"', "")
            content = content.replace(' ', "")
            serie_id = content.split('=')
            self.serie_id_ = serie_id[1]
            id = self.serie_id_
        else:
            id = req
        return id
        
    #Get episode id
    def episode_id(self,name:str,chapter:int):
        """[summary]

        Args:
            name (str): [Name of the anime]
            chapter (int): [Anime chapter]

        Returns:
            [str]: [Episode id]
        """
        name = self.transform(name)
        req = session.get(f"{self.api}{name}-{chapter}")
        if req.status_code == 200:
            req = req.text
            inicio = req.find('episode_id')
            string = str(req[inicio:inicio + (req.find('";'))])
            content= string[:string.find(';')]
            content = content.replace('"',"")
            content = content.replace(' ',"")
            episode_id = content.split('=')
            self.episode_id_ = episode_id[1]
            id = self.episode_id_
        else:
            id = req
        return id
       
    #Get emision animes    
    def emision_animes(self):
        """[summary]

        Returns:
            [list]: [An list of emision animes]
        """
        count = 1
        animes = []
        page = 1
        i = 0
        while i == 0:
            try:
                response = session.get(f"{self.api_2}estado[]=1&page={count}")
                count += 1
                if response.status_code == 200:
                    i = 1
            except Exception as error:
                print(error)
        while page < count+2:
            request = session.get(f"{self.api_2}estado[]=1&page={page}").text
            soup = BeautifulSoup(request ,"html.parser")
            entradas = soup.find_all('figure', {'class': 'image'})
            for entrada in enumerate(entradas):
                imgs = entrada[1].find_all('img')
                for img in enumerate(imgs):
                    cadena = str(img[1])
                    img = cadena.find('alt="')
                    img = str(cadena[img + img:cadena.find('" ')])
                    animes.append(img)
            page += 1
        return animes
    
    #Get chapters from the home page
    def chapters_of_the_day(self):
        """[summary]

        Returns:
            [dict]: [Chapters in the animefenix home,
            with anime name with the chapter and his link]
        """
        web = []
        title = []
        dicc = {}
        count = 0
        day = session.get(self.api)
        html = BeautifulSoup(day.text, "html.parser")
        all = html.find_all('div', {'class': 'capitulos-grid'})
        for todo in enumerate(all):
            animes = todo[1].find_all('div', {'class': 'overarchingdiv'})
            for anime in enumerate(animes):
                names = anime[1].find_all('a')
                for name in enumerate(names):
                    cadena = str(name[1])
                    link = cadena.find('href="')
                    link = str(cadena[link+6:cadena.find('" ')])
                    web.append(link)
                    for titulo in enumerate(names):
                        cadena = str(titulo[1])
                        tit = cadena.find('title="')
                        tit = cadena[tit+7:cadena.find('">')]
                        tit = tit.replace(" ","-")
                        chapter = tit[tit.rfind("-")+1:]
                        tit = tit[:tit.rfind("-")]
                        tit = tit + ": " + chapter
                        title.append(tit)    
            while count < len(web):
                titulos = title[count].strip()
                dicc[titulos] = web[count]
                count += 1
        return dicc
    
    #Get the amime's last chapter
    def anime_last_chapter(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [int]: [The chapter number]
        """
        name = self.transform(name)
        text = session.get(self.api+name)
        if text.status_code == 200:
            html = BeautifulSoup(text.text, "html.parser")
            all = html.find_all('ul', {'class': 'anime-page__episode-list is-size-6'})
            for todo in enumerate(all):
                find = str(todo[1].find('a', {
                    'class': 'fa-play-circle d-inline-flex align-items-center is-rounded'}))
                inicio = find.find('Episodio ')
                chapter = int(find[inicio + 9: -11])
        else:
            chapter = text
        return chapter
    
    #Get the next anime's chapter day    
    def next_chapter_day(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Next anime chapter day]
        """
        name = self.transform(name)
        text = session.get(f"{self.api}{name}")
        if text.status_code == 200:
            html = BeautifulSoup(text.text, "html.parser")
            all = html.find_all('figure', {'class': 'image is-2by4'})
            for todo in enumerate(all):
                imgs = todo[1].find_all('img')
                for img in enumerate(imgs):
                    cadena = str(img[1])
                    inicio = cadena.find('src="')+5
                    cadena = cadena[inicio:cadena.find('">')]
        else:
            cadena = text
        return cadena
    #Get anime's image
    def anime_image(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Url of the anime cover image]
        """
        name = self.transform(name)
        text = session.get(f"{self.api}{name}")
        if text.status_code == 200:
            html = BeautifulSoup(text.text, "html.parser")
            all = html.find_all('figure', {'class': 'image is-2by4'})
            for todo in enumerate(all):
                imgs = todo[1].find_all('img')
                for img in enumerate(imgs):
                    cadena = str(img[1])
                    inicio = cadena.find('src="')+5
                    cadena = cadena[inicio:cadena.find('">')]
        else:
            cadena = text  
        return cadena
              
    #Put the anime in your pendiet animes list
    def pendient_anime(self,vl:int):
        """[summary]

        Args:
            vl (int): [1= add to pendient animes list, 0 = Nothing,
            -1 = remove from pendient animes list]

        Returns:
            [response]: [The request response]
        """
        return session.post(f"{self.api}/app/wl_sHandler.php", data={
            'vl': vl,
            'idUser': self.user_id,
            'idSerie':self.serie_id_
            })
    
    #Put the anime in your fav animes list
    def fav_anime(self,fav:int):
        """[summary]

        Args:
            fav (int): [1= add to favorites list, 0 = Nothing,
            -1 = remove from favorites list]

        Returns:
            [response]: [The request response]
        """
        return session.post(f"{self.api}app/favHandler.php", data={
            'fav': fav,
            'id_usuario': self.user_id,
            'id_serie':self.serie_id_
            })
    #Put the anime in your pendient animes chapter list    
    def pendient_anime_chapter(self,pd:int):
        """[summary]

        Args:
            pd (int): [1= add to pendient chapter list, 0 = Nothing,
            -1 = remove from pendient chapter list]

        Returns:
            [response]: [The request response]
        """
        return session.post(f"{self.api}app/wlHandler.php", data={
            'vl': pd,
            'idUser':self.user_id,
            'idSerie':self.episode_id_
            })
        
    #Get anime's description    
    def description(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Anime description]
        """
        name = self.transform(name)
        req = session.get(f"{self.api}{name}")
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")   
            description = str(html.find_all('p', {'class': 'has-text-light sinopsis'}))
            inicio = description.find('>')
            description = description[inicio+1:]
            description = description[:description.find('<')]
        else:
            description = req
        return description
    
    #Get anime's chapters
    def anime_chapters(self,name:str): 
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [list]: [A list of the anime chapters]
        """
        name = self.transform(name)
        chapters = []
        req = session.get(f"{self.api}{name}")
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")   
            entradas = (html.find_all('ul', {'class': 'anime-page__episode-list is-size-6'}))
            for entrada in enumerate(entradas):
                links = entrada[1].find_all('a',{
                    'class': 'fa-play-circle d-inline-flex align-items-center is-rounded'})
                for link in enumerate(links):
                    cadena = str(link[1])
                    parse = cadena.find('ver/')
                    text = (cadena[parse+4: (cadena.find('">'))])
                    chapters.append(text)
        else:
            chapters = req
        return chapters
    
    #Get the anime chapter's download links    
    def download_links(self,name:str,cap:int):
        """[summary]

        Args:
            name (str): [Anime name]
            cap (int): [Anime chapter]

        Returns:
            [dict]: [Server and his link]
        """
        name = self.transform(name)
        page = session.get(f"{self.api}ver/{name}-{cap}/descarga")
        if page.status_code == 200:
            x = 0
            total = {}
            lista = []
            dic = []
            servers = []
            soup = BeautifulSoup(page.text, "html.parser")
            entradas = soup.find_all('section', {'class': 'section'})
            for i, entrada in enumerate(entradas):
                links = entrada.find_all('a')
                if i == 1:
                    for b, link in enumerate(links):
                        cadena = str(link)
                        parse = cadena.find('href="')
                        key = str(cadena[cadena.find("i>")+3: -4])
                        dic.append(key)
                        text = str(cadena[parse+6: parse + cadena.find(f'{b}" ')-40])
                        if re.search('dl=',text):
                            servers = text.replace("amp;", "")
                            lista.append(servers)
                    try:
                        while x < len(lista):
                            server = dic[x].title()
                            total[server] = lista[x]
                            x += 1
                    except Exception as error:
                        print(error)
        else:
            total = page
        return total