from flask import Flask
from flask import request, escape
from flask import render_template
import pandas as pd
import project_hos as ph

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def index():
    prob_hos = 'data/prob_hos_age.csv'
    pop_def = 'data/pop_defaults.csv'
    pop_def_df = pd.read_csv(pop_def)
    vax_rate_def = pop_def_df['vax_rate_2'].values.tolist()
    def_c1_vax = vax_rate_def[0]*100
    def_c2_vax = vax_rate_def[1]*100
    def_c3_vax = vax_rate_def[2]*100
    def_c4_vax = vax_rate_def[3]*100
    def_c5_vax = vax_rate_def[4]*100
    def_c6_vax = vax_rate_def[5]*100
    if request.method=='POST':
        r0 = float(request.form['r0'])
        si = float(request.form['si'])
        cat_1_vax = float(request.form["cat_1_vax"])/100
        cat_2_vax = float(request.form["cat_2_vax"])/100
        cat_3_vax = float(request.form["cat_3_vax"])/100
        cat_4_vax = float(request.form["cat_4_vax"])/100
        cat_5_vax = float(request.form["cat_5_vax"])/100
        cat_6_vax = float(request.form["cat_6_vax"])/100
        vax_rate_2 = [cat_1_vax,cat_2_vax,cat_3_vax,cat_4_vax,cat_5_vax,cat_6_vax]
        output = ph.project_hospitalized(prob_hos,pop_def,vax_rate=vax_rate_2,r0=r0,si=si)
        no_cycles = output[1]
        days = int(round(output[2],0))
        infected = int(round(output[0],0))
        icu = int(round(output[3],0))
        sus_pop = float(round(output[4]*100,1))
        effective_r0 = float(round(output[5],1))
        weeks = float(round(days/7,1))
        if weeks <= 7:
            out_string = "Alamak! Singapore hospitals will be overrun in " + str(weeks) +" weeks by COVID! Better take precautions to flatten that curve bro!"
        else:
            out_string = "Wah! " + str(weeks) +" weeks then hospital is full! Looks like got alot of buffer, you sure we need to lockdown because of another spike in cases from KTV again?"
        return render_template('index.html',
                                no_cycles=no_cycles,
                                days=days,
                                icu=icu,
                                infected=infected,
                                def_c1_vax=def_c1_vax,
                                def_c2_vax=def_c2_vax,
                                def_c3_vax=def_c3_vax,
                                def_c4_vax=def_c4_vax,
                                def_c5_vax=def_c5_vax,
                                def_c6_vax=def_c6_vax,
                                r0=r0,
                                si=si,
                                cat_1_vax=cat_1_vax*100,
                                cat_2_vax=cat_2_vax*100,
                                cat_3_vax=cat_3_vax*100,
                                cat_4_vax=cat_4_vax*100,
                                cat_5_vax=cat_5_vax*100,
                                cat_6_vax=cat_6_vax*100,
                                out_string = out_string,
                                sus_pop = sus_pop,
                                effective_r0 = effective_r0
                                )
    elif request.method=='GET':
        output = ph.project_hospitalized(prob_hos,pop_def)
        no_cycles = output[1]
        days = int(round(output[2],0))
        infected = int(round(output[0],0))
        icu = int(round(output[3],0))
        sus_pop = float(round(output[4]*100,1))
        effective_r0 = float(round(output[5],1))
        weeks = float(round(days/7,1))
        if weeks <= 7:
            out_string = "Alamak! Singapore hospitals will be overrun in " + str(weeks) +" weeks by COVID! Better take precautions to flatten that curve bro!"
        else:
            out_string = "Wah! " + str(weeks) +" weeks then hospital is full! Looks like got alot of buffer, you sure we need to lockdown because of another spike in cases from KTV again?"
        # return render_template('test.html',out_string = out_string)
        return render_template('index.html',
                                no_cycles=no_cycles,
                                days=days,
                                icu=icu,
                                infected=infected,
                                def_c1_vax=def_c1_vax,
                                def_c2_vax=def_c2_vax,
                                def_c3_vax=def_c3_vax,
                                def_c4_vax=def_c4_vax,
                                def_c5_vax=def_c5_vax,
                                def_c6_vax=def_c6_vax,
                                r0=6,
                                si=5.4,
                                cat_1_vax=def_c1_vax,
                                cat_2_vax=def_c2_vax,
                                cat_3_vax=def_c3_vax,
                                cat_4_vax=def_c4_vax,
                                cat_5_vax=def_c5_vax,
                                cat_6_vax=def_c6_vax,
                                out_string = out_string,
                                sus_pop = sus_pop,effective_r0 = effective_r0
                                )



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

"""
to get development environment for flask run the following commands in terminal
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
"""