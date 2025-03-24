# importing modules
import time
from tkinter import *
from tkinter import messagebox as mb
import requests
from plyer import notification

# Function to get notification of weather report
def getNotification():
    cityName = place.get().strip()  # getting input of name of the place from user
    if not cityName:
        mb.showerror("Error", "Please enter a city name.")
        return

    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"  # base URL
    api_key = 'd850f7f52bf19300a9eb4b0aa6b80f0d'
    url = baseUrl + "appid=" + api_key + "&q=" + cityName

    try:
        response = requests.get(url)  # requesting the content of the URL
        x = response.json()  # converting it into JSON
        
        if x["cod"] != 200:
            mb.showerror("Error", f"City '{cityName}' not found!")
            return
        
        y = x["main"]  # getting the "main" key from JSON object
        temp_kelvin = y["temp"]
        temp_celsius = round(temp_kelvin - 273.15, 2)  # convert temperature from Kelvin to Celsius

        pres = y["pressure"]
        hum = y["humidity"]
        weather_desc = x["weather"][0]["description"].capitalize()

        # prepare info string
        info = (f"Here is the weather description for {cityName}:\n"
                f"Temperature: {temp_celsius}°C\n"
                f"Atmospheric pressure: {pres} hPa\n"
                f"Humidity: {hum}%\n"
                f"Description: {weather_desc}")

        # show notification
        notification.notify(
            title="YOUR WEATHER REPORT",
            message=info,
            timeout=4
        )

        # also show in a popup info box
        mb.showinfo("Weather Report", info)
        time.sleep(3)

    except Exception as e:
        mb.showerror('Error', str(e))  # show pop-up message if any error occurred

# creating the window
wn = Tk()
wn.title("Weather Forecast ")
wn.geometry('700x200')
wn.config(bg='azure')

# Heading label
Label(wn, text="Weather Forecast ", font=('Courier', 15), fg='grey19', bg='azure').place(x=100, y=15)

# Getting the place name
Label(wn, text='Enter the Location:', font=("Courier", 13), bg='azure').place(relx=0.05, rely=0.3)

place = StringVar(wn)
place_entry = Entry(wn, width=50, textvariable=place)
place_entry.place(relx=0.5, rely=0.3)

# Button to get notification
btn = Button(wn, text='Get Data', font=7, fg='grey19', command=getNotification)
btn.place(relx=0.4, rely=0.75)

# run the window till closed by user
wn.mainloop()
