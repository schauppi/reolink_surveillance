import json

class CredentionHandler():

    def load_credentials(cam: int):
        
        credentials = open("./credentials.json")
        credentials = json.load(credentials)

        username = credentials["credentials"][cam]["username"]
        password = credentials["credentials"][cam]["password"]
        ip = credentials["credentials"][cam]["ip"]

        return username, password, ip