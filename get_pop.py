import pandas as pd
import json
import urllib.request

def get_pop_data():
    urlData = "https://tablebuilder.singstat.gov.sg/api/table/tabledata/M810011?timeFilter=2020&sortBy=seriesno%20asc"
    webURL = urllib.request.urlopen(urlData)
    data = json.loads(webURL.read())
    pop = pd.DataFrame(data['Data']['row'])
    pop['seriesNo'] = pop['seriesNo'].astype(float) 
    pop = pop[pop['seriesNo']<2]
    pop['columns'] = pop.explode('columns')['columns']
    pop['no_of_res'] = pop['columns'].apply(lambda x: x.get('value'))
    pop = pop[['rowText','no_of_res']]
    pop['no_of_res'] = pop['no_of_res'].astype(float)

    less_12 = [1,'Below 12',pop.iloc[1:4]['no_of_res'].sum(),0,1,0.0235]
    a12_to_39 = [2,'12 to 39',pop.iloc[4:9]['no_of_res'].sum(),0.45,1.5,0.0395]
    a40_to_44 = [3,'40 to 44',pop.iloc[9:10]['no_of_res'].sum(),0.70,2,0.0695]
    a45_to_59 = [4,'45 to 59',pop.iloc[10:13]['no_of_res'].sum(),0.80,3,0.0975]
    a60_to_69 = [5,'60 to 69',pop.iloc[13:15]['no_of_res'].sum(),0.82,5,0.1285]
    a70_up = [6,'70 and Over',pop.iloc[20:21]['no_of_res'].sum(),0.71,10,0.1540]
    
    total_pop = pop.iloc[0]['no_of_res']
    risk_reduction = 1-0.6455

    pop_by_age = pd.DataFrame([less_12,
    a12_to_39,
    a40_to_44,
    a45_to_59,
    a60_to_69,
    a70_up],columns=['cat','group','no_of_res','vax_rate_2','risk_of_hos','prob_hos_no_vaxx'])
    
    pop_by_age['perc_of_pop'] = pop_by_age['no_of_res']/total_pop
    pop_by_age['prob_hos_vax'] = pop_by_age['prob_hos_no_vaxx']*risk_reduction

    prob_by_age = pop_by_age[['cat','group','prob_hos_vax','prob_hos_no_vaxx']]

    return pop_by_age, prob_by_age

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'output_file1', help='default args for each group (CSV)'
    )
    parser.add_argument(
        'output_file2', help='prob of hospitalization by age group (CSV)'
    )
    args = parser.parse_args()

    pop_data = get_pop_data()
    pop_data[0].to_csv(args.output_file1, index=False)
    pop_data[1].to_csv(args.output_file2, index=False)
