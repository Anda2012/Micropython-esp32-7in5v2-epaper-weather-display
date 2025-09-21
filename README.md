#ESP32 E-Paper Weather Station
This project is a weather station built on an ESP32 with a 7.5-inch Waveshare e-Paper display and a DHT20 temperature & humidity sensor.
It connects to Wi-Fi, fetches live weather data from OpenWeatherMap, and displays it on the e-Paper screen along with local room temperature/humidity readings.
The display updates every 15 minutes and shows:

 Current weather condition (from OWM)

 Outdoor temperature & “feels like” temperature

 Humidity

 Wind speed & direction

 Rainfall (last 1h)

 Pressure

 Visibility

 Sunrise &  Sunset **(adjust line 80 to correct time zone # default is UTC +7)**

 Room temperature & humidity (via DHT20)

 Last updated time

ADDITIONAL FEATURES:

Automatic Wi-Fi reconnection

Auto-reset at midnight to prevent time drift

Low-power e-Paper display (black text on white background)

HARDWARE REQUIRED :

ESP32 board running micropython

7.5" Waveshare e-Paper display (SPI)

Waveshare e-Paper driver board / e-Paper driver hat (the one I'm using)

DHT20 I²C temperature & humidity sensor

Wi-Fi network with internet access

SETUP :
| e-Paper Pin | ESP32 Pin | Notes                                       |
| ----------- | --------- | ------------------------------------------- |
| **SCK**     | GPIO 18   | SPI Clock                                   |
| **MOSI**    | GPIO 23   | SPI Data                                    |
| **MISO**    | GPIO 19   | SPI Data In (not always needed for e-Paper) |
| **CS**      | GPIO 5    | Chip Select                                 |
| **DC**      | GPIO 17   | Data/Command                                |
| **RST**     | GPIO 16   | Reset                                       |
| **BUSY**    | GPIO 4    | Busy Pin (e-Paper status)                   |
| **GND**     | GND       | Ground                                      |
| **VCC**     | 3.3V      | Power                                       |
| **PWR**     | 3.3V      | Power                                       |

| DHT20 Pin | ESP32 Pin | Notes     |
| --------- | --------- | --------- |
| **SDA**   | GPIO 15   | I2C Data  |
| **SCL**   | GPIO 2    | I2C Clock |
| **VCC**   | 3.3V      | Power     |
| **GND**   | GND       | Ground    |

**NOTE**
When connecting the three 3.3v power wires you may need to make a power rail board for all 3 connections, most esp32's have only one 3.3v pin.

Copy secrets.py to ESP32 and fill in:

WIFI_SSID = "YourWiFiSSID"
WIFI_PASSWORD = "YourWiFiPassword"
OWM_API_KEY = "YourOpenWeatherMapAPIKey"
CITY = "Yourcity"
COUNTRY = "Yourcountry"

Flash main.py and epd7in5.py, dht20.py to your ESP32 running MicroPython.
