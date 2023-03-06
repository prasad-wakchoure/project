from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)


model = pickle.load(open(r'project_1\Siddharth\frontend\model.pkl', 'rb'))
dv = pd.read_csv(r"project_1\Siddharth\frontend\PED-data-final.csv")


def ss(x):
    print(x)


@app.route('/', methods=["GET", 'POST'])
def home():
    if request.method == 'POST':
        global pid, pprice, pcon, pav, psale, pmon, pdem, hgname, hgcat, hgpe, hdemm, hnew_p, hgpx, hgpr
        pid = request.form.get('pid')
        pprice = request.form.get('pprice')
        pcon = request.form.get('pcon')
        pav = request.form.get('pav')
        psale = request.form.get('psale')
        pmon = request.form.get('pmon')
        pdem = request.form.get('pdem')
        print(type(pmon))
        sensei(pid, pprice, pcon, pav, psale, pmon, pdem)
        hgname = str(gname)
        hgcat = str(gcat)
        hgpe = str(gpe)
        hdemm = str(demm)
        hnew_p = str(new_p)
        hgpx = str(gpx)
        hgpr = str(gpr)
        return redirect(url_for('predz', hgname=hgname, hgcat=hgcat, hgpe=hgpe, hdemm=hdemm, hnew_p=hnew_p, hgpx=hgpx, hgpr=hgpr))
    else:
        return render_template('index.html')

    # print(type(pmon))
    #print("this is the best ---",pmon)
    # return render_template('index.html')


@app.route('/pred', methods=["GET", 'POST'])
def predz():
    return render_template('predz.html', hgname=hgname, hgcat=gcat, hgpe=gpe, hdemm=demm, hnew_p=new_p, hgpx=hgpx, hgpr=hgpr)


def loader(x):
    global gname, gcat, gpe, gpm, gim, gint, gslope, gpx, gpr
    g1 = dv[dv['namex'] == x]
    gname = g1["name"].iloc[0]
    gcat = g1["category"].iloc[0]
    gpe = g1["price_elasticity"].iloc[0]
    gpe = np.round(gpe, 2)
    gpm = g1["price_mean"].iloc[0]
    gim = g1["impressions_mean"].iloc[0]
    gint = g1["intercept"].iloc[0]
    gslope = g1["slope"].iloc[0]
    why = g1["price_elasticity"].iloc[0]
    gpx = np.round(why, 4)
    if gpx > 0 and gpx < 2:
        gpr = f"A price elasticity of demand(PED) value of {gpx}. indicates that a 0.1% increase in the price of the product will result in a {np.abs(gpx)}% increase in the quantity demanded of the product, assuming all other factors affecting demand remain constant."
        gpx = "The product has a relatively inelastic demand, and a small decrease in price does not affect the demand for the product."
    elif gpx >= 2:
        gpr = f"A price elasticity of demand(PED) value of {gpx}. indicates that a 0.1% increase in the price of the product will result in a {np.abs(gpx)}% increase in the quantity demanded of the product, assuming all other factors affecting demand remain constant."
        gpx = "The product has a highly elastic demand, and a small decrease in price significantly increase the demand for the product."
    elif gpx < 0 and gpx > -2:
        gpr = f"A price elasticity of demand(PED) value of {gpx}. indicates that a 0.1% increase in the price of the product will result in a {np.abs(gpx)}% decrease in the quantity demanded of the product, assuming all other factors affecting demand remain constant."
        gpx = "The product has a relatively inelastic demand, and a small decrease in price does not affect the demand for the product."
    elif gpx <= 2:
        gpr = f"A price elasticity of demand(PED) value of {gpx}. indicates that a 0.1% increase in the price of the product will result in a {np.abs(gpx)}% decrease in the quantity demanded of the product, assuming all other factors affecting demand remain constant."
        gpx = "The product has a negatively elastic demand, and a small decrease in price does not affect the demand for the product."


def sensei(pid, pprice, pcon, pav, psale, pmon, pdem):
    global demm, new_p
    pid = int(pid)
    pprice = float(pprice)
    pcon = int(pcon)
    pav = int(pav)
    psale = int(psale)
    pmon = int(pmon)
    pdem = float(pdem)
    y_pred = model.predict([[pid, pprice, pcon, pav, psale, pmon, pdem]])
    loader(pid)
    abs_x = np.abs(np.float(y_pred))
    percentage_diff = ((abs_x - pprice) / pprice) * 100  # abs
    demm = round(percentage_diff, 2)
    #####
    new_p = np.abs(((pprice/100)*percentage_diff)-pprice)
    new_p = np.abs(round(new_p, 2))
    #####
    return gname, gcat, gpe, demm, new_p


#action="{{ url_for('predz') }}"
if __name__ == "__main__":
    app.run(debug=True)
