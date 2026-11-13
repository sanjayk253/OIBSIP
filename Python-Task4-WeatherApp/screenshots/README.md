
# Basic Weather App

## Project Overview
A Python-based desktop Weather Application developed as part of the Oasis Infobyte Python Programming Internship.

The application retrieves real-time weather information using the OpenWeatherMap API.

## Features
- Search weather by city name.
- Display current temperature.
- Celsius and Fahrenheit conversion.
- Display weather conditions and icons.
- Show humidity and wind speed.
- Next 6-hour weather forecast.
- 5-day weather forecast.
- Handle invalid city names.
- Handle network and API errors.

## Technologies Used
- Python
- Tkinter
- Requests
- Pillow
- OpenWeatherMap API

## Project Structure

```text
Python-Task4-WeatherApp/
│
├── assets/
├── screenshots/
│   └── weather_app.png
├── .env
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
├── README.md
└── test_api.py
```

## Installation

1. Clone or download the project.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory:

```text
OPENWEATHER_API_KEY=your_api_key_here
```

5. Run the application:

```bash
python main.py
```

## API
Weather data is provided by the OpenWeatherMap API.

https://openweathermap.org/api

## Screenshot

See the `screenshots` folder for the application screenshot.

## Author
Sanjay K

## Internship
Oasis Infobyte – Python Programming Internship

## Project
Task 4 – Basic Weather App
