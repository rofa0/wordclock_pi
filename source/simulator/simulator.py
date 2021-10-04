from main.wordclock import Wordclock as wordclock
import numpy as np
import numpy.ma as ma

LETTER_MAP = np.array([
    ["E", "S", "K", "I", "S", "C", "H", "A", "F", "Ü", "F"],
    ["V", "I", "E", "R", "T", "U", "B", "F", "Z", "Ä", "Ä"],
    ["Z", "W", "Ä", "N", "Z", "G", "S", "I", "V", "O", "R"],
    ["A", "B", "O", "H", "A", "U", "B", "I", "E", "G", "E"],
    ["E", "I", "S", "Z", "W", "Ö", "I", "S", "D", "R", "Ü"],
    ["V", "I", "E", "R", "I", "F", "Ü", "F", "I", "Q", "T"],
    ["S", "Ä", "C", "H", "S", "I", "S", "I", "B", "N", "I"],
    ["A", "C", "H", "T", "I", "N", "Ü", "N", "I", "E", "L"],
    ["Z", "Ä", "N", "I", "E", "R", "B", "Ö", "U", "F", "I"],
    ["Z", "W", "Ö", "U", "F", "I", "N", "A", "U", "H", "R"]
])

LED_MAP = np.array([
    [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    [99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89],
    [78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88],
    [77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67],
    [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66],
    [55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45],
    [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
    [33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23],
    [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
])


def get_leds(hour, minute):
    leds_on = []
    # Round minute to 5
    minute_round = int(minute / 5) * 5

    # Prüfen ob mehr als 20 nach, falls ja eine Stunde hinzufügen
    if minute_round > 20:
        hour = hour + 1

    # Wortuhr hat 12 Stunden und nicht 24:
    if hour > 12:
        leds_on.extend(wordclock.STUNDEN[hour - 12])

    # bei 0 Uhr ist es zwölf
    elif hour == 0:

        leds_on.extend(wordclock.STUNDEN[12])

    # Sonst die aktuelle Stunde verwenden
    else:
        leds_on.extend(wordclock.STUNDEN[hour])

    # Anzeigen der einzelnen Minuten
    if minute_round != 0:
        leds_on.extend(wordclock.MINUTEN[minute_round])

    # # Anzeigen von UHR
    # if uhr:
    #     leds_on.extend(UHR)

    # Für die vier LEDS in den Ecken:
    additional_minutes = minute % 10
    if 0 < additional_minutes < 5:
        leds_on.extend(wordclock.ECKEN[additional_minutes])

    if additional_minutes > 5:
        leds_on.extend(wordclock.ECKEN[additional_minutes - 5])

    return leds_on


def simulate_wordclock(hour, minute):
    led_map_copy = np.copy(LED_MAP)
    for value in get_leds(hour, minute):
        led_map_copy[led_map_copy == value] = "0"
    c = ma.masked_where(led_map_copy != 0, LETTER_MAP)
    return (c)


def ndtotext(A, w=None, h=None):
    """
    pretty print np.ndarray
    """
    if A.ndim == 1:
        if w == None:
            return str(A)
        else:
            s = '[' + ' ' * (max(w[-1], len(str(A[0]))) - len(str(A[0]))) + str(A[0])
            for i, AA in enumerate(A[1:]):
                s += ' ' * (max(w[i], len(str(AA))) - len(str(AA)) + 1) + str(AA)
            s += '] '
    elif A.ndim == 2:
        w1 = [max([len(str(s)) for s in A[:, i]]) for i in range(A.shape[1])]
        w0 = sum(w1) + len(w1) + 1
        s = u'\u250c' + u'\u2500' * w0 + u'\u2510' + '\n'
        for AA in A:
            s += ' ' + ndtotext(AA, w=w1) + '\n'
        s += u'\u2514' + u'\u2500' * w0 + u'\u2518'
    elif A.ndim == 3:
        h = A.shape[1]
        s1 = u'\u250c' + '\n' + (u'\u2502' + '\n') * h + u'\u2514' + '\n'
        s2 = u'\u2510' + '\n' + (u'\u2502' + '\n') * h + u'\u2518' + '\n'
        strings = [ndtotext(a) + '\n' for a in A]
        strings.append(s2)
        strings.insert(0, s1)
        s = '\n'.join(''.join(pair) for pair in zip(*map(str.splitlines, strings)))
    return s


if __name__ == "__main__":

    sim_time = []
    for hour in range(0, 24):
        for minute in range(0, 60):
            display = "{:02d}:{:02d}".format(hour, minute)

            clock = simulate_wordclock(hour, minute)
            sim_time.append([display, clock])
            print(display)
            print(ndtotext(clock))
            print("")
            print("")
