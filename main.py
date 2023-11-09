from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df_meta = pd.read_csv("data_small/stations.txt", skiprows=17)
df_display = df_meta[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=df_display.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    station_name = df_meta.loc[df_meta["STAID"] == int(station)]\
    ["STANAME                                 "].squeeze()

    df = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt",
                     skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    return {"station": station_name.strip(),
            "station_number": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def alldata(station):
    df = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt",
                     skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    df = pd.read_csv(f"data_small/TG_STAID{str(station).zfill(6)}.txt",
                     skiprows=20,)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
