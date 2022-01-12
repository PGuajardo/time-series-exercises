import requests
import pandas as pd


# https://aphorisms.glitch.me returns a random quotation

#url = "https://python.zgulde.net/api/v1/items"
#response = requests.get(url)
#print(response.ok)


def get_all(endpoint):
    """ Read all records on all pages """
    
    if endpoint not in ["sales", "items", "stores"]:
        return "Not available from this API. Check the documentation"
    
    host = "https://python.zgulde.net/"
    api = "api/v1/"

    url = host + api + endpoint

    response = requests.get(url)

    if response.ok:
        payload = response.json()["payload"]

        # endpoint should be "items", "sales", or "stores"
        contents = payload[endpoint]

        # Make a dataframe of the contents
        df = pd.DataFrame(contents)

        next_page = payload["next_page"]

        while next_page:
            # Append the next_page url piece
            url = host + next_page
            response = requests.get(url)

            payload = response.json()["payload"]

            next_page = payload["next_page"]    
            contents = payload[endpoint]

            df = pd.concat([df, pd.DataFrame(contents)])

            df = df.reset_index(drop=True)

    return df
