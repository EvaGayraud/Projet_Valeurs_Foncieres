import os.path
from tqdm.notebook import tqdm
import pandas as pd
import json

url_dict = {
    '2020': 'https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f',
    '2019': 'https://www.data.gouv.fr/fr/datasets/r/3004168d-bec4-44d9-a781-ef16f41856a2',
    '2018': 'https://www.data.gouv.fr/fr/datasets/r/1be77ca5-dc1b-4e50-af2b-0240147e0346',
    '2017': 'https://www.data.gouv.fr/fr/datasets/r/7161c9f2-3d91-4caf-afa2-cfe535807f04',
    '2016': 'https://www.data.gouv.fr/fr/datasets/r/0ab442c5-57d1-4139-92c2-19672336401c',
}


def source_choice():
    if os.path.isfile('data/data.json'):
        with open('data/data.json') as f:
            data = f.read()
        a_json = json.loads(data)
        df = pd.DataFrame.from_dict(a_json, orient="index").transpose()
    else:
        df = get_subsample()

    return df


def get_subsample():
    data_all_year = []
    for year, url in tqdm(url_dict.items()):
        data_ = pd.read_csv(url, low_memory=False, sep="|")

        # drop columns based on number of null
        data_ = data_.drop(
            [
                'Code service CH', 'Reference document', '1 Articles CGI', '2 Articles CGI', '3 Articles CGI',
                '4 Articles CGI', '5 Articles CGI', 'B/T/Q', 'Prefixe de section', 'No Volume', '1er lot',
                'Surface Carrez du 1er lot', '2eme lot', 'Surface Carrez du 2eme lot', '3eme lot',
                'Surface Carrez du 3eme lot', '4eme lot', 'Surface Carrez du 4eme lot', '5eme lot',
                'Surface Carrez du 5eme lot', 'Identifiant local', 'Code voie', 'Code type local',
                'No Volume', 'Nature culture', 'Nature culture speciale', 'Surface terrain',
                'No voie', 'Voie', 'No plan'
            ],
            axis=1
        )

        data = data_[data_['Code departement'] == '75']
        del data_
        data['year'] = year
        data_all_year.append(data)
        del data

    df = pd.concat(data_all_year)
    convert_json(df)

    return df


def convert_json(df):
    df.reset_index(drop=True, inplace=True)
    df.to_json(r'data/data.json')
