from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

dati = []
FAILS = "dati.csv"

# Ielādē datus no CSV
def ieladet_datus():
    if os.path.exists(FAILS):
        with open(FAILS, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for rinda in reader:
                dati.append({
                    "tips": rinda[0],
                    "summa": float(rinda[1]),
                    "apraksts": rinda[2],
                    "valuta": rinda[3] if len(rinda) > 3 else "€"
                })

# Saglabā datus CSV
def saglabat_datus():
    with open(FAILS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for ier in dati:
            writer.writerow([
                ier["tips"],
                ier["summa"],
                ier["apraksts"],
                ier["valuta"]
            ])

# Aprēķina bilanci (vienkārši EUR bāzē)
def aprekinat_balanci():
    ienakumi = sum(i["summa"] for i in dati if i["tips"] == "Ienākums")
    izdevumi = sum(i["summa"] for i in dati if i["tips"] == "Izdevums")
    return ienakumi - izdevumi

@app.route('/')
def index():
    balanss = aprekinat_balanci()
    return render_template("index.html", dati=dati, balanss=balanss)

@app.route('/pievienot', methods=['POST'])
def pievienot():
    try:
        tips = request.form['tips']
        summa = float(request.form['summa'])
        apraksts = request.form['apraksts']
        valuta = request.form['valuta']

        ieraksts = {
            "tips": tips,
            "summa": summa,
            "apraksts": apraksts,
            "valuta": valuta
        }

        dati.append(ieraksts)
        saglabat_datus()

    except:
        print("Kļūda ievadē!")

    return redirect('/')

@app.route('/dzest/<int:index>')
def dzest(index):
    if 0 <= index < len(dati):
        dati.pop(index)
        saglabat_datus()
    return redirect('/')

if __name__ == "__main__":
    ieladet_datus()
    app.run(debug=True)