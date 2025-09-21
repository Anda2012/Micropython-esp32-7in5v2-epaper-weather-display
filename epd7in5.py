# epd7in5.py – Driver for Waveshare 7.5" T7 e-paper
from machine import Pin, SPI
import framebuf
import time

class EPD:
    WIDTH = 800
    HEIGHT = 480

    def __init__(self, spi, cs, dc, rst, busy):
        self.reset_pin = rst
        self.dc_pin = dc
        self.cs_pin = cs
        self.busy_pin = busy
        self.spi = spi

        self.cs_pin.init(Pin.OUT, value=1)
        self.dc_pin.init(Pin.OUT, value=0)
        self.reset_pin.init(Pin.OUT, value=0)
        self.busy_pin.init(Pin.IN)

        self.buffer = bytearray(self.WIDTH * self.HEIGHT // 8)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.WIDTH, self.HEIGHT, framebuf.MONO_HLSB)

    def digital_write(self, pin, value):
        pin.value(value)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray([command]))
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray([data]) if isinstance(data, int) else data)
        self.digital_write(self.cs_pin, 1)

    def wait_until_idle(self):
        while self.busy_pin.value() == 0:
            time.sleep_ms(100)

    def reset(self):
        self.digital_write(self.reset_pin, 0)
        time.sleep_ms(200)
        self.digital_write(self.reset_pin, 1)
        time.sleep_ms(200)

    def init(self):
        self.reset()

        self.send_command(0x01)  # POWER SETTING
        self.send_data(0x07)
        self.send_data(0x07)  # VGH=20V,VGL=-20V
        self.send_data(0x3f)  # VDH=15V
        self.send_data(0x3f)  # VDL=-15V

        self.send_command(0x04)  # POWER ON
        self.wait_until_idle()

        self.send_command(0x00)  # PANEL SETTING
        self.send_data(0x1F)     # LUT from OTP, 128x296

        self.send_command(0x61)  # Resolution setting
        self.send_data(0x03)     # 800 >> 8
        self.send_data(0x20)     # 800 & 0xff
        self.send_data(0x01)     # 480 >> 8
        self.send_data(0xE0)     # 480 & 0xff

        self.send_command(0X15)
        self.send_data(0x00)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x10)
        self.send_command(0X60)  # TCON SETTING
        self.send_data(0x22)

    def clear_frame(self, color=0xFF):
        for i in range(len(self.buffer)):
            self.buffer[i] = color


    def display_frame(self):
        self.send_command(0x10)
        self.send_data(self.buffer)

        self.send_command(0x13)
        self.send_data(self.buffer)

        self.send_command(0x12)
        self.wait_until_idle()

    def sleep(self):
        self.send_command(0x02)  # POWER_OFF
        self.wait_until_idle()
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0xA5)

    def draw_text(self, x, y, text):
        self.framebuf.text(text, x, y, 0x00)  # 0 = black
    
    def draw_icon(framebuf_obj, icon_bytes, x, y, width=40, height=40):
    # Convert bytes to bits and plot pixels
        for i in range(height):
            for j in range(width):
                byte_index = (i * width + j) // 8
                bit_index = 7 - (j % 8)
                if byte_index < len(icon_bytes):
                    if (icon_bytes[byte_index] >> bit_index) & 1:
                        framebuf_obj.pixel(x + j, y + i, 0)  # black pixel
                    else:
                        framebuf_obj.pixel(x + j, y + i, 1)  # white pixel


