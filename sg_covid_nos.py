import pandas as pd

def get_sg_only(inputfile):
    data = pd.read_csv(inputfile)
    # filter for SG only
    data = data[data['Country/Region']=='Singapore']
    data = data.T.iloc[4:]
    data.index = pd.to_datetime(data.index)
    data.rename(columns={data.columns[0] : 'daily_total'},inplace=True)
    data['daily_new'] = data.diff()
    data['rolling_mean'] = data['daily_new'].rolling(5).mean()
    data['rolling_sum'] = data['daily_new'].rolling(5).sum()
    return data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file', help='the raw covid data (CSV)'
    )
    parser.add_argument(
        'output_file', help='Covid Numbers SG Only (CSV)'
    )
    args = parser.parse_args()

    clean_data = get_sg_only(args.input_file)
    clean_data.to_csv(args.output_file)