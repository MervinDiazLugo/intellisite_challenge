import os


class Config():
    # Directorio Base
    basedir = os.path.abspath(os.path.join(__file__, "../.."))
    DateFormat = '%d/%m/%Y'
    HourFormat = "%H%M%S"

    # JsonData
    Json = basedir + u"/pages"

    Environment = 'DEV'

    # DIRECTORIO DE LA EVIDENCIA
    Path_Evidencias = basedir + u'/data/capturas'

    # HOJA DE DATOS EXCEL
    Excel = basedir + u'/data/DataTest.xlsx'

    if Environment == 'DEV':
        # API
        API_hostAddressBase = "http://localhost:9090/"
        USER = "user"
        PASS = "pass1234"

        API_headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
        }

        authentication_body = {"username": USER, "password": PASS, "scope": "", "client_secret": ""}

        API_body = {}
        API_subBody_dict = {}
        API_subBody_array = []

        Scenario = {
        }

    if Environment == 'TEST':
        # API
        API_hostAddressBase = "https://petstore.swagger.io/v2/"
        USER = "user"
        PASS = "pass1234"

        API_headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        API_body = {}
        API_subBody_dict = {}
        API_subBody_array = []

        Scenario = {
        }
