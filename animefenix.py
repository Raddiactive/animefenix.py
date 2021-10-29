from bs4 import BeautifulSoup
import os
import re
import requests



''' By Raddiactive#1886 '''

session = requests.Session()
class Client():
       
    def login(self, username: str, password: str, remember: str):
        """[summary]

        Args:
            username (str): [Username to login]
            password (str): [Account password]
            remember (str): [Yes/No]

        Returns:
            [Response]: [The response of the login request]
        """
        return session.post("https://www.animefenix.com/user/login",data={'username': username, 'password': password, 'remember': remember})
        
    def search(self,serie:str):
        """[summary]

        Args:
            serie (str): [Anime name]

        Returns:
            [list]: [A list of search results]
        """
        serie = serie.lower()
        serie = serie.strip()
        serie = serie.replace(",","").replace(".","").replace("+","")
        serie = serie.replace("&","and").replace(" ","-").replace("/","-")
                
        print(serie)
        self.i = 0
        self.count = 1
        self.series = []
        while self.i == 0:
            try:
                self.response = session.get(f"https://www.animefenix.com/animes?q={serie}=1&page={self.count}")
                self.count += 1
                if self.response != "<Response [200]>":
                    self.i = 1
            except: pass

        self.page = 1
        while self.page < self.count+2:
            self.request = session.get(f"https://www.animefenix.com/animes?q={serie}&page={self.page}")
            self.soup = BeautifulSoup(self.request.text,"html.parser")
            self.entradas = self.soup.find_all('figure', {'class': 'image'})
            
            for self.i, self.entrada in enumerate(self.entradas):
                self.imgs = self.entrada.find_all('img')
                for self.b, self.img in enumerate(self.imgs):
                    self.cadena = str(self.img)
                    self.img = self.cadena.find('alt="')
                    self.img = str(self.cadena[self.img:self.cadena.find('" ')])
                    self.series.append(self.img)
            self.page += 1

        return self.series    

    def user_id(self):
        """[summary]

        Returns:
            [str]: [User id]
        """
        self.headers = self.headers
        self.cokie = str(self.headers.get('set-cookie'))
        self.inicio = self.cokie.find('user_id=')
        self.cokie = self.cokie[self.inicio:self.inicio+(self.cokie.find(';'))]
        self.userid = self.cokie.split('=')
        return self.userid[1]
    
    def serie_id(self,name:str):
        """[summary]

        Args:
            name (str): [Name of the anime]

        Returns:
            [str]: [Anime id]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.req = session.get(f"https://www.animefenix.com/{name}")
        if self.req.status_code == 200:
            self.req = self.req.text
            self.inicio = self.req.find('serie_id')
            self.string = str(self.req[self.inicio:self.inicio+(self.req.find('";'))])
            self.content= self.string[:self.string.find(';')]
            self.content = self.content.replace('"',"")
            self.content = self.content.replace(' ',"")
            self.serieid = self.content.split('=')
            return self.serieid[1]
        else: return self.req
    
    def episode_id(self,name:str,chapter:int):
        """[summary]

        Args:
            name (str): [Name of the anime]
            chapter (int): [Anime chapter]

        Returns:
            [str]: [Episode id]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")
    
        self.req = self.session.get(f"https://www.animefenix.com/ver/{name}-{chapter}")
        if self.req.status_code == 200:
            self.req = self.req.text
            self.inicio = self.req.find('episode_id')
            self.string = str(self.req[self.inicio:self.inicio+(self.req.find('";'))])
            self.content= self.string[:self.string.find(';')]
            self.content = self.content.replace('"',"")
            self.content = self.content.replace(' ',"")
            self.episodeid = self.content.split('=')
            return self.episodeid[1]
        else: return self.req
        
    def emision_animes(self):
        """[summary]

        Returns:
            [list]: [An list of emision animes]
        """
        self.i = 0
        self.count = 1
        self.animes = []
        while self.i == 0:
            try:
                self.response = session.get(f"https://www.animefenix.com/animes?estado[]=1&page={self.count}")
                self.count += 1
                if self.response != "<Response [200]>":
                    i = 1
            except: pass
        self.page = 1
        while self.page < self.count+2:
            self.request = self.session.get(f"https://www.animefenix.com/animes?estado[]=1&page={self.page}").text
            self.soup = BeautifulSoup(self.request,"html.parser")
            self.entradas = self.soup.find_all('figure', {'class': 'image'})
            
            for self.i, self.entrada in enumerate(self.entradas):
                self.imgs = self.entrada.find_all('img')
                for self.b, self.img in enumerate(self.imgs):
                    self.cadena = str(self.img)
                    self.img = self.cadena.find('alt="')
                    self.img = str(self.cadena[self.img+self.img:self.cadena.find('" ')])
                    self.animes.append(self.img)
            self.page += 1
        return self.animes
    
    def chapters_of_the_day(self):
        """[summary]

        Returns:
            [dict]: [Chapters in the animefenix home, with anime name with the chapter and his link]
        """
        self.web = []
        self.i = 0
        self.x = 0
        self.title = []
        self.dicc= {}
        self.count = 0
        self.day = session.get("https://www.animefenix.com/")
        self.html = BeautifulSoup(self.day.text, "html.parser")
        self.todos = self.html.find_all('div', {'class': 'capitulos-grid'})
        for self.i,self.todo in enumerate(self.todos):
            self.animes = self.todo.find_all('div', {'class': 'overarchingdiv'})
            for self.b, self.anime in enumerate(self.animes):
                self.names = self.anime.find_all('a')
                for self.x,self.name in enumerate(self.names):
                    self.cadena = str(self.name)
                    self.link = self.cadena.find('href="')
                    self.link = str(self.cadena[self.link+6:self.cadena.find('" ')])
                    self.web.append(self.link)
                    for self.z, self.titulo in enumerate(self.names):
                        self.cadena = str(self.titulo)
                        self.tit = self.cadena.find('title="')
                        self.tit = self.cadena[self.tit+7:self.cadena.find('">')]
                        self.tit = self.tit.replace(" ","-")
                        self.chapter = self.tit[self.tit.rfind("-")+1:]
                        self.tit = self.tit[:self.tit.rfind("-")]
                        self.tit = self.tit+": "+self.chapter
                        self.title.append(self.tit)
            while self.count < len(self.web):
                self.titulos = self.title[self.count].strip()
                self.dicc[self.titulos]=self.web[self.count]
                self.count +=1
        return self.dicc
    
    def anime_last_chapter(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [int]: [The chapter number]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.text = session.get(f"https://www.animefenix.com/{name}")
        if self.text.status_code == 200:
            self.html = BeautifulSoup(self.text.text, "html.parser")
            self.todos = self.html.find_all('ul', {'class': 'anime-page__episode-list is-size-6'})

            for self.x,self.todo in enumerate(self.todos):
                self.find = str(self.todo.find('a',{'class':'fa-play-circle d-inline-flex align-items-center is-rounded'}))
                self.inicio = self.find.find('Episodio ')
                return int(self.find[self.inicio+9:-11])

        else: return self.text
        
    def next_chapter_day(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Next anime chapter day]
        """
        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.i = 0
        self.x = 0
        self.text = session.get(f"https://www.animefenix.com/{name}")
        if self.text.status_code == 200:
            self.html = BeautifulSoup(self.text.text, "html.parser")
            self.todos = self.html.find_all('figure', {'class': 'image is-2by4'})
            for self.i,todo in enumerate(self.todos):

                self.imgs = todo.find_all('img')
                for self.x, self.img in enumerate(self.imgs):

                    self.cadena = str(self.img)
                    self.inicio = self.cadena.find('src="')+5
                    return self.cadena[self.inicio:self.cadena.find('">')]

        else: return self.text 
 
    def anime_image(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Url of the anime cover image]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.i = 0
        self.x = 0
        self.text = session.get(f"https://www.animefenix.com/{name}")
        if self.text.status_code == 200:
            self.html = BeautifulSoup(self.text.text, "html.parser")
            self.todos = self.html.find_all('figure', {'class': 'image is-2by4'})

            for self.i,self.todo in enumerate(self.todos):
                self.imgs = self.todo.find_all('img')

                for self.x, self.img in enumerate(self.imgs):
                    self.cadena = str(self.img)
                    self.inicio = self.cadena.find('src="')+5
                    return self.cadena[self.inicio:self.cadena.find('">')]

        else: return self.text           

    def pendient_anime(self,vl:int):
        """[summary]

        Args:
            vl (int): [1= add to pendient animes list, 0 = Nothing, -1 = remove from pendient animes list]

        Returns:
            [response]: [The request response]
        """
        return session.post("https://www.animefenix.com/app/wl_sHandler.php", {'vl': vl,'idUser': self.user_id,'idSerie':self.serie_id})
    
    def fav_anime(self,fav:int):
        """[summary]

        Args:
            fav (int): [1= add to favorites list, 0 = Nothing, -1 = remove from favorites list]

        Returns:
            [response]: [The request response]
        """
        return session.post("https://www.animefenix.com/app/favHandler.php", {'fav': fav,'id_usuario': self.user_id,'id_serie':self.serie_id})
        
    def pendient_anime_chapter(self,pd:int):
        """[summary]

        Args:
            pd (int): [1= add to pendient chapter list, 0 = Nothing, -1 = remove from pendient chapter list]

        Returns:
            [response]: [The request response]
        """
        return session.post("https://www.animefenix.com/app/wlHandler.php", {'vl': pd,'idUser':self.user_id,'idSerie':self.episode_id})
        
    def description(self,name:str):
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [str]: [Anime description]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")
        
        self.req = session.get(f"https://www.animefenix.com/{name}")
        if self.req.status_code == 200:
            self.html = BeautifulSoup(self.req.text, "html.parser")   
            self.description = str(self.html.find_all('p', {'class': 'has-text-light sinopsis'}))
            self.inicio = self.description.find('>')
            self.description = self.description[self.inicio+1:]
            return self.description[:self.description.find('<')]

        else: return self.req
      
    def anime_chapters(self,name:str): 
        """[summary]

        Args:
            name (str): [Anime name]

        Returns:
            [list]: [A list of the anime chapters]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.i = 0
        self.c = 1
        self.d = 2
        self.req = session.get(f"https://www.animefenix.com/{name}")
        if self.req.status_code == 200:
            self.html = BeautifulSoup(self.req.text, "html.parser")   
            self.entradas = (self.html.find_all('ul', {'class': 'anime-page__episode-list is-size-6'}))

            for self.i, self.self.entrada in enumerate(self.entradas):
                self.links = self.entrada.find_all('a',{'class': 'fa-play-circle d-inline-flex align-items-center is-rounded'})

                for self.b,self.link in enumerate(self.links):
                    self.cadena = str(self.link)
                    self.parse = self.cadena.find('ver/')
                    self.text = (self.cadena[self.parse+4:(self.cadena.find('">'))])
                    self.chapters.append(self.text)
            return self.chapters

        else: return self.req
        
    def download_links(self,name:str,cap:int):
        """[summary]

        Args:
            name (str): [Anime name]
            cap (int): [Anime chapter]

        Returns:
            [dict]: [Server and his link]
        """

        name = name.lower()
        name = name.strip()
        name = name.replace(",","").replace(".","").replace("+","")
        name = name.replace("&","and").replace(" ","-").replace("/","-")

        self.page = session.get(f"https://www.animefenix.com/ver/{name}-{cap}/descarga")
        if self.page.status_code == 200:
            self.total = {}
            self.lista = []
            self.dic = []
            self.servers = []
            self.x = 0
            self.i = 0
            self.soup = BeautifulSoup(self.page.text,"html.parser")
            self.entradas = self.soup.find_all('section', {'class': 'section'})

            for self.i, self.entrada in enumerate(self.entradas):
                self.links = self.entrada.find_all('a')
                if self.i == 1:
                    for self.b, self.link in enumerate(self.links):
                        self.cadena = str(self.link)
                        self.parse = self.cadena.find('href="')
                        self.key = str(self.cadena[self.cadena.find("i>")+3:-4])
                        self.dic.append(self.key)
                        self.text = str(self.cadena[self.parse+6:self.parse+self.cadena.find(f'{self.b}" ')-40])
                        
                        if re.search('dl=',self.text):
                            self.servers = self.text.replace("amp;","")
                            self.lista.append(self.servers)
                    try:
                        while self.x < len(self.lista):
                            self.server = self.dic[self.x].title()
                            self.total[self.server]=self.lista[self.x]
                            self.x += 1
                    except: pass

            return self.total
        else: return self.page
    
    def dowload_page_by_link(self,url:str):
        """[summary]

        Args:
            url (str): [Url from the page]

        Returns:
            [dict]: [Server and his link]
        """
        self.page = session.get(f"{url}/descarga")
        if self.page.status_code == 200:
            self.total = {}
            self.lista = []
            self.dic = []
            self.servers = []
            self.x = 0
            self.i = 0
            self.soup = BeautifulSoup(self.page.text,"html.parser")
            self.entradas = self.soup.find_all('section', {'class': 'section'})

            for self.i, self.entrada in enumerate(self.entradas):
                self.links = self.entrada.find_all('a')
                if self.i == 1:
                    for self.b, self.link in enumerate(self.links):
                        self.cadena = str(self.link)
                        self.parse = self.cadena.find('href="')
                        self.key = str(self.cadena[self.cadena.find("i>")+3:-4])
                        self.dic.append(self.key)
                        self.text = str(self.cadena[self.parse+6:self.parse+self.cadena.find(f'{self.b}" ')-40])
                        
                        if re.search('dl=',self.text):
                            self.servers = self.text.replace("amp;","")
                            self.lista.append(self.servers)
                        
                    try:
                        while self.x < len(self.lista):
                            self.server = self.dic[self.x].title()
                            self.total[self.server]=self.lista[self.x]
                            self.x += 1
                    except: pass

            return self.total
        else: return self.page
        
