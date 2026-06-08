import streamlit as st
from fase1 import calculo_area
from fase1 import api_meteorologica
from fase2 import banco_dados
from fase3 import esp32_sensor_sim

st.title("🚜 Teste de Integração - Fases 1, 2 e 3")

aba1, aba2, aba3 = st.tabs(["Fase 1 (Cálculos)", "Fase 2 (Banco/Clima)", "Fase 3 (IoT)"])

with aba1:
    st.header("Teste: Cálculos de Área e Insumo")
    st.write("Simulando os dados que viriam do input do usuário:")
    try:
        resultado_f1 = calculo_area.processar_dados_plantio("café", "Retângulo", 100, 50, "NPK", 1.5)
        st.json(resultado_f1)
    except Exception as e:
        st.warning(f"Função em desenvolvimento ou nome diferente: {e}")

with aba2:
    st.header("Teste: Conexão com Banco de Dados")
    # Chamando a conexão do banco 
    status_banco = banco_dados.conectar_banco()
    if "✅" in status_banco:
        st.success(status_banco)
    else:
        st.error(status_banco)

    st.divider()

    st.header("Teste: API de Clima")
    st.write("Buscando dados da API na nuvem e transformando em DataFrame...")
    # Chamando sua função de Clima
    df_clima = api_meteorologica.buscar_clima_capitais()
    st.dataframe(df_clima)

with aba3:
    st.header("Teste: Sensores IoT (ESP32)")
    st.write("Lendo os sensores virtuais:")
    # Chamando a função de leitura dos sensores do ESP32
    try:
        dados_iot = esp32_sensor_sim.ler_sensores_esp32()
        st.json(dados_iot)
    except Exception as e:
        st.warning(f"Função em desenvolvimento ou nome diferente: {e}")