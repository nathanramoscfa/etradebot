import ast
import keyring

# Retrieve credentials from keyring
consumer_key = keyring.get_password("etrade", "consumer_key")
consumer_secret = keyring.get_password("etrade", "consumer_secret")
sandbox_key = keyring.get_password("etrade", "sandbox_key")
sandbox_secret = keyring.get_password("etrade", "sandbox_secret")
web_username = keyring.get_password("etrade", "web_username")
web_password = keyring.get_password("etrade", "web_password")
account_id = keyring.get_password("etrade", "account_id")
etrade_cookie = ast.literal_eval(keyring.get_password("etrade", "cookie"))
account_id_key = keyring.get_password("etrade", "account_id_key")


# Show the credentials
def show_credentials():
    print("consumer_key: " + consumer_key)
    print("consumer_secret: " + consumer_secret)
    print("sandbox_key: " + sandbox_key)
    print("sandbox_secret: " + sandbox_secret)
    print("web_username: " + web_username)
    print("web_password: " + web_password)
    print("account_id: " + account_id)
    print("etrade_cookie: " + str(etrade_cookie))
    print("account_id_key: " + account_id_key)
