from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template
import test_result_helper

# RUN THE APP
# Windows
# set FLASK_APP=app.py
# flask run
#
# Linux
# export FLASK_APP=app.py
# flask run

# Set the MongoDB connection and database connection
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://192.168.0.143:32768/Vault"
mongo = PyMongo(app)


@app.route("/adcp/<serial_number>")
def adcp_serial_page(serial_number):
    adcp = mongo.db.adcps.find_one_or_404({"SerialNumber": serial_number})
    print(adcp)
    return render_template("adcp.html", adcp=adcp)


@app.route("/cert/<serial_number>")
def adcp_cert_page(serial_number):
    adcp = mongo.db.adcps.find_one_or_404({"SerialNumber": serial_number})
    compass = mongo.db.CompassCalResults.find({"SerialNumber": serial_number, "IsSelected": True})
    compass_list = test_result_helper.process_compass_cal(compass)
    lake_dmgs = mongo.db.WaterTestResults.find({"SerialNumber": serial_number, "IsSelected": True})
    lake_snrs = mongo.db.SnrTestResults.find({"SerialNumber": serial_number, "IsSelected": True})
    lake_snr_list = test_result_helper.process_lake_snr(lake_snrs)
    tank_noise = mongo.db.TankTestResults.find({"SerialNumber": serial_number, "IsSelected": True, "TankTestType": "Noise"})
    tank_noise_list = test_result_helper.process_tanktest_noise(tank_noise)
    print(adcp)
    print(compass_list)
    print(lake_dmgs)
    print(lake_snr_list)
    print(tank_noise_list)
    return render_template("cert.j2", adcp=adcp, compasscals=compass_list, lake_dmgs=lake_dmgs, lake_snrs=lake_snr_list, tank_noises=tank_noise_list)


@app.route("/cert_hydro/<serial_number>")
def adcp_cert_hydro_page(serial_number):
    adcp = mongo.db.adcps.find_one_or_404({"SerialNumber": serial_number})
    compass = mongo.db.CompassCalResults.find({"SerialNumber": serial_number, "IsSelected": True})
    compass_list = test_result_helper.process_compass_cal(compass)
    hydro = mongo.db.HydrophoneLakeTestResults.find({"SerialNumber": serial_number, "IsSelected": True})
    tank_noise = mongo.db.TankTestResults.find({"SerialNumber": serial_number, "IsSelected": True, "TankTestType": "Noise"})
    tank_noise_list = test_result_helper.process_tanktest_noise(tank_noise)
    print(adcp)
    print(compass_list)
    print(hydro)
    print(tank_noise_list)
    return render_template("cert_hydro.j2", adcp=adcp, compasscals=compass_list, hydros=hydro, tank_noises=tank_noise_list)



@app.route("/")
def adcp_list_page():
    adcps = mongo.db.adcps.find().sort("created", -1)
    print(adcps)
    return render_template("adcp_list.html", adcps=adcps)


@app.route("/hydro")
def hydro_page():
    hydro = mongo.db.HydrophoneLakeTestResults.find({})
    print(hydro[0])
    return render_template("hydro.html", hydros=hydro[0])


@app.route("/hydro/<serial_number>")
def hydro_serial_page(serial_number):
    hydro = mongo.db.HydrophoneLakeTestResults.find_one_or_404({"SerialNumber": serial_number})
    print(hydro)
    return render_template("hydro.html", hydros=hydro)
