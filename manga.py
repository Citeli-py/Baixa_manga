"https://img.lermanga.org/{Primeira-letra-maiuscula}/{seu-manga}/capitulo-{capitulo}/{pagina}.jpg"
"https://img.lermanga.org/O/{seu-manga}/capitulo-{capitulo}/{pagina}.jpg"
"https://img.lermanga.org/B/berserk/capitulo--16/2.jpg"

"https://www.brmangas.net/ler/oyasumi-punpun-80-online/"
"https://dn1.imgstatic.club/uploads/o/oyasumi-punpun/80/1.png"

"https://img.lermanga.org/J/jojos-bizarre-adventure-part-9-the-jojolands/capitulo-1/1.jpg"


# Precisa fazer um codigo que possa colocar mais de um site para baixar
# ideia: formatar diferentes links e substituir os formatos conforme baixa


import requests, shutil, os, img2pdf, sys

class Manga:

    def __init__(self, manga: str, capitulo: str, NumThreads: int = 3) -> None:
        self.manga = manga
        self.capitulo = capitulo
        self.url = self.findUrl()
        self.NumThreads = NumThreads

    # def getPage(self, pagina=1) -> Procura a pagina web que está aquela pagina (extensão)

    def findUrl(self, ) -> str:
        zero = ["", "0"]
        exts = [".jpg", ".png", ".webp"]
        for zero1 in zero:
            for zero2 in zero:
                for ext in exts:
                    url = f"https://img.lermanga.org/{self.manga[0].upper()}/{self.manga}/capitulo-{zero1+str(self.capitulo)}/{zero2}1{ext}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        return url[:-(1+len(ext))]
        
        print(404)
        return None

    def downloadCapitulo(self,) -> None:
        os.makedirs(f'imgs/{self.manga}', exist_ok=True)
        pagina = 1
        while self.downloadPage(pagina):
            print("Pagina:", pagina, end='\r')
            pagina += 1
        
    
    def downloadCapituloThread(self, ):
        from threading import Thread, Lock

        os.makedirs(f'imgs/{self.manga}', exist_ok=True)

        thread_results = [{"thread": i, "pagina": 0} for i in range(self.NumThreads)]
        thread_pool = [Thread(target=self.downloadPageThread, args=(i+1, thread_results))
                       for i in range(self.NumThreads)]

        for thread in thread_pool:
            thread.start()
        
        for thread in thread_pool:
            thread.join()

        print("\n"*self.NumThreads) # Para o recuo do carrier


    def downloadPageThread(self, start: int, thread_results: dict) -> None:
        pagina = start

        while self.downloadPage(pagina):
            thread_results[start-1]["pagina"] = pagina
            self.printThreads(thread_results)
            #print(start, pagina)
            pagina += self.NumThreads
        
        print("fim", start)

    def printThreads(self, thread_results: dict) -> None:
        infos = [f"Thread: {thread_results[i]['thread']} -> Pagina: {thread_results[i]['pagina']}" 
                for i in range(self.NumThreads)]
        
        print("\n".join(infos))
        print(f"\033[{self.NumThreads}A", end='', flush=True)
        

    def getPage(self, pagina: int = 1):
        exts = [".jpg", ".png", ".webp"]
        for ext in exts:
            if self.url[-1] == '0' and pagina > 9: #caso a primeira pagina tenha 0 na frente
                self.url = self.url[:-1]

            url = f"{self.url}{pagina}{ext}"
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                #print(url, response)
                return response, ext
        
        return None, None


    def downloadPage(self, pagina: int) -> bool:
        response, ext = self.getPage(pagina)

        if response == None:
            #print("Essa pagina não existe")
            return False

        with open(f'imgs/{self.manga}/{self.capitulo}-{pagina}{ext}', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)      
        return True
    
    def generatePdf(self, ) -> None:
        os.makedirs(f'mangas/{self.manga}', exist_ok=True)

        paginas = os.listdir(f"imgs/{self.manga}")
        imagens = [f"imgs/{self.manga}/{pagina}" for pagina in paginas]
        imagens = sorted(imagens, key=self.extrair_numero)

        dados_pdf = img2pdf.convert(imagens)
        with open(f"mangas/{self.manga}/{self.manga}-{self.capitulo}.pdf", "wb") as arquivo:
            arquivo.write(dados_pdf)

        self.clean()
    
    def extrair_numero(self, imagem):
        # Obtém o número antes da extensão
        numero = int(imagem.split('/')[-1].split('-')[-1].split('.')[0])
        return numero

    
    def clean(self, ):
        shutil.rmtree(f"imgs/{self.manga}")

    
    def download(self, serial: bool = False ) -> None:
        if self.url != None:
            if serial:
                self.downloadCapitulo()
            else:
                self.downloadCapituloThread()

            self.generatePdf()
        
        else:
            print("Esse manga ou capitulo não existe em Ler Manga, ou ocorreu um erro!")


def searchManga(manga: str) -> list():
    #https://lermanga.org/?s=jojo
    response = requests.get(f"https://lermanga.org/?s={manga}")

    import re
    elementos = re.findall('<a href="(.*?)" title="(.*?)" class="dynamic-name" data-jname="(.*?)">(.*?)</a>', response.text)

    mangas =[]
    for elemento in elementos:
        nome, f_manga = elemento[3], re.search("https://lermanga.org/mangas/(.*?)/", elemento[0]).group(1)
        mangas.append((nome, f_manga))

    return mangas
        
def printMangas(mangas: list):
    i=1
    for manga in mangas:
        print(f"{i}:", manga[0])
        i+=1


#manga = "jojo-no-kimyou-na-bouken-part-7-steel-ball-run-colorida"
#capitulo = "85"

#searchManga("jojo")

#printMangas(searchManga("One Piece"))

#m = Manga(manga, capitulo)
#m.downloadCapituloThread()
#m.generatePdf()


# python3 main.py -s jojo 1 -c 86