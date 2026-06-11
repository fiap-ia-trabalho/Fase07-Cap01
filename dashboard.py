import streamlit as st
from fase1 import calculo_area
from fase1 import api_meteorologica
from fase2 import banco_dados
from fase3 import esp32_sensor_sim
from fase6 import alertas_aws
from fase6 import yolo_derector

st.title("🚜 Teste de Integração - Fases 1, 2, 3, 5 e 6")

aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Fase 1 (Cálculos)", "Fase 2 (Banco/Clima)", "Fase 3 (IoT)",
    "Fase 5 (Alertas)", "Fase 6 (YOLO)"
])

with aba1:
    st.header("Teste: Cálculos de Área e Insumo")
    st.write("Simulando os dados que viriam do input do usuário:")
    st.sidebar.header("Parâmetros")

    umidade = st.number_input("Umidade", value=0.0)
    ph = st.number_input("Ph", value=0.0)
    forma = st.selectbox("Qual formato da área?", ("Retângulo", "Triângulo", "Círculo"))
    cultivo = st.selectbox("Qual cultura que você vai utilizar?",("cafe", "milho"))
    produto = st.selectbox("Qual produto você vai utilizar?",("NPK", "Fertilizante", "Inseticida"))
    dose = st.number_input("Qual dose você vai utilizar?", value=0.0)


    try:
        st.write(f"Resultado do cálculo de área e insumo:")
        resultado_f1 = calculo_area.processar_dados_plantio(cultivo, forma, umidade, ph, produto, dose)
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

with aba4:
    st.header("Enviar alerta via SNS")
    alerta = st.text_input("Digite o alerta:")
    
    if st.button("Enviar"):
        try:
            if not alerta.strip():
                st.warning("Digite uma mensagem antes de enviar.")
            else:
                sucesso = alertas_aws.enviar_alerta(alerta)
                if sucesso:
                    st.success("Alerta enviado com sucesso!")
                else:
                    st.error("Falha ao enviar o alerta.")
        except Exception as e:
            st.warning(f"Função em desenvolvimento ou nome diferente: {e}")

with aba5:
    st.header("Detecção de Pragas (YOLOv5)")
    imagem_enviada = st.file_uploader(
        "Envie uma imagem da planta",
        type=["jpg", "jpeg", "png"],
    )

    if imagem_enviada and st.button("Analisar imagem"):
        try:
            with st.spinner("Analisando imagem..."):
                resultado = yolo_derector.detectar_imagem(imagem_enviada)

            if resultado["praga_detectada"]:
                st.error("Praga ou doença detectada na imagem!")
            else:
                st.success("Nenhuma praga detectada.")

            st.write(f"Total de detecções: {resultado['total_deteccoes']}")
            st.json({
                "praga_detectada": resultado["praga_detectada"],
                "deteccoes": resultado["deteccoes"],
            })
            st.image(resultado["imagem_anotada"], caption="Imagem com detecções")
        except Exception as e:
            st.warning(f"Erro ao processar imagem: {e}")