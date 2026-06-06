import pandas as pd

def calcular_area(forma, dim1, dim2=0.0):
    """
    Calcula a área com base no formato geométrico.
    dim1 = largura, base ou raio.
    dim2 = comprimento ou altura (ignorado se for círculo).
    """
    if forma == "Retângulo":
        return dim1 * dim2
    elif forma == "Triângulo":
        return (dim1 * dim2) / 2
    elif forma == "Círculo":
        return 3.14 * (dim1 ** 2)
    return 0.0

def calcular_insumo(area, produto, dose_por_m2):
    """Retorna dicionário com os dados do consumo de insumos."""
    return {
        "produto": produto, 
        "dose": dose_por_m2, 
        "total": dose_por_m2 * area
    }

def capacidade_produtiva(cultura, area):
    """Retorna a estimativa de plantas/árvores de acordo com a área."""
    cultura = cultura.lower()
    if cultura == "laranja":
        return area / 18
    elif cultura == "milho":
        return area / 0.24
    elif cultura == "soja":
        return area / 0.03
    elif cultura == "café":
        return area / 4
    return 0

def processar_dados_plantio(cultura, forma, dim1, dim2, produto, dose):
    """
    Função Integradora para o Streamlit chamar ao clicar no botão "Calcular".
    """
    area = calcular_area(forma, dim1, dim2)
    insumo = calcular_insumo(area, produto, dose)
    capacidade = capacidade_produtiva(cultura, area)
    
    resultado = {
        "Cultura": cultura.capitalize(),
        "Formato Área": forma,
        "Área Total (m²)": round(area, 2),
        "Produto Aplicado": produto,
        "Dose (mL/m²)": dose,
        "Total Insumo (mL)": round(insumo["total"], 2),
        "Capacidade Produtiva (plantas)": int(capacidade)
    }
    
    return resultado

# TESTE LOCAL 

if __name__ == "__main__":
    dados_mock = processar_dados_plantio(
        cultura="café", 
        forma="Retângulo", 
        dim1=100,  
        dim2=50,   
        produto="Fertilizante NPK", 
        dose=1.5
    )
    
    print("\n--- Resultado do Processamento (Fase 1) ---")
    for chave, valor in dados_mock.items():
        print(f"{chave}: {valor}")
