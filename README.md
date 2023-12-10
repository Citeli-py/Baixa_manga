# Baixa mangá
Esse projeto tem como objetivo baixar qualquer mangá presentes no site [lermanga](https://lermanga.org)
## Como usar
Usar é simples, basta ter Python 3 instalado e executar o programa.<br>
Para baixar os seus mangas é só seguir o exemplo:

```bash
# mangapdf -create <nome> -l <diretorio_manga>                  => Cria um manga na lista de mangas 
# mangapdf -list                                                => Mostra os mangas registrados
# mangapdf -update <nome> -n <novo_nome> -l <novo_diretorio>    => Atualiza as informações de um manga
# mangapdf -delete <nome>                                       => Deleta um manga
# mangapdf -get <nome> -c <capitulo>                            => Baixa um capitulo do manga
```
Após colocar as informações, os mangas serão baixados na pasta **Mangas** no mesmo diretório do programa. 
## Conclusões finais
**Ainda há melhorias que precisam ser feitas, como:<br>**
baixar capitulos não inteiros (35.5 ou 35-5).<br>
Fazer o paralelismo funcionar em todos os casos.<br>
