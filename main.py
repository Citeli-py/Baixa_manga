from PIL import Image
import os, requests, time

def format(x):
    x = int(x)
    if x<10:
        return "0"+str(x)
    else:
        return str(x)

def baixar(manga, cap):
    cap = format(cap)
    print("baixar",cap)
    url = gen_url(manga, cap)
    imgs = []
    i = 0
    while True:
        pg = format(i)
        r = requests.get(url+"/capitulo-"+ cap + "/"+ pg + ".jpg")
        if r.content[2:9]!= b'DOCTYPE' and r.status_code == 200 and len(r.content)>300:
            path = "Imagens/imagem_"+pg+".jpg"
            img = open(path, "wb")
            img.write(r.content)
            imgs.append(Image.open(path).convert('RGB'))
        elif i>1:
            break
        i+=1
    
    criar_pasta(f'Mangas/{manga}')
    imgs[0].save(f'Mangas/{manga}/{manga}-{cap}.pdf', save_all=True, append_images=imgs[1:])

def baixar_range(manga, inicio, fim):
    print("baixar",inicio)
    for i in range(inicio, fim):
        baixar(manga, i)
        print(f"Baixando capítulo {i}", end="\r")

def gen_url(manga, cap):
    manga = manga.replace(" ", "-").lower()

    auxs = ["cdn.", ""]
    exts = ["com/mangas/", "com/mangas2/", "top/mangas/", "top/mangas2/"]

    for aux in auxs:
        for ext in exts:
            url = f"https://{aux}mangayabu.{ext}{manga}/capitulo-{format(cap)}/01.jpg"
            print(url)
            req = requests.get(url)
            if req.content[2:9]!= b'DOCTYPE' and req.status_code == 200 and len(req.content)>300:
                return url

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

def capitulos(caps):
    caps = caps.split("-")
    if len(caps) > 1:
        return int(caps[0]), int(caps[1])
    return int(caps[0]), int(caps[0])

if __name__ == "__main__":
    criar_pasta('Imagens')
    criar_pasta('Mangas')
    #t0 = time.time()
    #manga = input("Qual manga deseja baixar? ")
    manga = "chainsaw man"
    #caps = input("Baixar de: ")
    #cap_inicial, cap_final = capitulos(caps)
    cap_inicial, cap_final = 99,99
    #print(cap_inicial,cap_final)
    baixar_range(manga, cap_inicial, cap_final)
    limpa()
    #print("\nTudo foi executado em "+ str(round(time.time()-t0, 2)) + " Segundos")
