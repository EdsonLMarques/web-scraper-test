import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
from pesquisa_manual.lello_imoveis import casas
import sqlite3

def connect():
    # Conecte-se ao banco de dados
    conn = sqlite3.connect('database/imoveis.db')
    cursor = conn.cursor()

    # Consulta SQL para selecionar todos os imóveis
    cursor.execute('SELECT * FROM imoveis')

    # Obtenha todos os resultados da consulta
    imoveis = cursor.fetchall()

    # Feche a conexão com o banco de dados
    conn.close()

    return imoveis


def get_color(price, min_price, max_price):
    colormap = LinearColormap(
        ['blue', 'yellow', 'red'],
        vmin=min_price,
        vmax=max_price
    )
    return colormap(price)


if __name__ == '__main__':
    #conexão com banco de dados
    imoveis = connect()
    imoveis = sorted(imoveis, key=lambda x: x[5])
    # Crie o mapa
    mapa = folium.Map(location=[-23.5505199, -46.6333094], zoom_start=14)

    # Defina os limites de preço mínimo e máximo
    min_price = imoveis[0][5]
    max_price = imoveis[-1][5]

    # Crie um colormap linear
    colormap = LinearColormap(
        ['blue', 'yellow', 'red'],
        vmin=min_price,
        vmax=max_price
    )

    # Para cada imóvel, crie um polígono com base na latitude, longitude e preço

    for imovel in imoveis:
        lat = imovel[1]
        lon = imovel[2]
        price = imovel[5]
        color = get_color(price, min_price, max_price)

        # Crie um polígono com centro em (lat, lon) e dimensões de 10m x 20m
        polygon = folium.RegularPolygonMarker(
            location=(lat, lon),
            number_of_sides=4,
            radius=5,  # 5m
            fill_color=colormap(price),
            color=color,
            fill_opacity=0.7
        )

        # Adicione um popup com informações adicionais
        try:
            popup_text = f"OLA FELIPAO" \
                         f"Região: {imovel[3]}<br>" \
                         f"Cidade: {imovel[4]}<br>" \
                         f"Valor de Locação: R$ {imovel[5]}"
            popup = folium.Popup(popup_text, max_width=300)
            polygon.add_child(popup)

            # Adicione o polígono ao mapa
            polygon.add_to(mapa)
        except:
            pass

    # Adicione a legenda ao mapa
    colormap = LinearColormap(
        ['blue', 'yellow', 'red'],
        vmin=min_price,
        vmax=max_price
    )
    colormap.caption = 'Preço (R$)'
    mapa.add_child(colormap)

    # Exiba o mapa
    mapa.save('map.html')

    #heat map
    # Crie o mapa
    Hmapa = folium.Map(location=[-23.5505199, -46.6333094], zoom_start=14)

    min_price = imoveis[0][5]
    max_price = imoveis[-1][5]

    # Normaliza os preços para estar na mesma faixa que o colormap
    normalized_data = [
        (imovel[1], imovel[2], (imovel[5] - min_price) / (max_price - min_price)) for
        imovel in imoveis]


    # Crie o HeatMap
    heatmap = HeatMap(normalized_data, radius=15)

    # Adicione o HeatMap ao mapa
    heatmap.add_to(Hmapa)

    # Exiba o mapa
    Hmapa.save('heatmap.html')

