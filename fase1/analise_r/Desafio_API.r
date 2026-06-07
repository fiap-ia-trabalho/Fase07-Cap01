library(httr)
library(jsonlite)

# Função para obter coordenadas via Nominatim
obter_coordenadas <- function(cidade, uf) {
  local <- paste(cidade, uf, "Brasil")
  url <- paste0("https://nominatim.openstreetmap.org/search?format=json&q=", URLencode(local))
  res <- GET(url, user_agent("R"))

  if (status_code(res) == 200) {
    dados <- fromJSON(content(res, "text", encoding = "UTF-8"))
    if (length(dados) > 0) {
      lat <- as.numeric(dados$lat[1])
      lon <- as.numeric(dados$lon[1])
      return(list(lat = lat, lon = lon))
    }
  }
  return(NULL)
}

# Função para traduzir weathercode
interpretar_weathercode <- function(code) {
  if (code == 0) return("Céu limpo")
  if (code %in% 1:3) return("Parcialmente nublado")
  if (code %in% 45:48) return("Neblina ou névoa")
  if (code %in% 51:57) return("Chuvisco leve a moderado")
  if (code %in% 61:67) return("Chuva leve a forte")
  if (code %in% 71:77) return("Neve leve a forte")
  if (code %in% 80:82) return("Pancadas de chuva")
  if (code %in% 85:86) return("Pancadas de neve")
  if (code == 95) return("Tempestade")
  if (code %in% 96:99) return("Tempestade com granizo")
  return("Condição desconhecida")
}

# Input do usuário
cidade <- readline(prompt = "Digite o nome da cidade: ")
uf <- readline(prompt = "Digite a sigla do estado (UF): ")

# Busca coordenadas
coord <- obter_coordenadas(cidade, uf)

if (!is.null(coord)) {
  latitude <- coord$lat
  longitude <- coord$lon

  # Monta a URL do clima com variáveis adicionais
  url_clima <- paste0("https://api.open-meteo.com/v1/forecast?latitude=", latitude,
                      "&longitude=", longitude,
                      "&current_weather=true&hourly=relative_humidity_2m,pressure_msl")

  # Faz a requisição
  res <- GET(url_clima)

  # Processa os dados
  if (status_code(res) == 200) {
    dados <- fromJSON(content(res, "text", encoding = "UTF-8"))
    clima <- dados$current_weather

    # Formata a data
    data_formatada <- format(as.POSIXct(clima$time, format = "%Y-%m-%d"), "%d/%m/%Y")

    # Busca umidade e pressão do horário atual
    hora_atual <- clima$time

    # Interpreta condição climática
    condicao <- interpretar_weathercode(clima$weathercode)

    # Exibe os dados
    cat("\n📍 Local:", cidade, "-", uf, "\n")
    cat("🕒 Data:", data_formatada, "\n")
    cat("🌡️ Temperatura:", clima$temperature, "°C\n")
    cat("🌬️ Vento:", clima$windspeed, "km/h\n")
    cat("🧭 Direção do vento:", clima$winddirection, "°\n")
    cat("☁️ Condição:", condicao, "\n")
  } else {
    cat("❌ Erro na requisição do clima. Status:", status_code(res), "\n")
  }

} else {
  cat("🚫 Não foi possível localizar a cidade informada.\n")
}