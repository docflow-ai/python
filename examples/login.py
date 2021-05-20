from docflow import APIClient


email = "branislav@vaculciak.sk"
password = "spustiwacco"
with APIClient(email=email, password=password) as api:
    if api.is_logged_in():
        print("You are logged in")

        for owner_id, data in api.get_owners():
            print(owner_id, " -> ", data.get('name'))
    else:
        raise Exception("You are not logged in!!!")
