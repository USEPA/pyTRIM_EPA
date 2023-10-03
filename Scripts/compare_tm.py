import argparse
import pandas as pd


def compare_tm(tm_1, tm_2):
    df1 = pd.read_csv(tm_1, index_col=0)
    df2 = pd.read_csv(tm_2, index_col=0)

    print(df1)
    print(df2)

    print(df1.compare(df2))

    df1.compare(df2).to_csv('./.output/tm_comparison.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-tm1', '--tm-1', default=None)
    parser.add_argument('-tm2', '--tm-2', default=None)
    args = parser.parse_args()

    compare_tm(args.tm_1, args.tm_2)
