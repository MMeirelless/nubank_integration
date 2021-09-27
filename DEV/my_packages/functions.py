import json
from datetime import datetime

# Funções personalizadas e variáveis globais
from my_packages.global_variable import env

# Sumarização dos valores presentes no "card_statements.json"
def summarizing_amounts():
    with open(f"{env}/data/card_statements.json", "r", encoding="utf-8") as r:
        data = json.loads(r.read())

        for transaction in range(len(data)):

            cents = str(data[transaction]["amount"])[-2:]
            value = str(data[transaction]["amount"])[:-2]

            data[transaction]["amount"] = float(value+"."+cents)

        with open(f"{env}/data/card_statements.json", "w", encoding="utf-8") as w:
            
            w.write(json.dumps(data, indent=4))

# Função responsável por atualizar os dados
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