from selenium import webdriver
from PIL import Image
import os, requests, time

'''
https://mangayabu.top/ler/berserk-capitulo-364-my683112/
https://cdn.mangayabu.top/mangas/chainsaw-man/capitulo-70/02.jpg
https://mangayabu.top/mangas2/berserk/capitulo-364/03.jpg
https://cdn.mangayabu.com/mangas2/chainsaw-man/capitulo-97/22.jpg
https://cdn.mangayabu.top/mangas/oyasumi-punpun/capitulo-01/02.jpg
https://cdn.mangayabu.top/mangas/shingeki-no-kyojin/capitulo-01/00.jpg
Coisas para colocar:
Baixar capitulo,
Baixar de X ate Y capitulo
'''

def format(x):
    if x<10:
        return "0"+str(x)
    else:
        return str(x)

def baixar(manga, cap):
    print(manga)
    cap = format(cap)
    imgs = []
    i = 0
    while True:
        pg = format(i)
        r = requests.get("https://cdn.mangayabu.com/"+manga+"/capitulo-"+ cap + "/"+ pg + ".jpg")

        if r.content[2:9]!= b'DOCTYPE' and r.status_code == 200:
            path = "Imagens/imagem_"+pg+".jpg"
            img = open(path, "wb")
            img.write(r.content)
            imgs.append(Image.open(path).convert('RGB'))
        else:
            break
        i+=1
    manga = manga.split('/')[1]
    imgs[0].save(f'Mangas/{manga}_{cap}.pdf', save_all=True, append_images=imgs[1:])


def baixar_range(manga, inicio, fim):
    for i in range(fim-inicio+1):
        baixar(manga, inicio+i)
        print(f"Baixando capítulo {inicio+i}", end="\r")

def gen_url(manga):
    manga = manga.replace(" ", "-").lower()

    r1 = requests.get(f"https://cdn.mangayabu.com/mangas/{manga}/capitulo-01/00.jpg")
    r2 = requests.get(f"https://cdn.mangayabu.com/mangas2/{manga}/capitulo-01/00.jpg")

    if r1.status_code!=200 and r2.status_code!=200:
        print("Manga não encontrado")
        exit()

    if len(r1.content)>len(r2.content):
        return f"mangas/{manga}"
    else:
        return f"mangas2/{manga}"
        
def limpa():
    #limpa a pasta imagens
    pass

os.chdir(os.path.dirname(__file__))
t0 = time.time()
#baixar(gen_url("berserk"), 1)
baixar_range(gen_url("hunter x hunter"), 1, 2)
print("\nTudo foi executado em "+ str(round(time.time()-t0, 2)) + " Segundos")
