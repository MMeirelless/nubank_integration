# Biblioteca Nubank
from pynubank import Nubank, MockHttpClient

# Funções personalizadas e variáveis globais
from my_packages.global_variable import env
from my_packages.functions import summarizing_amounts, update_data

# Definindo que iremos 
nu = Nubank(MockHttpClient())

# Essa linha funciona porque não estamos chamando o servidor do Nubank ;) 
# Utilizando essa autenticação nós conseguimos coletar dados falsos para testarmos o quanto quisermos
nu.authenticate_with_cert("qualquer-cpf", "qualquer-senha", f"{env}/certificado/cert.p12")

# Variables
metrics = [
    "account_statements",
    "card_statements",
    "account_balance",
    "account_investments_details",
    "account_investments_yield"
    ]

# Coletando todas as métricas listadas
for metric in metrics:
    update_data(metric, nu)

summarizing_amounts()
