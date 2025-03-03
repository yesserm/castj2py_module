import requests

URL = "https://carriers.dentalautomation.ai/api/"
URL_API = "https://carriersync.dentalautomation.ai/api/"
Token = ""

# inicio de sesion en CCC
def sigin():
    global URL, Token
    credentials = {"username": "user", "password": "pass"}
    response = requests.post(URL + "signin", json=credentials)
    if response.status_code == 200:
        Token = response.json()["token"]
        print("\n TOKEN", Token)
    else:
        print("Sigin failed", response.status_code)

# Se obtiene el id del Bot
def get_id_bot(bot_name):
    global URL_API, Token
    bot_id = "None"
    if Token == "":
        sigin()
    headers = {"x-access-token": Token}
    response = requests.get(URL_API + "v1/bots", headers=headers)
    if response.status_code == 200:
        for bot in response.json()["data"]:
            if bot["botName"] == bot_name:
                bot_id = bot["_id"]
                return bot_id
 
    else:
        print("Get id bot failed", response.status_code)

# Se obtienen los archivos json de los updates del Bot
def get_updates_bot(bot_id):
    global URL, Token
    list_files = []
    headers = {"x-access-token": Token}
    response = requests.get(URL + "bots/" + bot_id, headers=headers)
    if response.status_code == 200:
        for update in response.json()["updates"]:
            if update["name"].endswith(".json"):
                list_files.append(update["name"])
        return list_files
    else:
        print("Get updates bot failed", response.status_code)

# Se obtiene el contenido de un archivo json del Bot
def get_file_bot(file_name):
    global URL, Token
    headers = {"x-access-token": Token}
    response = requests.get(URL + "updates/file/" + file_name, headers=headers)
    if response.status_code == 200:
        return response.json()





