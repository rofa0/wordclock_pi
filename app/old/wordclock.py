# from machine import Pin, Timer
import time

"""
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
"""



def wheel(pos):
    """
    Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r.
    """
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


class Wordclock(Layout):
    def __init__(self):

        # Zeit und Einstellungen:
        self.utc_corr = 2  # UTC Zeit korrektur
        self.hour = None
        self.minute = None
        self.second = None

        self.uhr = True,
        self.es_ist = True

        self.color = (0, 255, 229)
        self.style = "WORD"

        self.maxBrightness = 150
        self.minBrightness = 35
        self.AmbientLightPin = 0
        self.BRIGHTNESS = 255

        # List with all LED's which are ON depending on time
        self.leds_on = []
        self.data = []

        # Anzahl led's und gpio
        self.led_count = 114
        self.gpio = 15  # Wemos D1 = D8

        # Neopixel object erstellen
        self.np = neopixel.NeoPixel(machine.Pin(self.gpio), self.led_count)
        self.strip_clear()

        self.ntp_time_sync()
        self.get_time()
        print

    def ntp_time_sync(self):
        print("INFO: Time before synchronization：%s" % str(time.localtime()))
        ntptime.settime()
        print("INFO: Time after synchronization：%s" % str(time.localtime()))

    def get_time(self):
        # Time format: [2020, 10, 20, 21, 2, 52, 1, 294]
        # TODO Automatische winter sommerzeit korrektur
        local_time = list(time.localtime())
        self.hour = local_time[3] + self.utc_corr
        if self.hour >= 24:
            self.hour = self.hour - 24

        self.minute = local_time[4]
        self.second = local_time[5]

        # self.display = "{:2d}:{:2d}:{2d}".format(self.hour, self.minute, self.second)

    def get_leds(self):
        self.leds_on = []
        # Round minute to 5
        minute_round = int(self.minute / 5) * 5

        # Anzeigen von ES IST
        if self.es_ist:
            self.leds_on.extend(self.ES)
            self.leds_on.extend(self.IST)

        # Prüfen ob mehr als 20 nach, falls ja eine Stunde hinzufügen
        if minute_round > 20:
            self.hour = self.hour + 1

        # Wortuhr hat 12 Stunden und nicht 24:
        if self.hour > 12:
            self.leds_on.extend(self.STUNDEN[self.hour - 12])

        # bei 0 Uhr ist es zwölf
        elif self.hour == 0:

            self.leds_on.extend(self.STUNDEN[12])

        # Sonst die aktuelle Stunde verwenden
        else:
            self.leds_on.extend(self.STUNDEN[self.hour])

        # Anzeigen der einzelnen Minuten
        if minute_round != 0:
            self.leds_on.extend(self.MINUTEN[minute_round])

        # Anzeigen von UHR
        if self.uhr:
            self.leds_on.extend(self.UHR)

        # Für die vier LEDS in den Ecken:
        additional_minutes = self.minute % 10
        if 0 < additional_minutes < 5:
            self.leds_on.extend(self.ECKEN[additional_minutes])

        if additional_minutes > 5:
            self.leds_on.extend(self.ECKEN[additional_minutes - 5])

    def data_generator(self):
        self.data = []
        for i in range(self.led_count):
            if i in self.leds_on:
                self.data.append(self.color)
            else:
                self.data.append((0, 0, 0))

    def strip_clear(self):
        for i in range(self.led_count):
            self.np[i] = (0, 0, 0)
            self.np.write()

    def strip_show(self):
        for i in range(len(self.data)):
            self.np[i] = self.data[i]
            self.np.write()

    def change_color(self, red, green, blue):
        """
        Change LED color to red green and blue value
        """
        self.color = (red, green, blue)
        self.tick('dummy')

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.led_count):
                rc_index = (i * 256 // self.led_count) + j
                self.np[i] = wheel(rc_index & 255)
            self.np.write()
            time.sleep_ms(wait)

    def rainbow_clock(self):
        print("rainbow clock")

    def update_wordclock(self):
        self.get_leds()
        self.data_generator()
        self.strip_show()

    def tick(self, timer):
        """
        Clock Tick Method
        """
        # self.update_time()
        self.get_time()
        print("INFO: Tick {:02d}:{:02d}:{:02d}".format(self.hour, self.minute, self.second))
        self.update_wordclock()

    def start_timer(self, timer):
        self.tick('dummy')
        # deint begin timer
        timer_delta.deinit()

        global timer_1s
        timer_1s = machine.Timer(-1)
        timer_1s.init(period=60000, mode=machine.Timer.PERIODIC, callback=self.tick)

    def begin(self):
        """
        Method to start the clock, first sync the timer to the next minute
        then call the timer for every second
        """
        self.tick('dummy')
        global timer_delta
        timer_delta = machine.Timer(-1)
        # Calculate the delta to the next full minute.
        delta_next_minute = (60 - self.second) * 1000
        print("INFO: Delta to next minute: {}s".format(delta_next_minute / 1000))
        # Wait until the next minute is complete,
        # then start the 1 minute timer with start_timer Method
        timer_delta.init(period=delta_next_minute, mode=machine.Timer.ONE_SHOT, callback=self.start_timer)

    def end(self):
        try:
            timer_delta.deinit()
            timer_1s.deinit()
        except NameError as e:
            # If the webserver get request for off bevore the clock was on then
            # error occurs because timer is not defined. Also for 1s timer when
            # the interval is not reached.
            pass

        self.strip_clear()
