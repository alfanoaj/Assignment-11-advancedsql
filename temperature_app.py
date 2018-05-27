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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<br/>"
        f"/api/v1.0//<br/>"
    )


@app.route("/api/v1.0/precipitation")
def dates():
    """Run a query for all of the dates and measurements for last year"""
    # Query the dates for last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>"2016-08-23").all()

     # Create a dictionary from the row data and append to a list of measurements
    measurements = []
    for date in results:
        measurements.append(results)

    return jsonify(measurements)

@app.route("/api/v1.0/stations")
def stations():
    """Run a query to list all of the stations"""
    # Query stations
    stations = session.query(Station.station).all()

    # Jsonify the data
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Run a query to return all of the temp observations for the previous year"""
    # Query stations
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>"2016-08-23").all()
    temps = []
    for temp in tobs:
        temps.append(temp)

    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def temperature_start(start):
    """Returns a list of the minimum, average, and maximum temp for a given start range unless there is an
       error with the path variable supplied by the user, resulting in a 404 if not.  
       Must be yyyy-mm-dd format"""

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

    return(f'The average temp for {start} to present is {int(avg_temp[0][0])} degrees farenheight. <br/>'
            f'The minimum temp for {start} to present is {min_temp[0][0]} degrees farenheight. <br/>'
            f'The maximum temp for {start} to present is {max_temp[0][0]} degrees farenheight.')
    

@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end):
    """Returns a list of the minimum, average, and maximum temp for a given start range unless there is an
       error with the path variable supplied by the user, resulting in a 404 if not.  
       Must be yyyy-mm-dd format"""

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>start).filter(Measurement.date<end).all()

    return(f'The average temp for {start} to {end} is {int(avg_temp[0][0])} degrees farenheight. <br/>'
                    f'The minimum temp for {start} to {end} is {min_temp[0][0]} degrees farenheight. <br/>'
                    f'The maximum temp for {start} to {end} is {max_temp[0][0]} degrees farenheight.')
    
if __name__ == '__main__':
    app.run(debug=True)
