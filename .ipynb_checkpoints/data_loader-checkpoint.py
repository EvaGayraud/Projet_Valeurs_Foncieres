import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler


def load_house_attributes(url):
    # get the dataframe
    cols = [
        "Valeur fonciere",
        "Surface reelle bati",
        "Nombre pieces principales",
        "Type local",
        "Commune",
        "Code postal",
    ]
    df0 = pd.read_csv(url, usecols=cols, low_memory=False, sep="|")
    df = df0.copy()

    df["Type local"].replace("", np.nan, inplace=True)
    df.dropna(inplace=True)

    Arrondissements_Paris = [
        "PARIS 01",
        "PARIS 02",
        "PARIS 03",
        "PARIS 04",
        "PARIS 05",
        "PARIS 06",
        "PARIS 07",
        "PARIS 08",
        "PARIS 09",
        "PARIS 10",
        "PARIS 11",
        "PARIS 12",
        "PARIS 13",
        "PARIS 14",
        "PARIS 15",
        "PARIS 16",
        "PARIS 17",
        "PARIS 18",
        "PARIS 19",
        "PARIS 20",
    ]
    df_paris = df[df["Commune"].isin(Arrondissements_Paris)]
    df_paris = df_paris.drop_duplicates()
    df_paris["Valeur fonciere"] = df_paris["Valeur fonciere"].str.replace(",", ".")

    # convert to the correct type
    df_paris["Valeur fonciere"] = df_paris["Valeur fonciere"].astype(float)
    df_paris["Code postal"] = df_paris["Code postal"].astype(str)
    df_paris["Nombre pieces principales"] = df_paris[
        "Nombre pieces principales"
    ].astype(int)

    # remove outliers
    df_paris = df_paris[df_paris["Valeur fonciere"] <= 30000000]
    df_paris = df_paris[df_paris["Surface reelle bati"] >= 10]
    df_paris = df_paris[df_paris["Nombre pieces principales"] <= 20]
    df_paris = df_paris[df_paris["Nombre pieces principales"] > 0]

    return df_paris


def process_house_attributes(df_paris, train, test):
    # we would like to exploit continuous data from 0 to 1
    continuous = ["Surface reelle bati", "Nombre pieces principales"]
    cs = MinMaxScaler()
    trainContinuous = cs.fit_transform(train[continuous])
    testContinuous = cs.transform(test[continuous])

    # put into categorical data the qualitative variables
    categorical = ["Type local", "Code postal"]
    ord_enc = OrdinalEncoder()
    CategoricalBin = ord_enc.fit(df_paris[categorical])
    trainCategorical = CategoricalBin.transform(train[categorical])
    testCategorical = CategoricalBin.transform(test[categorical])

    # construct and concatenate the training and testing categorical and continuous dataset
    trainX = np.hstack([trainCategorical, trainContinuous])

    testX = np.hstack([testCategorical, testContinuous])

    # return the concatenated data
    return trainX, testX
