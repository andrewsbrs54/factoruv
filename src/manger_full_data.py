from pandas import pandas
import os


def main():
    print('hola')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../data/data.csv')
    df = pandas.read_csv(filename, sep=';', header=None, na_values=" NaN")
    print(df)


if __name__ == '__main__':
    main()
