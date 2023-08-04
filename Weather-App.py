import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def show_advanced_weather_info(city):
    advanced_window = tk.Toplevel()
    advanced_window.title("Advanced Weather Info")
    advanced_window.geometry("800x600")

    base_url = "http://api.weatherapi.com/v1/forecast.json"
    api_key = "4421923a24f545e4acc220651230308"

    params = {
        "key": api_key,
        "q": city,
        "days": 3,  # Fetch 3-day forecast (includes the current day)
        "aqi": "no",
        "alerts": "no",
        "lang": "en"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", f"Error: {data['error']['message']}")
        else:
            advanced_canvas = tk.Canvas(advanced_window)
            advanced_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(advanced_window, orient=tk.VERTICAL, command=advanced_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            advanced_canvas.configure(yscrollcommand=scrollbar.set)
            advanced_canvas.bind('<Configure>', lambda e: advanced_canvas.configure(scrollregion=advanced_canvas.bbox("all")))
            advanced_canvas.bind_all("<MouseWheel>", lambda event: advanced_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

            advanced_frame = ttk.Frame(advanced_canvas)
            advanced_canvas.create_window((0, 0), window=advanced_frame, anchor="nw")

            for day in data["forecast"]["forecastday"]:
                date = day["date"]
                max_temp_c = day["day"]["maxtemp_c"]
                min_temp_c = day["day"]["mintemp_c"]
                avg_temp_c = day["day"]["avgtemp_c"]
                max_temp_f = celsius_to_fahrenheit(max_temp_c)
                min_temp_f = celsius_to_fahrenheit(min_temp_c)
                avg_temp_f = celsius_to_fahrenheit(avg_temp_c)

                weather_info = (
                    f"{date}\n"
                    f"Max Temp: {max_temp_f:.1f}°F, Min Temp: {min_temp_f:.1f}°F, Avg Temp: {avg_temp_f:.1f}°F\n"
                    f"Description: {day['day']['condition']['text'].capitalize()}\n"
                    f"Max Wind: {day['day']['maxwind_mph']} mph, {day['day']['maxwind_kph']} km/h\n"
                    f"Total Precipitation: {day['day']['totalprecip_in']} in, {day['day']['totalprecip_mm']} mm\n"
                    f"Avg Visibility: {day['day']['avgvis_miles']} miles, {day['day']['avgvis_km']} km\n"
                    f"Avg Humidity: {day['day']['avghumidity']}%\n"
                    f"UV Index: {day['day']['uv']}\n\n"
                    f"Sunrise: {day['astro']['sunrise']}, Sunset: {day['astro']['sunset']}\n"
                    f"Moonrise: {day['astro']['moonrise']}, Moonset: {day['astro']['moonset']}\n\n"
                )

                day_info = tk.Label(advanced_frame, text=weather_info)
                day_info.pack()

                hourly_data = day["hour"]
                hourly_info = tk.Label(advanced_frame, text="Hourly Weather Information:", font=("Helvetica", 12, "bold"))
                hourly_info.pack(pady=5)

                for hour in hourly_data:
                    time = hour["time"]
                    temp_c = hour["temp_c"]
                    temp_f = celsius_to_fahrenheit(temp_c)
                    description = hour["condition"]["text"]

                    hourly_weather_info = (
                        f"{time}\n"
                        f"Temperature: {temp_f:.1f}°F, Description: {description.capitalize()}\n\n"
                    )

                    hour_info = tk.Label(advanced_frame, text=hourly_weather_info)
                    hour_info.pack()

                # Add a separator between days
                ttk.Separator(advanced_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def show_weather_info(city):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    api_key = "4421923a24f545e4acc220651230308"

    params = {
        "key": api_key,
        "q": city,
        "days": 3,  # Fetch 3-day forecast (includes the current day)
        "aqi": "no",
        "alerts": "no",
        "lang": "en"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", f"Error: {data['error']['message']}")
        else:
            current = data["current"]
            forecast_days = data["forecast"]["forecastday"]

            forecast_info = ""

            for day in forecast_days:
                date = day["date"]
                max_temp_c = day["day"]["maxtemp_c"]
                min_temp_c = day["day"]["mintemp_c"]
                description = day["day"]["condition"]["text"]

                # Convert Celsius temperatures to Fahrenheit
                max_temp_f = celsius_to_fahrenheit(max_temp_c)
                min_temp_f = celsius_to_fahrenheit(min_temp_c)

                forecast_info += (
                    f"{date}\n"
                    f"Max Temp: {max_temp_f:.1f}°F, Min Temp: {min_temp_f:.1f}°F\n"
                    f"Description: {description.capitalize()}\n\n"
                )

            # Convert current temperature to Fahrenheit
            current_temp_c = current['temp_c']
            current_temp_f = celsius_to_fahrenheit(current_temp_c)

            weather_message = (
                f"Weather in {city}:\n"
                f"Current Temperature: {current_temp_f:.1f}°F\n"
                f"Description: {current['condition']['text'].capitalize()}\n"
                f"Humidity: {current['humidity']}%\n"
                f"Wind Speed: {current['wind_kph']} km/h\n\n"
                f"{forecast_info}"
            )

            weather_label.config(text=weather_message)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def get_weather_button_click():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
    else:
        show_weather_info(city)


def on_enter_key(event):
    get_weather_button_click()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather App")

    root.geometry("600x450")

    city_label = tk.Label(root, text="Enter city name:")
    city_label.pack()

    city_entry = ttk.Entry(root)
    city_entry.pack()

    get_weather_button = ttk.Button(root, text="Get Weather", command=get_weather_button_click)
    get_weather_button.pack()

    advanced_button = ttk.Button(root, text="Advanced", command=lambda: show_advanced_weather_info(city_entry.get()))
    advanced_button.pack()

    city_entry.bind('<Return>', on_enter_key)

    weather_label = tk.Label(root, text="", font=("Helvetica", 12))
    weather_label.pack()

    root.mainloop()