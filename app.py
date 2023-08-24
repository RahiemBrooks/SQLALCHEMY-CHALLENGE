# Import the dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the tables into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the classes
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Route to the homepage that lists all available routes
@app.route("/")
def welcome():
    return (
        '<html>'
        '<head>'
        '<style>'
        'body {'
        '    font-family: Arial, sans-serif;'
        '    margin: 0;'
        '    padding: 0;'
        '    background-color: #f2f2f2;'
        '}'
        'h1 {'
        '    background-color: #333;'
        '    color: #fff;'
        '    padding: 20px;'
        '    margin: 0;'
        '    text-align: center;'
        '}'
        'h3 {'
        '    margin-top: 20px;'
        '    margin-bottom: 10px;'
        '    font-size: 24px;'
        '    color: #333;'
        '}'
        'ul {'
        '    list-style-type: none;'
        '    margin: 0;'
        '    padding: 0;'
        '    padding-left: 20px;'
        '}'
        'li {'
        '    margin-bottom: 10px;'
        '}'
        'a {'
        '    text-decoration: none;'
        '    color: #333;'
        '}'
        '</style>'
        '</head>'
        '<title>Climate App API</title>'
        '<body >'
        '<h1>Welcome to the Climate App API!</h1>'
        '<h3>Available Routes:</h3>'
        '<ul>'
        '<li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>'
        '<li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>'
        '<li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>'
        '<li><a href="/api/v1.0/2016-01-01">/api/v1.0/&lt;start&gt;</a></li>'
        '<li><a href="/api/v1.0/2016-01-01/2017-12-31">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a></li>'
        '</ul>'
        '</body>'
        '</html>'
    )



# Route for the precipitation analysis results
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the dataset
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    
    # Query the precipitation data for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                         filter(Measurement.date >= one_year_ago.date()).all()
    
    # Convert the query results to a dictionary with date as the key and prcp as the value
    prcp_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(prcp_dict)

# Route for the list of stations
@app.route("/api/v1.0/stations")
def stations():
    # Create a new session for this route
    session = Session(engine)
    try:
        # Query the list of stations
        stations_data = session.query(Station.station).all()
        stations_list = list(np.ravel(stations_data))
        
        # Return the stations list
        return jsonify(stations_list)
    finally:
        # Close the session to release resources
        session.close()

# Route for temperature observations for the most-active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most-active station
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                     group_by(Measurement.station).\
                     order_by(func.count(Measurement.station).desc()).first()[0]
    
    # Find the most recent date for the most-active station
    most_recent_date = session.query(Measurement.date).\
                       filter(Measurement.station == active_station).\
                       order_by(Measurement.date.desc()).first()[0]
    
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    
    # Query the temperature observations for the last 12 months for the most-active station
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == active_station).\
                filter(Measurement.date >= one_year_ago.date()).all()
    
    # Convert the query results to a list of dictionaries
    tobs_list = [{"Date": date, "Temperature": temp} for date, temp in tobs_data]
    
    return jsonify(tobs_list)

# Route for temperature statistics based on start date
@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Use a context manager to ensure proper session handling
    with Session(engine) as session:
        # Query temperature statistics for dates greater than or equal to the start date
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                     filter(Measurement.date >= start_date).all()
        
    temp_stats_dict = {
        "Min Temperature": temp_stats[0][0],
        "Avg Temperature": temp_stats[0][1],
        "Max Temperature": temp_stats[0][2]
    }
    
    return jsonify(temp_stats_dict)


# Route for temperature statistics based on start and end dates
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # Use a context manager to ensure proper session handling
    with Session(engine) as session:
        # Query temperature statistics for dates between start and end dates (inclusive)
        temp_stats_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                           filter(Measurement.date >= start_date).\
                           filter(Measurement.date <= end_date).all()
    
    temp_stats_range_dict = {
        "Min Temperature": temp_stats_range[0][0],
        "Avg Temperature": temp_stats_range[0][1],
        "Max Temperature": temp_stats_range[0][2]
    }
    
    return jsonify(temp_stats_range_dict)


if __name__ == '__main__':
    app.run(debug=True)
