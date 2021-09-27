# Nubank Integration
[![Python package](https://github.com/andreroggeri/pynubank/actions/workflows/build.yml/badge.svg)](https://github.com/andreroggeri/pynubank/actions/workflows/build.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pynubank)

Melhore o controle financeiro da sua NuConta utilizando a biblioteca [pynubank](https://github.com/andreroggeri/pynubank)

## main.py
Responsável por iniciar uma conexão com o Nubank e executar as funções para atualizar os dados.

### metrics
Defina todas as métricas que você deseja atualizar nessa variável. Caso a métrica que você queira atualizar não esteja listada, será necessário adiciona-la no "functions.py" e posteriormente na lista "metrics".

### Autenticação
Na documentação da biblioteca é explicado como podemos autenticar o código para realizar uma coleta real, [acesse aqui](https://github.com/andreroggeri/pynubank#autentica%C3%A7%C3%A3o) para saber mais. 

> :warning:  **Atenção**: Abrimos a conexão utilizando o "MockHttpClient()" (linha 11), sendo assim, qualquer autenticação que utilizarmos irá funcionar,
pois não estamos coletando dados reais.

```python
# main.py

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
```

## functions.py

Funções utilizadas em outros scripts.

### summarizing_amounts()
Por algum motivo a coleta da métrica "card_statements" retorna os valores(amounts) sem pontuação, essa função formata todos os valores principais do arquivo.

```python
def summarizing_amounts():
    with open(f"{env}/data/card_statements.json", "r", encoding="utf-8") as r:
        data = json.loads(r.read())

        for transaction in range(len(data)):

            cents = str(data[transaction]["amount"])[-2:]
            value = str(data[transaction]["amount"])[:-2]

            data[transaction]["amount"] = float(value+"."+cents)

        with open(f"{env}/data/card_statements.json", "w", encoding="utf-8") as w:
            
            w.write(json.dumps(data, indent=4))
```

### update_data()
Função responsável por atualizar os dados, listei as principais métricas que podem ser extraídas, mas não todas, vale dar uma olhada :).

```python
def update_data(metric, nu):

    # Extrato da NuConta
    if metric == "account_statements":
        account_statements_file = open(f"{env}/data/account_statements.json", "w", encoding="utf-8") 
        account_statements_data = json.dumps(nu.get_account_statements(), indent=4)
        account_statements_file.write(account_statements_data)
        account_statements_file.close()

    # Extrato do Cartão de Crédito
    elif metric == "card_statements":
        card_statements_file = open(f"{env}/data/card_statements.json", "w", encoding="utf-8") 
        card_statements_data = json.dumps(nu.get_card_statements(), indent=4)
        card_statements_file.write(card_statements_data)
        card_statements_file.close()

    # Saldo atual da conta
    elif metric == "account_balance":
        account_balance_file = open(f"{env}/data/account_balance.csv", "a", encoding="utf-8") 
        account_balance_data = json.dumps(nu.get_account_balance(), indent=4)
        account_balance_file.write(datetime.today().strftime("%d/%m/%Y") + ", " + account_balance_data + "\n")
        account_balance_file.close()

    # Detalhe dos investimentos
    elif metric == "account_investments_details":
        account_investments_details_file = open(f"{env}/data/account_investments_details.json", "w", encoding="utf-8") 
        account_investments_details_data = json.dumps(nu.get_account_investments_details(), indent=4)
        account_investments_details_file.write(account_investments_details_data)
        account_investments_details_file.close()

    # Rendimento dos investimentos
    elif metric == "account_investments_yield":
        account_investments_yield_file = open(f"{env}/data/account_investments_yield.json", "w", encoding="utf-8") 
        account_investments_yield_data = json.dumps(nu.get_account_investments_yield(), indent=4)
        account_investments_yield_file.write(account_investments_yield_data)
        account_investments_yield_file.close()

    else:
        print("INVALID METRIC")
```

## global_variables.py

Variáveis utilizadas em outros scripts.
```python
#global_variables.py

# Variáveis globais, utilizadas em mais de 1 script
env = "DEV"
```

### env
Inicialmente essa variável foi pensada e criada com o intuito de controlar o "ambiente", separando por pastas eu criei o seguinte diretório:
![Diretórios](https://github.com/MMeirelless/Nubank-Integration/blob/main/DEV/Imagens/diret%C3%B3rios.jpg)<br />
Dessa forma foi mais fácil de separar as consultas reais das testes.

## Power BI
> :warning:  **Atenção**: Quando você for utilizar o pbix na sua máquina será necessário atualizar as bases, pois o diretório irá mudar. 
### Atualizando os dados
1- Execute o main.py)<br />
2- Clique em Atualizar(Refresh) dentro do Power BI
![Diretórios](https://github.com/MMeirelless/Nubank-Integration/blob/main/DEV/Imagens/atualizando_dados.jpg)<br />

### Resultado
![Diretórios](https://github.com/MMeirelless/Nubank-Integration/blob/main/DEV/Imagens/controle_de_saidas.jpg)<br />
