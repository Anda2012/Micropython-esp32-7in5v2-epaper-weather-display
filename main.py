import time
import network
import urequests
import epd7in5
import ntptime
import machine
from dht20 import DHT20
from machine import Pin, SPI, I2C
from secrets import WIFI_SSID, WIFI_PASSWORD, OWM_API_KEY, CITY, COUNTRY

# Initialize e-Paper display
spi = SPI(2, baudrate=2000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)
epd = epd7in5.EPD(spi, cs, dc, rst, busy)

# Initialize DHT20
i2c0_sda = Pin(15)
i2c0_scl = Pin(2)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)
dht20 = DHT20(0x38, i2c0)

# Connect to Wi-Fi and sync NTP time
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected:", wlan.ifconfig())

    # Sync time via NTP (sets to UTC)
    try:
        ntptime.settime()
        print("Time synchronized via NTP")
    except:
        print("Failed to sync time")

# Fetch weather data from OpenWeatherMap API
def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&appid={OWM_API_KEY}&units=metric"
    response = urequests.get(url)
    data = response.json()
    response.close()
    
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    wind_deg = data["wind"].get("deg", 0)
    visibility = data.get("visibility", 0)
    sunrise = data["sys"]["sunrise"]
    sunset = data["sys"]["sunset"]
    
    rain = data.get("rain", {}).get("1h", 0)
    snow = data.get("snow", {}).get("1h", 0)
    
    return {
        "condition": weather,
        "temp": temp,
        "feels": feels,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "wind_deg": wind_deg,
        "visibility": visibility,
        "sunrise": sunrise,
        "sunset": sunset,
        "rain": rain,
        "snow": snow
    }

# Convert Unix timestamp to hh:mm
def format_time(ts, tz_offset=0): #offset 0 is acctually utc+7 adjust as needed
    t = time.localtime(ts + tz_offset * 3600)
    return "{:02d}:{:02d}".format(t[3], t[4])

# Draw weather info on e-Paper
def draw_weather(w):
    epd.init()
    epd.clear_frame()
    fb = epd.framebuf
    
    measurements = dht20.measurements
    fb.fill(1)  # White background
    color = 0   # Black text

    fb.text(f"Condition: {w['condition']}", 20, 30, color)
    fb.text(f"Temperature: {w['temp']} 'C (feels {w['feels']} 'C)", 20, 70, color)
    fb.text(f"Humidity: {w['humidity']}%", 20, 110, color)
    fb.text(f"Room Temp: {measurements['t']} 'C  Humidity: {measurements['rh']}%", 20, 150, color)
    fb.text(f"Wind: {w['wind_speed']} m/s, {w['wind_deg']}'", 20, 190, color)
    fb.text(f"Rain (1h): {w['rain']} mm", 20, 230, color)
    fb.text(f"Pressure: {w['pressure']} hPa", 20, 270, color)
    fb.text(f"Visibility: {w['visibility']} m", 20, 310, color)
    fb.text(f"Sunrise: {format_time(w['sunrise'], tz_offset=7)}", 20, 350, color)
    fb.text(f"Sunset: {format_time(w['sunset'], tz_offset=7)}", 20, 390, color)

    # Last updated in Thailand time (UTC+7)
    last_update = int(time.time())
    fb.text(f"Last Updated: {format_time(last_update, tz_offset=7)}", 20, 430, color)

    epd.display_frame()
    epd.sleep()

# Main function
def main():
    connect_wifi()
    while True:
        weather = fetch_weather()
        draw_weather(weather)
        
        # Check local Thailand time
        t = time.localtime(time.time() + 7 * 3600)
        hour = t[3]
        minute = t[4]

        # Reset device at midnight
        if hour == 0 and minute == 0:
            print("Reached midnight, resetting...")
            machine.reset()

        # Sleep for 15 minutes
        time.sleep(900)

main()

