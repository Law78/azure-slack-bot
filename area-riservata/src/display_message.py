from colorama import init, Fore, Style
import json

# colorama
init(autoreset=True)

def print_error_response(response):
    print(Fore.RED + f"Errore nella richiesta. Codice di stato: {response.status_code}")
    print("Testo dell'errore:", response.text)

def print_error(message):
    print(Fore.RED + message)

def print_formatted_json(data):
    print(Fore.GREEN + json.dumps(data, indent=2, ensure_ascii=False))

def print_ok_message(data, status_code):
    print(Fore.GREEN + data + Style.RESET_ALL, status_code)

def print_ko_message(data, status_code):
    print(Fore.RED + data + Style.RESET_ALL, status_code)

def print_product_users(product_choice,institution_name,institution_id ):
  print(f"Ecco gli utenti per il prodotto '{Fore.GREEN}{product_choice}{Fore.RESET}' per l'ente '{Fore.RED}{institution_name}{Fore.RESET}' ({Fore.RED}{institution_id}{Fore.RESET}):")

def print_institution(index, state, description, product_id, role):
    print(f"{index}. Ente: {Fore.RED}{description}{Style.RESET_ALL}, Stato: {Fore.RED}{state}{Style.RESET_ALL}, Product ID: {Fore.RED}{product_id}{Style.RESET_ALL}, Ruolo: {Fore.RED}{role}{Style.RESET_ALL}")

def print_matching_institutions(index, matching_description, matching_role, matching_state, matching_product_id):
    print(f"{index}.Ente: {Fore.RED}{matching_description}{Style.RESET_ALL}, Stato: {Fore.RED}{matching_state}{Style.RESET_ALL}, Product ID: {Fore.RED}{matching_product_id}{Style.RESET_ALL}, Ruolo: {Fore.RED}{matching_role}{Style.RESET_ALL}")

def print_user_info(user_info):
    print("Informazioni sull'utente:")
    print(f"ID Utente: {Fore.GREEN}{user_info.get('id')}{Style.RESET_ALL}")
    print(f"Nome Utente: {Fore.GREEN}{user_info.get('name')}{Style.RESET_ALL}")
    print(f"Cognome Utente: {Fore.GREEN}{user_info.get('surname')}{Style.RESET_ALL}")