# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
     min_date = dt.datetime(2016,8,22)
     data = [measurements.date, func.max(measurements.prcp)]
     query = session.query(*data).filter(measurements.date > min_date).group_by(measurements.date)
     precip_dict = dict(query)
     return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations_types():
    station_query = session.query(stations.station, stations.name)
    station_dict = dict(station_query)
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def temps():
    min_date = dt.datetime(2016,8,22)
    tobs_query = session.query(measurements.date, measurements.tobs).filter(measurements.station == 'USC00519281', measurements.date > min_date)
    tobs_dict = dict(tobs_query)
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def by_start_date(start):
    start_date_query = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= start)
    start_date_dict = dict(start_date_query)
    return jsonify(start_date_dict)

@app.route("/api/v1.0/<start>/<end>")
def by_start_end_date(start, end):
    start_end_date_query = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= start, measurements.date <= end)
    start_end_date_dict = dict(start_end_date_query)
    return jsonify(start_end_date_dict)

if __name__ == "__main__":
    app.run(debug=True)