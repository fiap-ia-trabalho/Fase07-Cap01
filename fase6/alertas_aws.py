import os

import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.environ.get(
    "SNS_TOPIC_ARN",
    "arn:aws:sns:us-east-1:111225937941:notificacoes-email",
)

try:
    from config_aws import (
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_SESSION_TOKEN,
        AWS_REGION as _REGION,
        SNS_TOPIC_ARN as _ARN,
    )

    AWS_REGION = _REGION
    SNS_TOPIC_ARN = _ARN
    client_kwargs = {
        "region_name": AWS_REGION,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
    if AWS_SESSION_TOKEN:
        client_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    sns = boto3.client("sns", **client_kwargs)
except ImportError:
    sns = boto3.client("sns", region_name=AWS_REGION)


def enviar_alerta(mensagem: str, assunto: str = "FarmTech - Alerta"):
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=mensagem,
            Subject=assunto
        )
        print(f"Alerta enviado! MessageId: {response['MessageId']}")
        return True
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")
        return False


def verificar_sensores(umidade: float, ph: float, praga_detectada: bool = False):
    """
    Usa os mesmos nomes e limites do sketch.ino (Fase 3)
    e do treinar_modelo.py (Fase 4).
    """
    alertas = []

    # --- pH (mesmas faixas do analisar_ph() no sketch.ino) ---
    if ph < 4.8:
        alertas.append(
            f"⚠️ pH BAIXO: {ph:.2f}\n"
            "Ação: Solicitar K (Potássio) — mesmo critério do ESP32."
        )
    elif ph > 6.2 and ph < 8.0:
        alertas.append(
            f"⚠️ pH MÉDIO-ALTO: {ph:.2f}\n"
            "Ação: Solicitar N (Nitrogênio)."
        )
    elif ph >= 8.0:
        alertas.append(
            f"⚠️ pH ALTO: {ph:.2f}\n"
            "Ação: Solicitar P (Fósforo)."
        )

    # --- Umidade (mesmos limites UMI_ON/UMI_OFF do sketch.ino) ---
    if umidade <= 40.0:
        alertas.append(
            f"💧 UMIDADE CRÍTICA: {umidade:.1f}%\n"
            "Ação: Acionar bomba de irrigação (limite UMI_ON=40%)."
        )

    # --- Visão computacional Fase 6 ---
    if praga_detectada:
        alertas.append(
            "🐛 PRAGA DETECTADA pelo modelo YOLO (Fase 6).\n"
            "Ação: Acionar equipe de defensivos agrícolas."
        )

    if alertas:
        corpo = "=== ALERTAS FARMTECH ===\n\n" + "\n\n".join(alertas)
        enviar_alerta(corpo, assunto="FarmTech - Ação Necessária")
    else:
        print("✅ Sensores dentro dos parâmetros normais.")


if __name__ == "__main__":
    # Teste com valores reais dos seus limites
    verificar_sensores(umidade=38.5, ph=4.5, praga_detectada=False)
