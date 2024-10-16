import json
import os
import requests
import Config_Add_user

subscription_key = Config_Add_user.subscription_key

# Funzione per richiedere input dall'utente con verifica di lunghezza
def get_user_input(prompt, length=None):
    while True:
        user_input = input(prompt).strip()
        if length is not None and len(user_input) != length:
            print(f"Il valore inserito deve essere necessariamente di {length} caratteri. Riprova.")
        else:
            return user_input

# Funzione per creare il nuovo JSON e salvarlo
def create_and_save_json():
    base_json = {
        "institutionTaxCode": "",
        "productId": "",
        "sendCreateUserNotificationEmail": False,
        "users": [
            {
                "email": "",
                "env": "ROOT",
                "name": "",
                "surname": "",
                "taxCode": "",
                "productRole": "admin",
                "role": "SUB_DELEGATE",
                "roleLabel": "Amministratore"
            }
        ]
    }

    base_json["institutionTaxCode"] = get_user_input("Inserisci il codice fiscale dell'ente: ", length=11)

    product_choices = ["prod-pagopa", "prod-interop", "prod-pn", "prod-io"]
    print("Scegli il productId:")
    for i, choice in enumerate(product_choices, start=1):
        print(f"{i}. {choice}")

    product_choice_index = int(get_user_input("Inserisci il numero corrispondente alla tua scelta: ")) - 1
    base_json["productId"] = product_choices[product_choice_index]

    # nome e cognome solo numeri, mail @
    while True:
        base_json["users"][0]["surname"] = get_user_input("Inserisci il cognome: ")
        if base_json["users"][0]["surname"].isalpha():
            break
        else:
            print("Il cognome deve contenere solo lettere. Riprova.")

    base_json["users"][0]["taxCode"] = get_user_input("Inserisci Codice fiscale dell'utente: ", length=16).upper()

    while True:
        base_json["users"][0]["name"] = get_user_input("Inserisci il nome: ")
        if base_json["users"][0]["name"].isalpha():
            break
        else:
            print("Il nome deve contenere solo lettere. Riprova.")

    while True:
        base_json["users"][0]["email"] = get_user_input("Inserisci Email: ")
        if "@" in base_json["users"][0]["email"]:
            break
        else:
            print("L'indirizzo email deve contenere il simbolo '@'. Riprova.")

    folder_path = "json_selfacare"
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{base_json['users'][0]['name']}_{base_json['users'][0]['surname']}.json"
    file_path = os.path.join(folder_path, file_name)

    json_data = json.dumps(base_json, indent=2)

    with open(file_path, 'w') as file:
        file.write(json_data)

    print(f"\nIl JSON è stato salvato nel file: {file_path}")

    return file_path

# Funzione per stampare il contenuto del JSON con colore verde
def print_json_content_colored(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        print("\nContenuto del file JSON:")
        print("\033[92m" + json.dumps(json_data, indent=2) + "\033[0m")  # Verde

    except Exception as e:
        print(f"Si è verificato un errore durante la stampa del JSON: {str(e)}")

# Funzione per effettuare la chiamata API POST
def post_json_data(file_path):
    base_path = "https://api.selfcare.pagopa.it/external/internal/v1"
    endpoint = "/onboarding/users"
    api_url = base_path + endpoint
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key  # Sostituisci con il valore reale
    }

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        response = requests.post(api_url, json=json_data, headers=headers)

        if response.status_code == 200:
            print("Chiamata API POST effettuata con successo.")
        else:
            print(f"Errore nella chiamata API POST. Codice di stato: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")

# Chiamata alle funzioni principali
file_path = create_and_save_json()

# Chiamata alla funzione per stampare il contenuto del JSON con colori
print_json_content_colored(file_path)

user_choice = get_user_input("Vuoi effettuare la chiamata API POST? (Si/No): ").lower()

if user_choice == "si":
    post_json_data(file_path)
else:
    print("Chiamata API POST non effettuata.")
