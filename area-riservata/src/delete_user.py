import requests

from display_message import print_institution, print_error, print_ok_message, print_ko_message, print_user_info
from leggi_env import ConfigEnv

config = ConfigEnv().loadConfig();

def get_initial_data():
    url = config.endpoints.users_url
    headers = {
        "Ocp-Apim-Subscription-Key": config.apikey.user_info,
        "Content-Type": "application/json"
    }

    fiscal_code = input("Inserisci il codice fiscale per verificare l'utente da cancellare: ")
    data = {
        "fiscalCode": fiscal_code
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            user_info = data.get("user")
            institutions = data.get("onboardedInstitutions", [])
            print("Ecco i dati dell'utente:", user_info)
            return user_info, institutions
        else:
            print_error(response)
            return None, []

    except Exception as e:
        print(f"Errore durante la richiesta iniziale: {e}")
        return None, []

def display_institutions(institutions):
    print("\nL'utente ha le seguenti istituzioni dove l'utenza è attiva:")
    for index, institution in enumerate(institutions, start=1):
        # institution_id = institution.get("id")
        description = institution.get("description")
        product_info = institution.get("productInfo", {})
        state = institution.get("state")
        product_id = product_info.get("id")
        role = product_info.get("role")
        print_institution(index, state, description, product_id, role)

def get_active_institutions(institutions):
    return [inst for inst in institutions if inst.get("state") == "ACTIVE"]

def search_institutions_by_description(institutions, search_description):
    return [
        inst for inst in institutions if inst.get("state") == "ACTIVE" and search_description.lower() in inst.get("description", "").lower()
    ]

def display_matching_institutions(matching_institutions):
    print("\nIstituzioni corrispondenti alla ricerca:")
    for index, matching_institution in enumerate(matching_institutions, start=1):
        # matching_institution_id = matching_institution.get("id")
        matching_description = matching_institution.get("description")
        matching_product_info = matching_institution.get("productInfo", {})
        matching_state = matching_institution.get("state")
        matching_product_id = matching_product_info.get("id")
        matching_role = matching_product_info.get("role")
        print_institution(index, matching_description, matching_role, matching_state, matching_product_id)

def put_user_status(user_id, institution_id, product_Id):
    url = f"{config.endpoints.users2_url}/{user_id}/status"
    headers = {
        "Ocp-Apim-Subscription-Key": config.apikey.delete
    }

    # Assicurati che product_Id sia tra le opzioni valide
    if product_Id not in ["prod-pagopa", "prod-interop", "prod-pn", "prod-io","prod-io-sign"]:
        raise ValueError("product_Id non valido. Scegli tra le opzioni disponibili.")

    params = {
        "status": "DELETED",
        "productId": product_Id,
        "institutionId": institution_id,
        "user_id": user_id
    }

    try:
        response = requests.put(url, params=params, headers=headers)

        if response.status_code == 204:
            print_ok_message(f"Utente {user_id} è stato cancellato con successo.", response.status_code)
        else:
            print_ko_message(f"Errore nella richiesta: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Errore durante la richiesta: {e}")

def process_user_input(active_institutions, user_id):
    selected_index = input("Seleziona il numero corrispondente all'istituzione da cancellare: ")

    try:
        selected_index = int(selected_index)
        selected_institution = active_institutions[selected_index - 1]
        institution_id = selected_institution.get("id")
        selected_product_id = selected_institution.get("productInfo", {}).get("id")

        # Chiedi all'utente se desidera cancellare l'utente
        delete_user_input = input("Vuoi cancellare l'utente? (si/no): ").lower()

        if delete_user_input == "si":
            put_user_status(user_id, institution_id, selected_product_id)
        else:
            print("Operazione di cancellazione annullata.")

    except (ValueError, IndexError):
        print("Selezione non valida. Operazione di cancellazione annullata.")



user_info, institutions = get_initial_data()
print(user_info, institutions)
# Se la chiamata iniziale è andata a buon fine
if user_info is not None:
    user_id = user_info.get("id")
    print_user_info(user_info)

    # Se ci sono istituzioni
    if institutions:
        # Filtra le istituzioni attive
        active_institutions = get_active_institutions(institutions)

        # Se ci sono istituzioni attive
        if active_institutions:
            if len(active_institutions) > 10:
                search_by_description_input = input("Le istituzioni attive associate sono molte. Vuoi cercarle per Descrizione? (si/no): ").lower()

                if search_by_description_input == "si":
                    search_description = input("Inserisci la descrizione da cercare: ")
                    matching_institutions = search_institutions_by_description(active_institutions, search_description)

                    if matching_institutions:
                        display_matching_institutions(matching_institutions)
                        process_user_input(matching_institutions, user_id)
                    else:
                        print("Nessuna istituzione corrispondente trovata.")
                else:
                    process_user_input(active_institutions, user_id)
            else:
                display_institutions(active_institutions)
                process_user_input(active_institutions, user_id)
        else:
            print("L'utente non ha istituzioni attive.")
    else:
        print("L'utente non ha istituzioni associate.")
else:
    print("Errore durante la richiesta iniziale. Operazione di cancellazione annullata.")