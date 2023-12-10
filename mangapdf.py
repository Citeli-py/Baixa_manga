from manga import *
import sys, json

# Talvez usar regex

# Erro em "jojos-bizarre-adventure-part-9---the-jojolands" o link deveria ser "jojos-bizarre-adventure-part-9-the-jojolands"
# Algumas imagens podem ser PNG
# Mostrar numero de capitulos

# mangapdf -create <nome> -l <diretorio_manga>                  => Cria um manga na lista de mangas 
# mangapdf -list                                                => Mostra os mangas registrados
# mangapdf -update <nome> -n <novo_nome> -l <novo_diretorio>    => Atualiza as informações de um manga
# mangapdf -delete <nome>                                       => Deleta um manga
# mangapdf -get <nome> -c <capitulo>                            => Baixa um capitulo do manga

jsonFile = "mangaList.json"
mangasJson = json.loads(open(jsonFile, "r").read())

def findManga(nome: str):
    for manga in mangasJson:
        if manga["nome"] == nome:
            return manga
    return None

def create():
    linkIndex = sys.argv.index("-l")
    nomeManga = " ".join(sys.argv[2:linkIndex])
    linkManga = sys.argv[linkIndex+1]

    if findManga(nomeManga) == None:
        mangasJson.append({"nome": nomeManga, "link": linkManga})
        print(f"Manga {nomeManga} foi adicionado a lista!")
    else:
        print("Já existe um manga com esse nome")

def listmanga():
    for manga in mangasJson:
        print(f"Manga: {manga['nome']}\nLink:{manga['link']}", end="\n\n")

def update():
    pass

def delete():
    nomeManga = " ".join(sys.argv[2:])
    manga = findManga(nomeManga)
    if manga == None:
        print("Esse manga não existe!")
    else:
        mangasJson.remove(manga)
        print(f"Manga {nomeManga} removido!")

def get():
    capituloIndex = sys.argv.index("-c")
    nome = " ".join(sys.argv[2:capituloIndex])
    capitulo = sys.argv[capituloIndex+1]
    link = findManga(nome)["link"]
    Manga(link, capitulo).download(serial=True)

def help():
    print('''mangapdf -create <nome> -l <diretorio_manga>                  => Cria um manga na lista de mangas 
mangapdf -list                                                => Mostra os mangas registrados
mangapdf -update <nome> -n <novo_nome> -l <novo_diretorio>    => Atualiza as informações de um manga
mangapdf -delete <nome>                                       => Deleta um manga
mangapdf -get <nome> -c <capitulo>                            => Baixa um capitulo do manga''')
    pass

options = {
    "-create":create,
    "-c":create,
    "-list": listmanga,
    "-l": listmanga,
    "-update": update,
    "-u": update,
    "-delete": delete,
    "-d": delete,
    "-get": get,
    "-g": get,
    "-h": help,
}

op = sys.argv[1]
options.get(op, print)()


with open(jsonFile, "w") as f:
    f.write(json.dumps(mangasJson))
