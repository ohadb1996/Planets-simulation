import pandas as pd
import numpy as np


def open_data_csv(path):
    """
    Opens a .csv file containing planetary data and returns its content as a pandas dataframe
    :param path: the path of the file to open
    :return: a Pandas dataframe with the planetary data from the file
    """
    mydata = pd.read_csv(path)
    return mydata


def create_mat_data(mydata):
    return mydata.to_numpy()


data = create_mat_data(open_data_csv("data.csv"))
dataCSV = open_data_csv("data.csv")
