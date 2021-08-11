import pandas as pd

def get_latest_numbers():
    # URL from git
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    # read data from git
    df = pd.read_csv(url,sep=',')
    return df

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'output_file', help='the raw covid data (CSV)'
    )
    args = parser.parse_args()

    full_data = get_latest_numbers()
    full_data.to_csv(args.output_file, index=False)