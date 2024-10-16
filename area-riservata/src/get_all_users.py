import requests
import os
from leggi_env import ConfigEnv
from display_message import print_error_response, print_error, print_formatted_json, print_product_users

config = ConfigEnv().loadConfig();

# Definiamo la chiave di supporto direttamente qui nel file principale
support_key = config.apikey.user_info

def clear_screen():
    # Semplicemente fa un clear dello screen
    os.system('clear')

def get_institution_id_by_tax_code(tax_code):

    url = f"{config.endpoints.institutions_url}/?taxCode={tax_code}"
    headers = {
        "Ocp-Apim-Subscription-Key": support_key,  # Utilizza solo la chiave di supporto
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Estrai l'ID dell'istituzione dalla risposta JSON
            if data.get("institutions"):
                institution_id = data["institutions"][0]["id"]
                return institution_id
            else:
                print_error(f"Nessuna adesione trovata per l'ente con il codice fiscale '{tax_code}'.")
                return None
        else:
            print_error_response(response)

    except Exception as e:
        print_error(f"Errore durante la richiesta API: {str(e)}")

def get_pagopa_users(institution_id, product_choice, user_id_for_auth=None):
    url = f"{config.endpoints.institutions_url}/{institution_id}/users"

    headers = {
        "Ocp-Apim-Subscription-Key": product_choice,  # Utilizza la chiave specifica del prodotto
    }

    if user_id_for_auth:
        url += f"?userIdForAuth={user_id_for_auth}"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            institution_name = get_institution_name(institution_id)
            print_product_users(product_choice,institution_name,institution_id )
            # Estrai l'ID dell'utente e chiama un'altra API per ottenere ulteriori informazioni sull'utente
            count = 0
            for user in data:
                print_user_info(user, institution_id, product_choice)  # Passa il prodotto scelto come argomento
                count += 1
                if count % 7 == 0:  # Stampa solo 5 risultati alla volta
                    if input("Premi INVIO per visualizzare ulteriori risultati, o 'q' per uscire: ").lower() == 'q':
                        break
            return count

        else:
            print_error_response(response)

    except Exception as e:
        print_error(f"Errore durante la richiesta API: {str(e)}")

def get_institution_name(institution_id):
    institution_info_url = f"{config.endpoints.institutions_url}/{institution_id}"

    headers = {
        "Ocp-Apim-Subscription-Key": support_key,  # Utilizza solo la chiave di supporto
    }

    try:
        response = requests.get(institution_info_url, headers=headers)

        if response.status_code == 200:
            institution_info = response.json()
            return institution_info.get("description", f"Nome istituzione non disponibile per ID: {institution_id}")
        else:
            return f"Errore nella richiesta per ottenere il nome dell'istituzione. Codice di stato: {response.status_code}"

    except Exception as e:
        return f"Errore durante la richiesta per ottenere il nome dell'istituzione: {str(e)}"

def print_user_info(user, institution_id, product_choice):
    url = f"{config.endpoints.users_url}/{user['id']}"
    params = {
        "institutionId": institution_id
    }


    headers = {
        "Ocp-Apim-Subscription-Key": product_choice,  # Utilizza la chiave specifica del prodotto
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            user_info = response.json()
            user['fiscalCode'] = user_info.get("taxCode")
            print_formatted_json([user])  # Stampiamo direttamente l'utente aggiungendo il codice fiscale
        else:
            print_error_response(response)

    except Exception as e:
        print_error(f"Errore durante la richiesta API: {str(e)}")



def get_product_choice():
    products = [a for a in dir(config.productkey) if not a.startswith('__')]
    while True:
        print("Scegli il prodotto per il quale vuoi verificare l'ente:")
        index = 1
        ProductKeyList = []

        for key in products:
            if key != "support_key":
                print(f"{index}. {key}")
                ProductKeyList.append(getattr(config.productkey, key))
                index += 1

        product_choice = input("Inserisci il numero corrispondente al prodotto: ")
        if product_choice.isdigit():
            product_choice_index = int(product_choice) - 1
            product_choice_key = ProductKeyList[product_choice_index]
            return product_choice_key
        print("Per favore, inserisci un numero valido corrispondente a una delle opzioni di prodotto disponibili.")

# Input dell'utente per il codice fiscale dell'istituzione
tax_code = input("Inserisci il codice fiscale dell'istituzione: ")

# Ottieni l'ID dell'istituzione

institution_id = get_institution_id_by_tax_code(tax_code)

if institution_id:
    # Scelta del prodotto
    product_choice = get_product_choice()

    clear_screen()
    count = get_pagopa_users(institution_id, product_choice)
    if count is None:
        print_error(f"Nessun utente trovato per il prodotto '{product_choice}' per l'ente con il codice fiscale '{tax_code}'.")
    else:
        print(f"Il totale degli utenti per l'ente è: {count}")
