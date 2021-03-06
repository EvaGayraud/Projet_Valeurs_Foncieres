from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def process_attributes(df):
    # we would like to exploit continuous data from 0 to 1
    cont = ["Surface reelle bati", "Nombre pieces principales"]
    cs = MinMaxScaler()
    continuous = cs.fit_transform(df[cont])

    # put into categorical data the qualitative variables
    cat = ["Type local", "Code postal"]
    ord_enc = OrdinalEncoder()
    categorical_bin = ord_enc.fit(df[cat])
    categorical = categorical_bin.transform(df[cat])

    # construct and concatenate the training and testing categorical and continuous dataset
    attributes_norm = np.hstack([categorical, continuous])

    # return the concatenated data
    return attributes_norm
