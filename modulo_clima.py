import requests
import pandas as pd
from datetime import datetime

def buscar_clima_capitais(api_key="77b63a671563949ddd2ab6f5357fbb99"):
    """
    Consulta a API do OpenWeatherMap e retorna um DataFrame do Pandas
    com a probabilidade de chuva das capitais brasileiras.
    """
    MAPA_COORDENADAS = { 
        "AC": {"cidade": "Rio Branco", "lat": -9.9724, "lon": -67.8101},
        "AL": {"cidade": "Maceió", "lat": -9.6432, "lon": -35.7188},
        "AP": {"cidade": "Macapá", "lat": 0.0333, "lon": -51.0583},
        "AM": {"cidade": "Manaus", "lat": -3.0915, "lon": -60.0214},
        "BA": {"cidade": "Salvador", "lat": -12.9711, "lon": -38.5108},
        "CE": {"cidade": "Fortaleza", "lat": -3.7319, "lon": -38.5267},
        "DF": {"cidade": "Brasília", "lat": -15.7797, "lon": -47.9297},
        "ES": {"cidade": "Vitória", "lat": -20.3177, "lon": -40.3367},
        "GO": {"cidade": "Goiânia", "lat": -16.6869, "lon": -49.2656},
        "MA": {"cidade": "São Luís", "lat": -2.5300, "lon": -44.3030},
        "MG": {"cidade": "Belo Horizonte", "lat": -19.9227, "lon": -43.9450},
        "MS": {"cidade": "Campo Grande", "lat": -20.4427, "lon": -54.6468},
        "MT": {"cidade": "Cuiabá", "lat": -15.5989, "lon": -56.1088},
        "PA": {"cidade": "Belém", "lat": -1.4558, "lon": -48.5044},
        "PB": {"cidade": "João Pessoa", "lat": -7.1185, "lon": -34.8740},
        "PE": {"cidade": "Recife", "lat": -8.0578, "lon": -34.8829},
        "PI": {"cidade": "Teresina", "lat": -5.0917, "lon": -42.8039},
        "PR": {"cidade": "Curitiba", "lat": -25.4290, "lon": -49.2665},
        "RJ": {"cidade": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
        "RN": {"cidade": "Natal", "lat": -5.7945, "lon": -35.2101},
        "RO": {"cidade": "Porto Velho", "lat": -8.7608, "lon": -63.8967},
        "RR": {"cidade": "Boa Vista", "lat": 2.8182, "lon": -60.6714},
        "RS": {"cidade": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
        "SC": {"cidade": "Florianópolis", "lat": -27.5935, "lon": -48.5585},
        "SE": {"cidade": "Aracaju", "lat": -10.9472, "lon": -37.0731},
        "SP": {"cidade": "São Paulo", "lat": -23.5505, "lon": -46.6333},
        "TO": {"cidade": "Palmas", "lat": -10.2484, "lon": -48.3269} 
    }
    
    URL_BASE = "http://api.openweathermap.org/data/2.5/weather"
    resultados = []

    for uf, dados_local in MAPA_COORDENADAS.items():
        params = {
            'lat': dados_local['lat'],
            'lon': dados_local['lon'],
            'appid': api_key
        }
        
        try:
            # Timeout curto para evitar congelamento da tela se a API demorar
            response = requests.get(URL_BASE, params=params, timeout=3)
            if response.status_code == 200:
                dados = response.json()
                umidade = dados["main"]["humidity"]
                nuvens = dados["clouds"]["all"]
                prob_chuva = ((0.6 * (nuvens / 100)) + (0.4 * (umidade / 100))) * 100
                
                resultados.append({
                    "UF": uf,
                    "Cidade": dados_local['cidade'],
                    "Umidade (%)": umidade,
                    "Nuvens (%)": nuvens,
                    "Prob. Chuva (%)": round(prob_chuva, 2)
                })
        except requests.exceptions.RequestException:
            continue

    df_clima = pd.DataFrame(resultados)
    df_clima.attrs['ultima_atualizacao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    return df_clima

# TESTE LOCAL

if __name__ == "__main__":
    print("Consultando API... aguarde.")
    df_resultados = buscar_clima_capitais()
    print("\n--- Resultado do Processamento (Clima) ---")
    print(df_resultados.head())
