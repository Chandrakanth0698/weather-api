from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


df_meta = pd.read_csv("data_small/stations.txt", skiprows=17)


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_name = df_meta.loc[df_meta["STAID"] == int(station)]\
    ["STANAME                                 "].squeeze()

    df = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt",
                     skiprows=20,parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    return {"station": station_name.strip(),
            "station_number": station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)
