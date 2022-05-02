# -*- coding: utf-8 -*-
import datetime
import json
import random
import re
import string
import time

import objectpath
import pytest
import requests

from functions.GlobalConfig import Config

diaGlobal = time.strftime("%Y-%m-%d")  # formato aaaa/mm/dd
horaGlobal = time.strftime("%H%M%S")  # formato 24 houras
Scenario = {}


class Functions:

    def __init__(self):
        self.var = "Hola Mundo"
        self.conf = Config

    def sumas(self, number1, number2):
        self.result = int(number1) + int(number2)
        return self.result

    def resultscheck(self, checking):
        assert self.result == int(
            checking), f'el resultado no es el correcto, se esperaba {checking} pero se recibio {self.result}'

    def ReplaceWithContextValues(self, text):
        PatronDeBusqueda = r"(?<=Scenario:)\w+"
        variables = re.findall(str(PatronDeBusqueda), text, re.IGNORECASE)
        self.N = 0
        for variable in variables:
            if variable == 'today':
                dateToday = str(datetime.date.today().strftime("%Y-%m-%d"))
                text = re.sub('(Scenario:)' + variable, dateToday, text, re.IGNORECASE)
                continue
            text = re.sub('(Scenario:)' + variable, Config.Scenario[variable], text, re.IGNORECASE)
        return text

    def saveScenarioContext(self, variable, text):
        Config.Scenario[variable] = text
        print(Config.Scenario)
        print("Se almaceno el valor " + variable + " : " + Config.Scenario[variable])

    def ReplaceWithQueryValues(self, text):
        PatronDeBusqueda = r"(?<=Query:)\w+"
        variables = re.findall(str(PatronDeBusqueda), text, re.IGNORECASE)
        for variable in variables:
            text = re.sub('Query:' + variable, str(self.QUERY[variable]), text, re.IGNORECASE)
        return text

    def get_full_host(self, _PartHost):
        _RegexPartHost = str(Functions.ReplaceWithContextValues(self, _PartHost))
        self._endpoint = Config.API_hostAddressBase + _RegexPartHost
        print(self._endpoint)
        return self._endpoint

    def do_a_get(self):
        new_header = Config.API_headers
        self._response = requests.get(self._endpoint, headers=new_header)
        return self._response

    def print_api_response(self):
        if self._response.text != "":
            self.json_response = json.loads(self._response.text)
            print(json.dumps(self.json_response, indent=3))
        else:
            print("Endpoint response is " + str(self._response.status_code))

    def response_is(self, code):
        print("status code is: " + str(self._response.status_code))
        assert self._response.status_code == int(
            code), f'El codigo de respuesta no es el esperado {self._response.status_code} != {code}'

    def response_is_200(self):
        print("status code is: " + str(self._response.status_code))
        assert self._response.status_code == 200, f'El codigo de respuesta no es el esperado {self._response.status_code} != 200'

    def response_is_404(self):
        print("status code is: " + str(self._response.status_code))
        assert self._response.status_code == 404, f'El codigo de respuesta no es el esperado {self._response.status_code} != 404'

    def set_body_values(self, entity, value):
        def set_ramdon_values(self):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(6))

        if value.lower() == "random":
            value = set_ramdon_values(self)
            if entity.lower() == "email":
                value = set_ramdon_values(self) + "@amazon.com"
            if entity.lower() == "password":
                value = set_ramdon_values(self) + set_ramdon_values(self)

        value = Functions.ReplaceWithQueryValues(self, value)
        Config.API_body[entity] = str(value)
        Functions.saveScenarioContext(self, entity, value)
        self._new_body = Config.API_body
        print(self._new_body)
        return self._new_body

    def set_sub_body_dict_values(self, entity, value):
        Config.API_subBody_dict[entity] = value
        print((json.dumps(Config.API_subBody_dict, indent=4)))
        return Config.API_subBody_dict

    def set_sub_body_dict(self, key):
        Config.API_body[key] = Config.API_subBody_dict
        print((json.dumps(self._new_body, indent=4)))
        Config.API_subBody_dict = {}
        return Config.API_subBody_dict

    def set_sub_body_array_values(self, value):
        Config.API_subBody_array.append(value)
        print(Config.API_subBody_array)
        return Config.API_subBody_array

    def set_sub_body_array(self, key):
        Config.API_body[key] = Config.API_subBody_array
        print((json.dumps(self._new_body, indent=4)))
        Config.API_subBody_array = []
        return Config.API_subBody_array

    def get_json_inData(self, file):
        json_path = self.Json_Data + file + '.json'
        try:
            with open(json_path, "r") as read_file:
                self.json_strings = json.loads(read_file.read())
                print("get_json_inData: " + file)
                return self.json_strings
        except FileNotFoundError:
            self.json_strings = False
            pytest.skip(u"get_json_file: No se encontro el Archivo " + file)

    def set_initial_json_body(self, file):
        self.New_Body = Functions.get_json_inData(self, file)
        Config.API_body = self.New_Body
        print((json.dumps(Config.API_body, indent=4)))

    def do_a_put(self):
        new_header = Config.API_headers
        print(self._new_body)
        self._response = requests.put(self._endpoint, headers=new_header, data=json.dumps(self._new_body))
        return self._response

    def do_a_post(self):
        new_header = Config.API_headers
        print(self._new_body)
        self._response = requests.post(self._endpoint, headers=new_header, data=json.dumps(self._new_body))
        return self._response

    def assert_response_expected(self, entity, expected, subPath=0):
        self.json_response = json.loads(self._response.text)
        PATH_VALUE = self.json_response[entity]

        if expected == "NOT NULL":
            assert str(PATH_VALUE) is not None, f"Value is Null: {PATH_VALUE} != {expected}"
            return

        elif expected == "NULL":
            assert str(PATH_VALUE) is None, f"Value is not Null: {PATH_VALUE} != {expected}"
            return

        if expected == "NUMERIC":
            assert isinstance(PATH_VALUE, int), f"Value is not numeric: {PATH_VALUE} != {expected} "
            return
        else:
            lista = isinstance(PATH_VALUE, list)
            dicts = isinstance(PATH_VALUE, dict)
            if lista:
                PATH_VALUE = self.json_response[entity][int(subPath)]
            if dicts:
                PATH_VALUE = self.json_response[entity][subPath]

            assert str(PATH_VALUE) == expected, f"value it is different to expected : {PATH_VALUE} != {expected}"

    def expected_results_value(self, file):
        self.json_strings = Functions.get_json_inData(self, file)
        try:
            assert self.json_strings == self.json_response
            print(u"Se cumplió con el valor esperado")
            verificar = True
        except AssertionError:
            verificar = False
            print("La respuesta fue: ")
            print(json.dumps(self.json_response, indent=4))
            print("Se esperaba: ")
            print(json.dumps(self.json_strings, indent=4))
            assert verificar == True

    def new_compare_entity_values(self, path, esperado):
        esperado = str(esperado)
        try:
            tree_obj = objectpath.Tree(self.json_response)
            PATH_VALUE = tree_obj.execute('$data' + path)

            if "generator object Tree.execute" in str(PATH_VALUE):
                entity = tuple(tree_obj.execute('$data' + path))
                PATH_VALUE = entity[0]

            print(PATH_VALUE)

        except TypeError:
            entity = tuple(str(tree_obj.execute('$.' + path)))
            PATH_VALUE = ''.join(map(str, entity))

        except SyntaxError:
            print("No se pudo obtener ningun valor de la busqueda")

        if esperado == "NOT NULL":
            assert str(PATH_VALUE) != None, f"El valor es Null: {PATH_VALUE} != {esperado}"
            return

        elif esperado == "NULL":
            assert str(PATH_VALUE) == None, f"El valor no es Null: {PATH_VALUE} != {esperado}"
            return
        else:
            assert str(PATH_VALUE) == str(esperado), f"No es el valor esperado {path}: {PATH_VALUE} != {esperado}"

    def get_accessToken(self):
        body = Config.authentication_body
        response = requests.post(Config.API_hostAddressBase + "auth/token", data=body)
        Authorization_response = json.loads(response.text)
        print(Authorization_response['access_token'])
        Config.API_headers["Authorization"] = "Bearer " + Authorization_response['access_token']
