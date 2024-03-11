# Ingénierie des Langues
# OUKHEMANOU Mohand-Tahar & VILFEU Vincent L3-Y
# Projet

import csv
import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from functools import reduce
from operator import concat

NB_POKEMON_MAX = "0493"


class Pokemon:

    def __init__(self, number='', french_name='', english_name='', types=[]) -> None:
        self.number = number
        self.french_name = french_name
        self.english_name = english_name
        self.types = types
        self.category = ""
        self.size = ""
        self.weight = ""
        self.talents = ""
        self.hatching = ""
        self.ev = ""
        self.exp = ""
        self.exp_100 = ""
        self.gender = ""
        self.color = ""
        self.capture = ""
        self.pv = ""
        self.atk = ""
        self.dfs = ""
        self.atk_sp = ""
        self.dfs_sp = ""
        self.vit = ""
        self.total = ""

    def __str__(self) -> str:
        return f"Numéro du Pokémon: {str(self.number)}, Nom Français: {self.french_name}, Nom Anglais: {self.english_name}, Type(s): {self.types}, Catégorie: {self.category}, Taille: {self.size}, Poids: {self.weight}, Talent(s): {self.talents}, Éclosion: {self.hatching}, EVs: {self.ev}, Expérience: {self.exp}, Expérience au Niv.100: {self.exp_100}, Genres: {self.gender}, Couleur: {self.color}, Taux de Capture: {self.capture}, PV: {self.pv}, Attaque: {self.atk}, Défense: {self.dfs}, Attaque Spéciale: {self.atk_sp}, Défense Spéciale: {self.dfs_sp}, Vitesse: {self.vit}, Total - Stat: {self.total}"

    def add_attribute(self, **attribs):
        if 'category' in attribs:
            self.category = attribs['category']
        if 'size' in attribs:
            self.size = attribs['size']
        if 'weight' in attribs:
            self.weight = attribs['weight']
        if 'talents' in attribs:
            self.talents = attribs['talents']
        if 'hatching' in attribs:
            self.hatching = attribs['hatching']
        if 'ev' in attribs:
            self.ev = attribs['ev']
        if 'exp' in attribs:
            self.exp = attribs['exp']
        if 'exp_100' in attribs:
            self.exp_100 = attribs['exp_100']
        if 'gender' in attribs:
            self.gender = attribs['gender']
        if 'color' in attribs:
            self.color = attribs['color']
        if 'capture' in attribs:
            self.capture = attribs['capture']

    def add_stat(self, **stat):
        if 'pv' in stat:
            self.pv = stat['pv']
        if 'atk' in stat:
            self.atk = stat['atk']
        if 'dfs' in stat:
            self.dfs = stat['dfs']
        if 'atk_sp' in stat:
            self.atk_sp = stat['atk_sp']
        if 'dfs_sp' in stat:
            self.dfs_sp = stat['dfs_sp']
        if 'vit' in stat:
            self.vit = stat['vit']
        if 'total' in stat:
            self.total = stat['total']


def get_page(url, poke):
    url = url + poke
    data = requests.get(url).text
    return BeautifulSoup(data, 'html.parser')


def get_infos(list_of_pokemon):
    soup = get_page("https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National", "")
    table = soup.find('table', class_='tableaustandard sortable entetefixe')
    types = []
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        types = [type['alt'] for type in columns[-1].find_all('img')]
        if columns[0].text != "":
            number = columns[0].text
            list_of_pokemon.append(
                Pokemon(number, columns[2].a.text, columns[3].a.text, types))
        if columns[0].text == "":
            continue
        if number == NB_POKEMON_MAX:
            break


def get_detail(list_of_pokemon):
    for pokemon in list_of_pokemon:
        soup2 = get_page("https://www.pokepedia.fr/", pokemon.french_name)
        table2 = soup2.find(
            'table', class_='tableaustandard ficheinfo ' + pokemon.types[0].lower())
        infos = []
        temp = []
        for row2 in table2.tbody.find_all('tr'):
            cols = row2.find_all('td')
            cols = [x.text.strip() for x in cols]
            temp.append(cols)
        if pokemon.number == "0483" or pokemon.number == "0484":
            temp.pop(15)
            temp.pop(16)
            infos.append(temp[-17:])
        if pokemon.number == "0487":
            temp.pop(13)
            temp.pop(14)
            temp.pop(15)
            infos.append(temp[-17:])
        if pokemon.number == "0492":
            temp.pop(16)
            temp.pop(17)
            temp.pop(18)
            infos.append(temp[-18:])
        else:
            infos.append(temp[-17:])
        infos = reduce(concat, infos)
        del infos[-5:]
        infos.pop(4)
        infos[3][0] = re.sub("1. ", "", infos[3][0])
        infos[3][0] = re.sub("2.", ",", infos[3][0])
        infos[3][0] = re.sub("3.", ",", infos[3][0])
        pokemon.add_attribute(category=infos[0][0], size=infos[1][0], weight=infos[2][0], talents=infos[3][0], hatching=infos[4]
                              [0], ev=infos[5][0], exp=infos[6][0], exp_100=infos[7][0], gender=infos[8][0], color=infos[9][0], capture=infos[10][0])
        if pokemon.number == NB_POKEMON_MAX:
            break


def get_stat(list_of_pokemon):
    for pokemon in list_of_pokemon:
        soup2 = get_page("https://www.pokepedia.fr/", pokemon.french_name)
        if pokemon.number == "0413":
            table2 = soup2.find_all(
                'table', class_='tableaustandard ' + pokemon.types[1].lower())
        else:
            table2 = soup2.find_all(
                'table', class_='tableaustandard ' + pokemon.types[0].lower())
        infos = []
        temp = []
        if len(table2) == 1 or (len(table2) > 1 and len(table2[0].tbody) > 20) or pokemon.number == "0413":
            for row2 in table2[0].tbody.find_all('tr'):
                cols = row2.find_all('td')
                cols = [x.text.strip() for x in cols]
                temp.append(cols)
            infos.append(temp[3:9])
            infos = reduce(concat, infos)
            pokemon.add_stat(pv=infos[0][1], atk=infos[1][1], dfs=infos[2][1], atk_sp=infos[3][1], dfs_sp=infos[4]
                             [1], vit=infos[5][1], total=int(infos[0][1])+int(infos[1][1])+int(infos[2][1])+int(infos[3][1])+int(infos[4][1])+int(infos[5][1]))
        else:
            for row2 in table2[1].tbody.find_all('tr'):
                cols = row2.find_all('td')
                cols = [x.text.strip() for x in cols]
                temp.append(cols)
            infos.append(temp[3:9])
            infos = reduce(concat, infos)
            pokemon.add_stat(pv=infos[0][1], atk=infos[1][1], dfs=infos[2][1], atk_sp=infos[3][1], dfs_sp=infos[4]
                             [1], vit=infos[5][1], total=int(infos[0][1])+int(infos[1][1])+int(infos[2][1])+int(infos[3][1])+int(infos[4][1])+int(infos[5][1]))
        if pokemon.number == NB_POKEMON_MAX:
            break


def create_csv_with_data(array_of_object):
    columns = ['Numéro', 'Nom Français', 'Nom Anglais', 'Type(s)', 'Catégorie', 'Taille', 'Poids', 'Talent(s)', 'Éclosion',
               'EVs', 'Expérience', 'Expérience au Niv.100', 'Sexe', 'Couleur', 'Taux de Capture', 'PV', 'Attaque', 'Défense', 'Attaque Spéciale', 'Défense Spéciale', 'Vitesse', 'Total - Stats']

    os.makedirs("data", exist_ok=True)
    path_file_csv = 'data/pokemons.csv'
    with open(path_file_csv, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        for object in array_of_object:
            types_str = ','.join(object.types)
            writer.writerow({columns[0]: object.number, columns[1]: object.french_name,
                            columns[2]: object.english_name, columns[3]: types_str, columns[4]: object.category, columns[5]: object.size, columns[6]: object.weight, columns[7]: object.talents, columns[8]: object.hatching, columns[9]: object.ev, columns[10]: object.exp, columns[11]: object.exp_100, columns[12]: object.gender, columns[13]: object.color, columns[14]: object.capture, columns[15]: object.pv, columns[16]: object.atk, columns[17]: object.dfs, columns[18]: object.atk_sp, columns[19]: object.dfs_sp, columns[20]: object.vit, columns[21]: object.total})

    print("Le fichier csv a été créé avec succès.")


def convert_csv_to_excel(path_csv_file, path_excel_file):
    data_frame = pd.read_csv(path_csv_file)
    data_frame.to_excel(path_excel_file, index=False)

    print("Le fichier excel a été créé avec succès.")


def main() -> None:
    list_of_pokemon = []

    get_infos(list_of_pokemon)

    get_detail(list_of_pokemon)

    get_stat(list_of_pokemon)

    create_csv_with_data(list_of_pokemon)
    convert_csv_to_excel('data/pokemons.csv', 'data/pokemons.xlsx')


if __name__ == "__main__":
    main()
