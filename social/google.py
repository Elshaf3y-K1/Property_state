import base64
import json

class Google:
    @staticmethod
    def validate(auth_token: str) -> dict:
        try : 
            parts = auth_token.split(".")
            if len(parts) != 3:
                raise Exception("Incorrect id token format")

            payload = parts[1]
            padded = payload + '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(padded)
            user = json.loads(decoded)
            return user
        except :
            return "The token is invalid or expired."
