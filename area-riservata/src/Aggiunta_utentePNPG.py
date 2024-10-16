import requests
import json
import pnpg
#VPN ACCESA PER LANCIARE QUESTO SCRIPT

token=pnpg.codice_token
def inserisci_utente(institution_id, fiscal_code, institution_email, family_name, name, product_id, role, product_roles, institution_description, has_to_send_email, token):
    url = pnpg.endpoint
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "institutionId": institution_id,
        "user": {
            "fiscalCode": fiscal_code,
            "institutionEmail": institution_email,
            "familyName": family_name,
            "name": name
        },
        "product": {
            "productId": product_id,
            "role": role,
            "productRoles": product_roles
        },
        "institutionDescription": institution_description,
        "hasToSendEmail": has_to_send_email
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print("Utente inserito con successo!")
    else:
        print(f"Errore nell'inserimento dell'utente: {response.status_code}")
        print(response.text)

def main():
    token 
    institution_id = input("Inserisci l'ID dell'impresa: ")
    fiscal_code = input("Inserisci il codie fiscale dell'utente: ")
    institution_email = input("Inserisci la mail dell'utente: ")
    family_name = input("inserisci il cognome dell'utente: ")
    name = input("inserisci il nome dell'utente: ")
    product_id = "prod-pn-pg"
    role = "SUB_DELEGATE"
    product_roles = ["pg-admin"]
    institution_description = input("inserisci la ragione sociale dell'impresa: ")
    has_to_send_email = "false"

    inserisci_utente(institution_id, fiscal_code, institution_email, family_name, name, product_id, role, product_roles, institution_description, has_to_send_email, token)

if __name__ == "__main__":
    main()
