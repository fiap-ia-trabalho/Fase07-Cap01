import random
from datetime import datetime

def ler_sensores_esp32():
    """
    Simula a leitura dos sensores físicos do ESP32 (Wokwi).
    Na vida real, isso viria de uma requisição MQTT ou banco de dados.
    """
    # Simulando a leitura do DHT22 (Umidade)
    umidade = round(random.uniform(20.0, 80.0), 1)
    
    # Simulando a leitura do LDR (Convertido para escala de pH 0 a 14)
    ph_solo = round(random.uniform(4.5, 8.5), 1)
    
    # Simulando os 3 botões do NPK (True = Bom, False = Baixo)
    nivel_n = random.choice([True, False])
    nivel_p = random.choice([True, False])
    nivel_k = random.choice([True, False])
    
    # Lógica de Irrigação (Relé Azul da Bomba d'água)
    bomba_ligada = False
    motivo_bomba = "Condições ideais. Bomba desligada."
    
    if umidade < 40.0:
        bomba_ligada = True
        motivo_bomba = "Umidade crítica. Irrigação ativada."
    elif ph_solo < 5.5:
        bomba_ligada = True
        motivo_bomba = "pH ácido detectado. Irrigação para diluição ativada."
        
    return {
        "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Umidade do Solo (%)": umidade,
        "pH (LDR)": ph_solo,
        "Nitrogênio (N)": "Ideal" if nivel_n else "Baixo",
        "Fósforo (P)": "Ideal" if nivel_p else "Baixo",
        "Potássio (K)": "Ideal" if nivel_k else "Baixo",
        "Status Bomba D'água": "LIGADA" if bomba_ligada else "DESLIGADA",
        "Aviso do Sistema": motivo_bomba
    }

# TESTE LOCAL

if __name__ == "__main__":
    leitura = ler_sensores_esp32()
    print("--- Leitura dos Sensores IoT ---")
    for chave, valor in leitura.items():
        print(f"{chave}: {valor}")
