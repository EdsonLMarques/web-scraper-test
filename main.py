from bs4 import BeautifulSoup
import requests

class Imovel:
    def __init__(self, imobiliaria, url, endereco, preco,):
        self.imobiliaria = imobiliaria
        self.link = url
        self.endereco = endereco
        self.preco = preco

    def __repr__(self):
        return f"Imóvel em {self.endereco} da imobiliária {self.imobiliaria}: R${self.preco}, {self.quartos} quartos"
class Imobiliaria:
    def __init__(self, url):
        self.nome = self.__get_name(url)
        self.link = url

    def __get_name(self, url):
        name = url.split('.')[1]
        return name

    def __repr__(self):
        return self.nome

def getGoogleData(lista):
    # URL da pesquisa no Google
    url = 'https://www.google.com/search?q=imobiliarias+em+sao+paulo+capital'

    # Enviar solicitação HTTP e obter o conteúdo da página
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os links para as imobiliárias
    links_imobiliarias = []
    for link in soup.find_all('a'):
        href = link.get('href')
        contidions = ['google' not in href and 'maps' not in href and 'search%' not in href]
        if href.startswith('/url?q=') and all(contidions):
            link_imobiliaria = href.split('/url?q=')[1].split('&sa=')[0]
            links_imobiliarias.append(link_imobiliaria)


    # Criar objetos Imobiliarias
    listaNomes = ['spimovel']
    for link in links_imobiliarias:
        nome = str(link.split('.')[1])
        if nome not in listaNomes:
            listaNomes.append(nome)
            lista.append(Imobiliaria(link))

    return lista

def getImoveis(link):
    pass


if __name__ == '__main__':
    listaImobiliarias= []
    listaImobiliarias = getGoogleData(lista=listaImobiliarias)
    for imobiliaria in listaImobiliarias:
        getImoveis(imobiliaria.link)
