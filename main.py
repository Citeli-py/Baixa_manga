from PIL import Image
import os, requests, time

def format(x):
    if x<10:
        return "0"+str(x)
    else:
        return str(x)

def baixar(manga, cap):
    cap = format(cap)
    imgs = []
    i = 0
    while True:
        pg = format(i)
        r = requests.get("https://cdn.mangayabu."+manga+"/capitulo-"+ cap + "/"+ pg + ".jpg")
        if r.content[2:9]!= b'DOCTYPE' and r.status_code == 200 and len(r.content)>300:
            path = "Imagens/imagem_"+pg+".jpg"
            img = open(path, "wb")
            img.write(r.content)
            imgs.append(Image.open(path).convert('RGB'))
        elif i>1:
            break
        i+=1
    manga = manga.split('/')[2]
    criar_pasta(f'Mangas/{manga}')
    imgs[0].save(f'Mangas/{manga}/{manga} {cap}.pdf', save_all=True, append_images=imgs[1:])

def baixar_range(manga, inicio, fim):
    for i in range(fim-inicio+1):
        baixar(manga, inicio+i)
        print(f"Baixando capítulo {inicio+i}", end="\r")

def gen_url(manga):
    manga = manga.replace(" ", "-").lower()

    ext = ["com/mangas/", "com/mangas2/", "top/mangas/", "top/mangas2/"]
    req_len = []
    for i in ext:
        req = requests.get(f"https://cdn.mangayabu.{i}{manga}/capitulo-01/01.jpg")
        if req.content[2:9]!= b'DOCTYPE' and req.status_code == 200 and len(req.content)>300:
            req_len.append(len(req.content))
        else:
            req_len.append(-1)
    if max(req_len) != -1:
        return ext[req_len.index(max(req_len))]+manga
    else:
        print("Manga não encontrado")
        exit()

def limpa():
    i = 0
    while True:
        try:
            os.remove("Imagens/imagem_"+format(i)+".jpg")
            i += 1
        except:
            break

def criar_pasta(diretorio):
    os.chdir(os.path.dirname(__file__))
    try:
        os.makedirs(diretorio)
    except OSError:
        pass

if __name__ == "__main__":
    criar_pasta('Imagens')
    criar_pasta('Mangas')
    t0 = time.time()
    manga = input("Qual manga deseja baixar? ")
    cap_inicial = int(input("Baixar de: "))
    cap_final = int(input("Até: "))
    baixar_range(gen_url(manga), cap_inicial, cap_final)
    limpa()
    print("\nTudo foi executado em "+ str(round(time.time()-t0, 2)) + " Segundos")
