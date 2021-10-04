
#from machine import Pin, Timer
import time


"""
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
"""

class Layout:
    """
    =========================================================================================//
                                              LED Layout                                     //
    =========================================================================================//
      112                                                                               111
           100/E  101/S  102/K  103/I  104/S  105/C  106/H  107/A  108/F  109/Ü  110/F
           99/V   98/I   97/E   96/R   95/T   94/U   93/B   92/F   91/Z   90/Ä   89/Ä
           78/Z   79/W   80/Ä   81/N   82/Z   83/G   84/S   85/I   86/V   87/O   88/R
           77/A   76/B   75/O   74/H   73/A   72/U   71/B   70/I   69/E   68/G   67/E
           56/E   57/I   58/S   59/Z   60/W   61/Ö   62/I   63/S   64/D   65/R   66/Ü
           55/V   54/I   53/E   52/R   51/I   50/F   49/Ü   48/F   47I    46/Q   45/T
           34/S   35/Ä   36/C   37/H   38/S   39/I   40/S   41/I   42/B   43/N   44/I
           33/A   32/C   31/H   30/T   29/I   28/N   27/Ü   26/N   25/I   24/E   23/L
           12/Z   13/Ä   14/N   15/I   16/E   17/R   18/B   19/Ö   20/U   21/F   22/I
           11/Z   10/W   9/Ö    8/U    7/F    6/I    5/N    4/A    3/U    2/H    1/R
      113                                                                                0
     """

    # Fünf Minuten Schritte
    nach = [77, 76]
    vor = [86, 87, 88]
    halb = [74, 73, 72, 71, 70]
    fünf = [108, 109, 110]
    zehn = [91, 90, 89]
    zwanzig = [78, 79, 80, 81, 82, 83]
    viertel = [94, 95, 96, 97, 98, 99]

    MINUTEN = {
        5: fünf + nach,  # Fünf nach
        10: zehn + nach,  # Zehn nach
        15: viertel + nach,  # Viertel Nach
        20: zwanzig + nach,  # Zwanzig nach"
        25: fünf + vor + halb,  # Fünf vor halb
        30: halb,  # Halb
        35: fünf + nach + halb,  # Fünf nach Halb
        40: zwanzig + vor,  # Zwanzig vor
        45: viertel + vor,  # Viertel vor
        50: zehn + vor,  # Zehn vor
        55: fünf + vor,  # Fünf vor
    }

    # Stunden
    STUNDEN = {
        1: [56, 57, 58],
        2: [59, 60, 61, 62],
        3: [64, 65, 66],
        4: [55, 54, 53, 52, 51],
        5: [50, 49, 48, 57],
        6: [34, 35, 36, 37, 38, 39],
        7: [40, 41, 42, 43, 44],
        8: [29, 30, 31, 32, 33],
        9: [28, 27, 26, 25],
        10: [12, 13, 14, 15],
        11: [19, 20, 21, 22],
        12: [11, 10, 9, 8, 7, 6],
    }

    # Einzelne Minuten in den Ecken
    ECKEN = {
        1: [111],
        2: [111, 0],
        3: [111, 0, 113],
        4: [111, 0, 113, 112]
    }

    ES = [100, 101]
    IST = [103, 104, 105, 106]
    UHR = [3, 2, 1]


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
        self.gpio = 15 # Wemos D1 = D8

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
        #self.update_time()
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
        delta_next_minute = (60 - self.second)*1000
        print("INFO: Delta to next minute: {}s".format(delta_next_minute/1000))
        # Wait until the next minute is complete,
        # then start the 1 minute timer with start_timer Method
        timer_delta.init(period=delta_next_minute, mode = machine.Timer.ONE_SHOT, callback = self.start_timer)
        
        
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
        
