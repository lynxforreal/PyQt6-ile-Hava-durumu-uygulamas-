import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70℃", self)
        self.emoji_label = QLabel("☁️", self)
        self.description_label = QLabel("Sunny", self)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.emoji_label)
        self.setLayout(vbox) 

        # Alignment
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Object names for stylesheet
        self.city_label.setObjectName("city_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.city_input.setObjectName("city_input")

        # Styles
        self.setStyleSheet("""
            QLabel#city_label{
                color: Blue; 
                font-family: calibri;
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size:30px;
                font-weight:bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        # Button click
        self.get_weather_button.clicked.connect(self.Get_Weather)

    def Get_Weather(self):
        api_key = "40f94396122f5a3a3a908019928c4ac8"    
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:  
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.Display_Error("Bad requests \nPlease check your input")
                case 401:
                    self.Display_Error("Unauthorized \nInvalid API key")
                case 403:
                    self.Display_Error("Access is denied")
                case 404:
                    self.Display_Error("City not found")
                case 500:
                    self.Display_Error("Internal server error")
                case 502:
                    self.Display_Error("Bad Gateway")
                case 503:
                    self.Display_Error("Service is down")
                case 505:
                    self.Display_Error("Gateway timeout\nNo response from server")
                case _:
                    self.Display_Error("An unknown HTTP error occurred")

        except requests.exceptions.TooManyRedirects:
            self.Display_Error("Too many redirects")
        except requests.exceptions.ConnectionError:
            self.Display_Error("Connection error. Check your internet connection.")
        except requests.exceptions.Timeout:
            self.Display_Error("The request timed out")
        except requests.exceptions.ReadTimeout as req_error:
            self.Display_Error(f"Request error:\n{req_error}")

    def Display_Error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; color:red;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_description = data["weather"][0]["description"].capitalize()
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_c:.0f}℃")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather(weather_id))

    @staticmethod
    def get_weather(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌧️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🍃"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 800:
            return "☀️"
        elif weather_id == 781:
            return "🌪️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "❓"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
