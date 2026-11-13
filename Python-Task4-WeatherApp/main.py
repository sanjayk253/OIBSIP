
import tkinter as tk
from tkinter import messagebox
import requests

from io import BytesIO
from PIL import Image, ImageTk
from datetime import datetime, timezone, timedelta

from config import API_KEY, BASE_URL, FORECAST_URL


# ==========================================
# 1. MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Weather App")
root.geometry("1100x850")
root.configure(bg="#1e293b")
root.resizable(True, True)

current_unit = "metric"
weather_icon = None
daily_icons = []


# ==========================================
# 2. DOWNLOAD WEATHER ICON
# ==========================================

def download_weather_icon(icon_code, size=(60, 60)):

    icon_url = (
        f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    )

    response = requests.get(icon_url, timeout=10)
    response.raise_for_status()

    image = Image.open(
        BytesIO(response.content)
    ).convert("RGBA")

    image = image.resize(size)

    return ImageTk.PhotoImage(image)


# ==========================================
# 3. FIVE-DAY FORECAST
# ==========================================

def display_five_day_forecast(forecast_items, timezone_offset):

    global daily_icons

    daily_icons = []

    daily_data = {}

    for item in forecast_items:

        local_datetime = (
            datetime.fromtimestamp(
                item["dt"],
                tz=timezone.utc
            ) + timedelta(seconds=timezone_offset)
        )

        date_key = local_datetime.date()

        if date_key not in daily_data:
            daily_data[date_key] = []

        daily_data[date_key].append(
            (local_datetime, item)
        )

    # Remove old cards
    for widget in daily_forecast_frame.winfo_children():
        widget.destroy()

    symbol = "°C" if current_unit == "metric" else "°F"

    available_dates = sorted(daily_data.keys())[:5]

    for date_key in available_dates:

        entries = daily_data[date_key]

        temperatures = [
            item["main"]["temp"]
            for local_time, item in entries
        ]

        minimum_temp = min(temperatures)
        maximum_temp = max(temperatures)

        # Select forecast closest to noon
        representative_time, representative_item = min(
            entries,
            key=lambda entry: abs(
                entry[0].hour + entry[0].minute / 60 - 12
            )
        )

        condition = (
            representative_item["weather"][0]["description"].title()
        )

        icon_code = representative_item["weather"][0]["icon"]

        # Compact daily card
        day_card = tk.Frame(
            daily_forecast_frame,
            bg="#334155",
            padx=5,
            pady=4,
            width=190,
            height=145
        )

        day_card.pack(
            side="left",
            padx=4,
            pady=2
        )

        day_card.pack_propagate(False)

        day_label = tk.Label(
            day_card,
            text=date_key.strftime("%a, %d %b"),
            font=("Arial", 11, "bold"),
            fg="#38bdf8",
            bg="#334155"
        )

        day_label.pack(pady=1)

        icon_display = tk.Label(
            day_card,
            bg="#334155"
        )

        icon_display.pack(pady=0)

        try:

            icon_image = download_weather_icon(
                icon_code,
                (50, 50)
            )

            daily_icons.append(icon_image)

            icon_display.config(image=icon_image)

        except (requests.exceptions.RequestException, OSError) as error:

            print("Daily icon error:", error)

            icon_display.config(
                text="No icon",
                fg="white"
            )

        temperature_label = tk.Label(
            day_card,
            text=f"Max: {maximum_temp:.1f}°  Min: {minimum_temp:.1f}{symbol}",
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#334155"
        )

        temperature_label.pack(pady=1)

        condition_label = tk.Label(
            day_card,
            text=condition,
            font=("Arial", 9),
            fg="white",
            bg="#334155",
            wraplength=170
        )

        condition_label.pack(pady=1)


# ==========================================
# 4. SIX-HOUR FORECAST
# ==========================================

def display_hourly_forecast(forecast_items, timezone_offset):

    symbol = "°C" if current_unit == "metric" else "°F"

    for index in range(2):

        if index < len(forecast_items):

            item = forecast_items[index]

            forecast_time = (
                datetime.fromtimestamp(
                    item["dt"],
                    tz=timezone.utc
                ) + timedelta(seconds=timezone_offset)
            )

            time_text = forecast_time.strftime("%I:%M %p")

            temperature = item["main"]["temp"]

            condition = (
                item["weather"][0]["description"].title()
            )

            forecast_time_labels[index].config(
                text=time_text
            )

            forecast_detail_labels[index].config(
                text=f"{temperature:.1f} {symbol}\n{condition}"
            )

        else:

            forecast_time_labels[index].config(
                text="Unavailable"
            )

            forecast_detail_labels[index].config(
                text="No forecast data"
            )


# ==========================================
# 5. GET WEATHER
# ==========================================

def get_weather():

    global weather_icon

    city = city_entry.get().strip()

    if not city or city == "Enter city name":

        messagebox.showwarning(
            "Input Error",
            "Please enter a city name."
        )

        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": current_unit
    }

    try:

        # Current weather request
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # Current weather details
        city_label.config(
            text=f"City: {data['name']}, {data['sys']['country']}"
        )

        symbol = "°C" if current_unit == "metric" else "°F"

        temperature_label.config(
            text=f"{data['main']['temp']:.1f} {symbol}"
        )

        condition_label.config(
            text=data["weather"][0]["description"].title()
        )

        humidity_label.config(
            text=f"Humidity: {data['main']['humidity']} %"
        )

        wind_unit = "m/s" if current_unit == "metric" else "mph"

        wind_label.config(
            text=f"Wind Speed: {data['wind']['speed']} {wind_unit}"
        )

        # Current weather icon
        try:

            icon_code = data["weather"][0]["icon"]

            weather_icon = download_weather_icon(
                icon_code,
                (70, 70)
            )

            icon_label.config(image=weather_icon)

        except (requests.exceptions.RequestException, OSError) as error:

            icon_label.config(image="")
            print("Current icon error:", error)

        # Forecast request
        forecast_response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=10
        )

        forecast_response.raise_for_status()

        forecast_data = forecast_response.json()

        forecast_items = forecast_data.get("list", [])

        timezone_offset = forecast_data["city"]["timezone"]

        # Display hourly forecast
        display_hourly_forecast(
            forecast_items,
            timezone_offset
        )

        # Display five-day forecast
        display_five_day_forecast(
            forecast_items,
            timezone_offset
        )

    except requests.exceptions.HTTPError as error:

        status_code = (
            error.response.status_code
            if error.response is not None
            else None
        )

        if status_code == 404:

            messagebox.showerror(
                "City Not Found",
                "Please enter a valid city name."
            )

        elif status_code == 401:

            messagebox.showerror(
                "API Error",
                "Invalid API key."
            )

        else:

            messagebox.showerror(
                "Weather Error",
                f"API Error: {status_code}"
            )

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Timeout Error",
            "Request timed out. Please try again."
        )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(
            "Network Error",
            f"Check your internet connection.\n{error}"
        )

    except (KeyError, ValueError) as error:

        messagebox.showerror(
            "Data Error",
            f"Unable to process weather data.\n{error}"
        )


# ==========================================
# 6. CELSIUS / FAHRENHEIT TOGGLE
# ==========================================

def toggle_unit():

    global current_unit

    if current_unit == "metric":

        current_unit = "imperial"

        unit_button.config(
            text="Switch to °C"
        )

    else:

        current_unit = "metric"

        unit_button.config(
            text="Switch to °F"
        )

    city = city_entry.get().strip()

    if city and city != "Enter city name":
        get_weather()


# ==========================================
# 7. APPLICATION TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="WEATHER APP",
    font=("Arial", 26, "bold"),
    fg="white",
    bg="#1e293b"
)

title_label.pack(pady=5)


# ==========================================
# 8. CITY SEARCH
# ==========================================

search_frame = tk.Frame(
    root,
    bg="#1e293b"
)

search_frame.pack(pady=3)

city_entry = tk.Entry(
    search_frame,
    font=("Arial", 16),
    width=25,
    justify="center"
)

city_entry.pack(
    side="left",
    padx=10,
    ipady=7
)

city_entry.insert(0, "Enter city name")

search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Arial", 14, "bold"),
    bg="#38bdf8",
    fg="#0f172a",
    padx=20,
    pady=7,
    cursor="hand2",
    command=get_weather
)

search_button.pack(side="left")


# ==========================================
# 9. UNIT TOGGLE BUTTON
# ==========================================

unit_button = tk.Button(
    root,
    text="Switch to °F",
    font=("Arial", 11, "bold"),
    bg="#fbbf24",
    fg="#1e293b",
    padx=15,
    pady=7,
    cursor="hand2",
    command=toggle_unit
)

unit_button.pack(pady=2)


# ==========================================
# 10. CURRENT WEATHER PANEL
# ==========================================

weather_frame = tk.Frame(
    root,
    bg="#334155",
    padx=30,
    pady=3
)

weather_frame.pack(pady=2)

city_label = tk.Label(
    weather_frame,
    text="City: --",
    font=("Arial", 19, "bold"),
    fg="white",
    bg="#334155"
)

city_label.pack(pady=1)

icon_label = tk.Label(
    weather_frame,
    bg="#334155"
)

icon_label.pack(pady=0)

temperature_label = tk.Label(
    weather_frame,
    text="-- °C",
    font=("Arial", 27, "bold"),
    fg="#38bdf8",
    bg="#334155"
)

temperature_label.pack(pady=1)

condition_label = tk.Label(
    weather_frame,
    text="Weather: --",
    font=("Arial", 15),
    fg="white",
    bg="#334155"
)

condition_label.pack(pady=1)

humidity_label = tk.Label(
    weather_frame,
    text="Humidity: -- %",
    font=("Arial", 13),
    fg="white",
    bg="#334155"
)

humidity_label.pack(pady=1)

wind_label = tk.Label(
    weather_frame,
    text="Wind Speed: -- m/s",
    font=("Arial", 13),
    fg="white",
    bg="#334155"
)

wind_label.pack(pady=1)


# ==========================================
# 11. SIX-HOUR FORECAST SECTION
# ==========================================

forecast_title = tk.Label(
    root,
    text="NEXT 6 HOURS FORECAST",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#1e293b"
)

forecast_title.pack(pady=2)

forecast_frame = tk.Frame(
    root,
    bg="#1e293b"
)

forecast_frame.pack(pady=1)

forecast_time_labels = []
forecast_detail_labels = []

for index in range(2):

    forecast_card = tk.Frame(
        forecast_frame,
        bg="#334155",
        padx=20,
        pady=3,
        width=300,
        height=65
    )

    forecast_card.pack(
        side="left",
        padx=8
    )

    forecast_card.pack_propagate(False)

    time_label = tk.Label(
        forecast_card,
        text="--:--",
        font=("Arial", 13, "bold"),
        fg="#38bdf8",
        bg="#334155"
    )

    time_label.pack(pady=1)

    detail_label = tk.Label(
        forecast_card,
        text="Search a city",
        font=("Arial", 11),
        fg="white",
        bg="#334155"
    )

    detail_label.pack(pady=1)

    forecast_time_labels.append(time_label)
    forecast_detail_labels.append(detail_label)


# ==========================================
# 12. FIVE-DAY FORECAST SECTION
# ==========================================

daily_title = tk.Label(
    root,
    text="5-DAY WEATHER FORECAST",
    font=("Arial", 17, "bold"),
    fg="white",
    bg="#1e293b"
)

daily_title.pack(pady=3)

daily_forecast_frame = tk.Frame(
    root,
    bg="#1e293b"
)

daily_forecast_frame.pack(pady=1)


# ==========================================
# 13. ENTER KEY SUPPORT
# ==========================================

city_entry.bind(
    "<Return>",
    lambda event: get_weather()
)


# ==========================================
# 14. RUN APPLICATION
# ==========================================

root.mainloop()
