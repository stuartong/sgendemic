import pandas as pd

def project_hospitalized(prob_hos,default,vax_rate=None, perc_of_pop=None, r0=6,si=5.4):
    prob_hos = pd.read_csv(prob_hos)
    default = pd.read_csv(default)
    if vax_rate is None:
        vax_rate = default['vax_rate_2'].values.tolist()
    if perc_of_pop is None:
        perc_of_pop = default['perc_of_pop'].values.tolist()
    
    beds = 1000
    infected = 1
    no_in_icu = 0
    cycles = 0
    serial_int = si
    vac_eff = 0.6

    prob_hos['vax_rate_2'] = vax_rate
    prob_hos['perc_of_pop'] = perc_of_pop
    prob_hos['no_of_res'] = default['no_of_res']
    protected_pop = (prob_hos['no_of_res']*prob_hos['vax_rate_2']*vac_eff).sum()/prob_hos['no_of_res'].sum()
    sus_pop = 1-protected_pop
    effective_r0 = r0*sus_pop
    while no_in_icu<beds:
        infected = infected * (effective_r0)
        prob_hos['proj_vax_hos'] = (infected*prob_hos['perc_of_pop']*prob_hos['vax_rate_2']*prob_hos['prob_hos_vax'])
        prob_hos['proj_non_vax_hos'] = (infected*prob_hos['perc_of_pop']*(1-prob_hos['vax_rate_2'])*prob_hos['prob_hos_no_vaxx'])
        prob_hos['proj_total_hos'] = prob_hos['proj_vax_hos'] + prob_hos['proj_non_vax_hos']
        no_in_icu = prob_hos['proj_total_hos'].sum()
        cycles += 1
        # print(prob_hos)
    days_to_shortage = cycles * serial_int

    return (infected,cycles,days_to_shortage,no_in_icu,sus_pop,effective_r0)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file1', help='Default probability of hospitalization (CSV)'
    )
    parser.add_argument(
        'input_file2', help='Default population split (CSV)'
    )
    args = parser.parse_args()

    vax = [1,1,1,1,1,1]
    perc = []
    print(project_hospitalized(args.input_file1,args.input_file2,r0=6))

