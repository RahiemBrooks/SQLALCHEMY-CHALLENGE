# Climate App API

The Climate App API is a Flask-based web application that provides climate data analysis and exploration functionalities using SQLAlchemy, Pandas, and Matplotlib.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [API Routes](#api-routes)
- [Contributing](#contributing)
- [License](#license)

## Description

The Climate App API is designed to perform basic climate analysis and data exploration of a climate database. It includes two main parts:

1. **Part 1: Analyze and Explore the Climate Data**

   - Connects to an SQLite database using SQLAlchemy.
   - Performs precipitation analysis and station analysis.
   - Generates precipitation and temperature plots using Matplotlib.
   - Displays summary statistics for precipitation data.

2. **Part 2: Design Your Climate App**
   - Creates a Flask API with various routes for data retrieval.
   - Provides JSON representations of precipitation, station, and temperature data.
   - Calculates temperature statistics based on start and start-end ranges.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/climate-app.git
   cd climate-app
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```
   python app.py
   ```

## Usage

After starting the Flask app, you can access the API and its routes through a web browser or tools like Postman.

## API Routes

- `/` - Home page listing all available routes.
- `/api/v1.0/precipitation` - Retrieves precipitation data for the last 12 months.
- `/api/v1.0/stations` - Retrieves a list of weather stations.
- `/api/v1.0/tobs` - Retrieves temperature observations for the most active station.
- `/api/v1.0/<start>` - Retrieves temperature statistics for dates greater than or equal to the specified start date.
- `/api/v1.0/<start>/<end>` - Retrieves temperature statistics for a specified date range.

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
