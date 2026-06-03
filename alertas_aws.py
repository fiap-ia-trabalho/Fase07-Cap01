import boto3
from config_aws import *

# Inicializa cliente SNS
sns = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

def enviar_alerta(mensagem: str, assunto: str = "FarmTech - Alerta"):
    """Publica uma mensagem no tópico SNS."""
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


def verificar_sensores(ph: float, umidade: float, praga_detectada: bool):
    """
    Regras de alerta definidas pelo grupo.
    Recebe leituras das Fases 1, 3 ou resultado da Fase 6.
    """
    alertas = []

    # Regra 1 — pH fora do ideal (Fase 1 / Fase 3)
    if ph < 5.5:
        alertas.append(
            f"⚠️ pH BAIXO detectado: {ph:.1f}\n"
            "Ação: Aplicar calcário para corrigir acidez do solo."
        )
    elif ph > 7.0:
        alertas.append(
            f"⚠️ pH ALTO detectado: {ph:.1f}\n"
            "Ação: Verificar salinidade e aplicar corretivo adequado."
        )

    # Regra 2 — Umidade baixa (Fase 3)
    if umidade < 30.0:
        alertas.append(
            f"💧 UMIDADE CRÍTICA: {umidade:.1f}%\n"
            "Ação: Acionar irrigação imediatamente na zona afetada."
        )

    # Regra 3 — Praga detectada pelo YOLO (Fase 6)
    if praga_detectada:
        alertas.append(
            "🐛 PRAGA DETECTADA pela visão computacional.\n"
            "Ação: Acionar equipe de defensivos agrícolas urgente."
        )

    # Dispara um único e-mail consolidado se houver alertas
    if alertas:
        corpo = "=== ALERTAS FARMTECH ===\n\n" + "\n\n".join(alertas)
        enviar_alerta(corpo, assunto="FarmTech - Ação Necessária")
    else:
        print("✅ Todos os sensores dentro dos parâmetros normais.")


# Teste rápido (pode remover depois)
if __name__ == "__main__":
    verificar_sensores(ph=5.1, umidade=25.0, praga_detectada=True)
