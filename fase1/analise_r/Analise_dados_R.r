# Instalação

install.packages("dplyr")
library(dplyr)

# Extração os dados

data_farmtech <- read.csv("farmtech_base.csv", sep = ";", fileEncoding = "latin1")
head(data_farmtech)

# Análise capacidade produtiva por cultura

data_farmtech_cultura <- data_farmtech %>%
                         group_by(Cultura) %>%
                         summarize(mínimo = min(Capacidade), média = mean(Capacidade), mediana = median(Capacidade), máximo = max(Capacidade), "desvio padrão" = sd(Capacidade))

data_farmtech_cultura

# Análise consumo de insumo

data_farmtech_cultura <- data_farmtech %>%
                         group_by(Produto) %>%
                         summarize(mínimo = min(Dose), média = mean(Dose), mediana = median(Dose), máximo = max(Dose), "desvio padrão" = sd(Dose))

data_farmtech_cultura

# Análise de área

data_farmtech_cultura <- data_farmtech %>%
                         group_by(Formato) %>%
                         summarize(mínimo = min(Area), média = mean(Area), mediana = median(Area), máximo = max(Area), "desvio padrão" = sd(Area))

data_farmtech_cultura
