# FIAP - Faculdade de Informática e Administração Paulista

<img width="2385" height="642" alt="image" src="https://github.com/user-attachments/assets/594c28cc-66ae-40ac-b8a6-8c39e6f14de4" />

# A consolidação de um sistema — Fase 7, Capítulo 1

## 👨‍🎓 Integrantes
- [CAUAN OTTO RODRIGUES SOUSA (RM567940)](https://www.linkedin.com/in/cauanotto)
- [FERNANDO A GURGEL (RM567606)](https://www.linkedin.com/in/fernando-gurgel-75aa8369)
- [IRACI MONTEIRO SOUZA (RM567544)](https://www.linkedin.com/in/iraci-souza-bab42034)
- [MARIA LUISA RODRIGUES NASCIMENTO (RM567659)](https://www.linkedin.com/in/malu-rodrigues-bb756b271)
- [RAFAELA TORRES MARTINS (RM567735)](https://www.linkedin.com/in/rafaela-torres222)

## 👩‍🏫 Professores
- **Tutor(a):** [ANA CRISTINA DOS SANTOS](https://www.linkedin.com/company/inova-fusca)
- **Coordenador(a):** [ANDRÉ GODOI](https://www.linkedin.com/in/andregodoichiovato)

---

## 📌 Contexto

A **FarmTech Solutions** é uma empresa de tecnologia voltada ao agronegócio que consolidou, ao longo de 7 fases, um ecossistema digital completo da coleta de dados em sensores físicos até dashboards inteligentes em nuvem com alertas automatizados.
 
Este repositório representa a **Fase 7: A Consolidação**, onde todos os sistemas desenvolvidos anteriormente são integrados em um único projeto Python, acessível via dashboard interativa e infraestrutura AWS.

## 🗺️ Visão Geral do Projeto — Evolução por Fases
 
```
╔══════════════════════════════════════════════════════════════════════╗
║               ECOSSISTEMA FARMTECH SOLUTIONS                        ║
╠══════════════════════════════════════════════════════════════════════╣
║  📐 FASE 1    Base de Dados + API Meteorológica + Análise R         ║
║       ↓                                                              ║
║  🗃️  FASE 2    Banco de Dados Relacional (MER/DER + Oracle)         ║
║       ↓                                                              ║
║  🤖 FASE 3    IoT com ESP32 — Sensores + Automação de Irrigação     ║
║       ↓                                                              ║
║  📊 FASE 4    Dashboard ML com Streamlit + Scikit-Learn             ║
║       ↓                                                              ║
║  ☁️  FASE 5    Cloud AWS — Segurança (ISO 27001/27002) + RDS        ║
║       ↓                                                              ║
║  👁️  FASE 6    Visão Computacional — YOLOv5 para Detecção de Pragas ║
║       ↓                                                              ║
║  🔗 FASE 7    ✅ CONSOLIDAÇÃO — Integração Total + Alertas SNS/SES  ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🆕 Melhorias Implementadas na Fase 7
 
### ✅ Dashboard Principal Integrada
 
A dashboard da Fase 4 foi completamente aprimorada para centralizar o acesso a todos os módulos do sistema:
 
| Módulo | Antes (Fase 4) | Depois (Fase 7) |
|--------|---------------|-----------------|
| **Navegação** | xxxx | xxx |
| **Dados em tempo real** | xxxx | xxx |
| **Alertas** | Ausentes | E-mail/SMS via AWS SNS + SES |
| **Visão Computacional** | xxx | xxx |
| **IoT** | xxx | Monitorado em painel dedicado |
| **Relatórios** |xxx | xxx |
 
---
 
### ✅ Integração dos Serviços por Fase
 
Cada fase pode ser acionada diretamente da dashboard ou via terminal:
 
```
farmtech/
├── main_dashboard.py          ← Ponto de entrada principal
├── fase1/
│   ├── calculo_area.py        ← Cálculos de plantio e insumos
│   ├── api_meteorologica.py   ← Integração com API de clima
│   └── analise_r/             ← Scripts R para análise estatística
├── fase2/
│   └── banco_dados.py         ← CRUD Oracle / SQLite

**preencher diretório**


```
 
---

### ✅ Serviço de Alertas AWS
 
> Implementado novo serviço de mensageria que monitora os dados dos sensores e da visão computacional, disparando alertas automáticos por **e-mail** e **SMS** para os funcionários da fazenda.
 
#### Arquitetura do Serviço de Alertas
 
```
Sensores IoT (Fase 3)         Visão Computacional (Fase 6)
      │                                  │
      ▼                                  ▼
┌─────────────────────────────────────────────────┐
│              AWS Lambda (Processamento)          │
│  - Verifica umidade < 30% → irrigar             │
│  - Detecta pH fora da faixa → corrigir          │
│  - Identifica praga na imagem → inspecionar     │
└──────────────────────┬──────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      AWS SNS      AWS SES      Dashboard
     (SMS/Push)   (E-mail)    (Notificação
                               visual)
```
 
#### Regras de Alerta Implementadas
 
| Sensor / Análise | Condição de Alerta | Ação Sugerida | Canal |
|---|---|---|---|
| Umidade do Solo (DHT22) | `< 30%` | Acionar irrigação imediata | SMS + E-mail |
| pH do Solo (LDR) | `< 5.5` ou `> 7.5` | Aplicar calcário ou enxofre | E-mail |
| Nível de Nutrientes | `< 20%` | Fertilização necessária | E-mail |
| Visão Computacional (YOLO) | Confiança praga `> 80%` | Inspecionar setor indicado | SMS + E-mail |
| Temperatura (Meteorologia) | `> 38°C` por 3h | Aumentar frequência de irrigação | E-mail |
 
#### Exemplo de E-mail de Alerta
 
```
─────────────────────────────────────────────────
  🌾 FARMTECH SOLUTIONS — ALERTA AGRÍCOLA
─────────────────────────────────────────────────
  NÍVEL: ⚠️ ATENÇÃO
  DATA/HORA: 27/05/2026 14:32
 
  📍 Setor: Talhão 3 — Soja
  🔴 Problema: Umidade do solo = 22% (abaixo do mínimo)
 
  ✅ AÇÃO RECOMENDADA:
  Acionar bomba de irrigação por 45 minutos.
  Verificar filtros do sistema antes de ligar.
 
  🔗 Acessar Dashboard: https://farmtech.aws.com
─────────────────────────────────────────────────
```

## 🏗️ Arquitetura Geral do Sistema


 xxx

 
 
## 🚀 Como Executar
 
### Pré-requisitos
 
- Python 3.10+
- pip instalado
- Conta AWS configurada (para alertas)
- Arduino IDE (opcional — para ESP32 físico)


### Instalação
 
```bash
# 1. Clone o repositório
git clone https://github.com/fiap-ia-trabalho/farmtech-fase7.git
cd farmtech-fase7
 
# 2. Crie e ative ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
 
# 3. Instale as dependências
pip install -r requirements.txt
 
# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais AWS e banco de dados
```
 
### Executando a Dashboard
 
```bash
# Iniciar dashboard principal (integra todas as fases)
streamlit run main_dashboard.py
```
 
### Executando Módulos Individualmente via Terminal
 
```bash
# Fase 1 — Cálculo de área e insumos
python fase1/calculo_area.py
 
# Fase 3 — Simulação de sensores IoT
python fase3/esp32_sensor_sim.py
 
# Fase 6 — Detecção de pragas com YOLO
python fase6/yolo_detector.py --source fase6/images/test/
 
# Fase 7 — Testar envio de alertas
python fase7/alertas_sns.py --teste
```
 
### Principais Bibliotecas
 
```
streamlit>=1.32       # Dashboard interativa
scikit-learn>=1.4     # Machine Learning
torch>=2.0            # YOLOv5 (Fase 6)
boto3>=1.34           # AWS SDK (SNS, SES, RDS)
pandas>=2.1           # Manipulação de dados
sqlalchemy>=2.0       # ORM banco de dados
python-dotenv         # Variáveis de ambiente
opencv-python         # Visão computacional
rpy2                  # Interface Python ↔ R (Fase 1)
```
 
---
 
## ☁️ Serviço de Alertas AWS — Evidências
 
> Prints e comentários da configuração na AWS estão na pasta [`/docs/aws/`](./docs/aws/) deste repositório.
 
### Serviços AWS Utilizados
 
| Serviço | Finalidade | Fase |
|---------|-----------|------|
| **EC2** | Hospedagem da dashboard Streamlit | 5 |
| **RDS (PostgreSQL)** | Banco de dados central em nuvem | 5 |
| **S3** | Armazenamento de imagens (Fase 6) | 5 |
| **SNS** | Envio de SMS de alerta | 7 |
| **SES** | Envio de e-mails de alerta | 7 |
| **Lambda** | Processamento serverless das regras de alerta | 7 |
| **CloudWatch** | Monitoramento e logs do sistema | 5 + 7 |
| **IAM** | Controle de acesso (ISO 27001) | 5 |
 
---
 
## 📊 Dataset — Visão Computacional (Fase 6)
 
```
FIAP/
├── images/
│   ├── train/      (124 imagens: 74 saudáveis + 50 doentes)
│   ├── val/        (10 imagens: 5 saudáveis + 5 doentes)
│   └── test/       (8 imagens inéditas: 4 saudáveis + 4 doentes)
├── labels/
│   ├── train/      (arquivos .txt com bounding boxes YOLOv5)
│   └── val/        (arquivos .txt com bounding boxes YOLOv5)
└── plantas.yaml    (configuração do dataset)
```
 
**Classes detectadas:**
- 🟢 `healthy` — Planta saudável
- 🔴 `diseased` — Planta com doença ou praga
---
 
## 🎬 Vídeo Demonstrativo
 
📹 [Assistir no YouTube (não listado)](xxx)
 
> Vídeo de até 10 minutos demonstrando todas as funcionalidades das Fases 1 a 7, incluindo:
> - Execução da dashboard integrada
> - Demonstração dos sensores IoT (simulados)
> - Detecção de pragas com YOLOv5
> - Disparo de alertas por SMS e e-mail via AWS
 


