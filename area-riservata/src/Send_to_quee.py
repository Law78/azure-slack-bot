import requests
from leggi_env import ConfigEnv
import os



config = ConfigEnv().loadConfig();  

def main():
    contratto=input("inserisci l'id del contratto: \n")
    Institution=input("inserisci l'id dell'instituzione: \n")
    # URL dell'API
    base_url = config.endpoints.quee_url
    url = f"{base_url}?tokenId={contratto}&institutionId={Institution}"

    # Parametri della richiesta
    params = {
        "tokenId": contratto,
        "institutionId": Institution
    }
    headers = {
            "Ocp-Apim-Subscription-Key": config.apikey.delete
        }
    print("URL della richiesta:", url)

    try:
        # Effettua la richiesta GET all'API
        response = requests.get(url, headers=headers)

        # Verifica se la richiesta è andata a buon fine (codice di stato 200)
        if response.status_code == 200:
            # Stampa la risposta
            print("Risposta dall'API:")
            print(response.json())
        else:
            print(f"Errore nella richiesta: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Si è verificato un errore durante la richiesta: {e}")
        

if __name__ == "__main__":
    main()
