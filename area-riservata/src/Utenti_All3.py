import os
import requests
from collections import defaultdict
from colorama import Fore, Style, init
import random
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Inizializza colorama per l'uso dei colori nel terminale
init(autoreset=True)

# Carica le chiavi di abbonamento per l'autenticazione API dalle variabili d'ambiente
SUBSCRIPTION_KEY_GET_INSTITUTION = os.getenv("SUBSCRIPTION_KEY_INSTITUTION")
SUBSCRIPTION_KEY_GET_USERS = os.getenv("SUBSCRIPTION_KEY_GET_USERS")

# URL delle API caricate dalle variabili d'ambiente
API_URL_GET_INSTITUTION2 = os.getenv("API_URL_GET_INSTITUTION2")
API_URL_GET_USERS2 = os.getenv("API_URL_GET_USERS2")

# Dizionario che associa gli stati degli utenti a colori specifici per la stampa
STATUS_COLORS = {
    "ACTIVE": Fore.GREEN,      # Colore verde per lo stato 'ACTIVE'
    "DELETED": Fore.RED,       # Colore rosso per lo stato 'DELETED'
    "SUSPENDED": Fore.YELLOW   # Colore giallo per lo stato 'SUSPENDED'
}

# Lista di colori predefiniti per i prodotti (usati per colorare i vari prodotti nella stampa)
PRODUCT_COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Funzione per generare un colore casuale da usare se esauriamo i colori predefiniti
def generate_random_color():
    # Restituisce un codice ANSI per un colore casuale
    return f"\033[38;5;{random.randint(1, 255)}m"

# Funzione per pulire lo schermo del terminale
def clear_screen():
    # Usa 'cls' per Windows e 'clear' per Unix/Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

# Funzione per recuperare l'ID e la descrizione dell'istituzione in base al codice fiscale
def get_institution_id_and_description(tax_code):
    # Richiede l'istituzione usando il codice fiscale fornito
    response = requests.get(f"{API_URL_GET_INSTITUTION2}?taxCode={tax_code}", headers={"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY_GET_INSTITUTION})
    
    # Se la risposta è corretta (200 OK), estrae l'ID e la descrizione dell'istituzione
    if response.status_code == 200:
        institutions = response.json().get('institutions', [])
        if institutions:
            return institutions[0]['id'], institutions[0].get('description', 'N/A')  # Restituisce l'ID e la descrizione (o 'N/A' se non presente)
    
    # Stampa un errore se non riesce a recuperare l'istituzione e ritorna None
    print(f"Errore nel recupero dell'Institution ID: {response.status_code}")
    return None, None

# Funzione per recuperare la lista di utenti in base all'ID dell'istituzione
def get_users_by_institution_id(institution_id):
    # Richiede gli utenti collegati all'istituzione
    response = requests.get(f"{API_URL_GET_USERS2}{institution_id}/users", headers={"Content-Type": "application/octet-stream", "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY_GET_USERS})
    
    # Restituisce la lista degli utenti se la richiesta ha avuto successo
    return response.json() if response.status_code == 200 else print(f"Errore nel recupero degli utenti: {response.status_code}") or None

# Funzione per raggruppare gli utenti per prodotto
def group_users_by_product(users):
    # Usa defaultdict per creare una struttura dati che contiene una lista di utenti e un conteggio degli stati per prodotto
    grouped_users = defaultdict(lambda: {"users": [], "status_count": defaultdict(int)})
    
    # Itera su ogni utente e su ogni prodotto associato a quell'utente
    for user in users:
        for product in user['products']:
            # Aggiunge l'utente alla lista degli utenti per il prodotto specifico
            grouped_users[product['productId']]["users"].append({**user, **product})
            # Incrementa il conteggio dello stato (es. 'ACTIVE', 'DELETED', 'SUSPENDED') per quel prodotto
            grouped_users[product['productId']]["status_count"][product['status']] += 1
    
    return grouped_users  # Restituisce il dizionario raggruppato per prodotto

# Funzione per visualizzare un riepilogo dei prodotti e degli stati degli utenti
def display_products_summary(grouped_users):
    print("\nRiepilogo degli utenti per prodotto:")
    
    # Crea una mappa di colori per i prodotti, assegnando un colore a ciascun prodotto in modo ciclico
    product_colors_map = {product_id: PRODUCT_COLORS[idx % len(PRODUCT_COLORS)] for idx, product_id in enumerate(grouped_users)}
    
    # Itera su ciascun prodotto, stampa il numero di utenti e il riepilogo degli stati
    for idx, (product_id, data) in enumerate(grouped_users.items(), 1):
        # Crea una stringa che contiene lo stato e il numero di utenti in quello stato
        status_info = ", ".join(f"{STATUS_COLORS.get(status, '')}{status} {count}{Style.RESET_ALL}" for status, count in data["status_count"].items())
        
        # Colora la stampa del prodotto
        color = product_colors_map[product_id]
        print(f"{color}{idx}. {product_id}: {len(data['users'])} utenti ({status_info}){Style.RESET_ALL}")
    
    # Restituisce l'elenco dei product_id
    return list(grouped_users.keys())

# Funzione per visualizzare gli utenti per un prodotto specifico, raggruppati per ruolo
def display_users_for_product(grouped_users, product_id):
    # Raggruppa gli utenti per ruolo
    users_by_role = defaultdict(list)
    for user in grouped_users[product_id]["users"]:
        users_by_role[user['role']].append(user)
    
    # Stampa i dettagli degli utenti raggruppati per ruolo
    print(f"\nDettagli degli utenti per il prodotto {product_id}, raggruppati per ruolo:")
    for role, role_users in users_by_role.items():
        print(f"\nRuolo: {role}")
        for user in role_users:
            # Stampa i dettagli di ogni utente colorati in base al loro stato
            status_color = STATUS_COLORS.get(user['status'], Fore.WHITE)
            print(f"{status_color}- ID: {user['id']}, TaxCode: {user['taxCode']}, {user['name']} {user['surname']} "
                  f"(Email: {user['email']}, Role: {user['role']}, Status: {user['status']}){Style.RESET_ALL}")

# Funzione principale del programma
def main():
    # Chiede all'utente di inserire il codice fiscale
    tax_code = input("Inserisci il codice fiscale: ")
    clear_screen()  # Pulisce lo schermo dopo l'inserimento del codice fiscale
    
    # Recupera l'Institution ID e la descrizione in base al codice fiscale
    institution_id, description = get_institution_id_and_description(tax_code)
    
    if institution_id:
        # Se l'istituzione è trovata, stampa l'ID e la descrizione
        print(Fore.BLACK+(f"Institution ID trovato: {institution_id}"))
        print(Fore.RED+(f"Ente: {description}"))
        
        # Recupera gli utenti associati all'istituzione
        users = get_users_by_institution_id(institution_id)
        
        if users:
            # Raggruppa gli utenti per prodotto
            grouped_users = group_users_by_product(users)
            # Visualizza il riepilogo dei prodotti
            products = display_products_summary(grouped_users)
            
            # Chiede all'utente se vuole vedere i dettagli di un prodotto specifico
            while True:
                try:
                    choice = int(input("\nInserisci il numero del prodotto per visualizzare gli utenti (0 per uscire): "))
                    clear_screen()  # Pulisce lo schermo dopo l'inserimento del numero del prodotto
                    
                    match choice:
                        case 0:
                            # Esce dal programma
                            print("Uscita dal programma.")
                            break
                        case _ if 1 <= choice <= len(products):
                            # Visualizza gli utenti per il prodotto selezionato
                            display_users_for_product(grouped_users, products[choice - 1])
                        case _:
                            # Gestisce scelte non valide
                            print("Scelta non valida. Riprova.")
                except ValueError:
                    # Gestisce errori di input (es. l'utente non inserisce un numero valido)
                    print("Inserisci un numero valido.")
        else:
            print("Nessun utente trovato.")  # Nessun utente associato all'istituzione trovata
    else:
        print("Nessuna Institution trovata per il codice fiscale fornito.")  # Nessuna istituzione trovata con il codice fiscale fornito

# Esegue la funzione principale
if __name__ == "__main__":
    main()
