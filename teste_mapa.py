import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
from pesquisa_manual.lello_imoveis import casas

def get_color(price, min_price, max_price):
    colormap = LinearColormap(
        ['blue', 'yellow', 'red'],
        vmin=min_price,
        vmax=max_price
    )
    return colormap(price)


if __name__ == '__main__':
    # Crie o mapa
    mapa = folium.Map(location=[-23.5505199, -46.6333094], zoom_start=14)

    # Defina os limites de preço mínimo e máximo
    min_price = 500
    max_price = 50000

    # Crie um colormap linear
    colormap = LinearColormap(
        ['blue', 'yellow', 'red'],
        vmin=min_price,
        vmax=max_price
    )

    # Para cada imóvel, crie um polígono com base na latitude, longitude e preço



    imoveis = sorted(casas, key=lambda x: x["valorLocacao"])
    for imovel in imoveis:
        lat = imovel["latitude"]
        lon = imovel["longitude"]
        price = imovel["valorLocacao"]
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
            popup_text = f"Região: {imovel['regiao']}<br>" \
                         f"Cidade: {imovel['cidade']}<br>" \
                         f"Valor de Locação: R$ {imovel['valorLocacao']}"
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

    min_price = imoveis[0]["valorLocacao"]
    max_price = imoveis[-1]["valorLocacao"]

    # Normaliza os preços para estar na mesma faixa que o colormap
    normalized_data = [
        (imovel["latitude"], imovel["longitude"], (imovel["valorLocacao"] - min_price) / (max_price - min_price)) for
        imovel in imoveis]


    # Crie o HeatMap
    heatmap = HeatMap(normalized_data, radius=15)

    # Adicione o HeatMap ao mapa
    heatmap.add_to(Hmapa)

    # Exiba o mapa
    Hmapa.save('heatmap.html')

