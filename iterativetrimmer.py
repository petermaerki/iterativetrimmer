#!/usr/bin/python
# Autor: Peter Maerki, 2017, Switzerland.
# Please feel free to adopt to your needs.
# This script is a quick hack. No guarantee at all!
# See www.positron.ch/iterativetrimmer
from __future__ import annotations
import random
import math


class IterativeTrimmer:
    _TOLERANZ = 0.015 / 100.0
    """
    Standardtoleranz meiner Duennfilmwiderstaende 0.5%, gemessen am 17.1.14 anhand von 20 Widerstaenden
    """

    _UNENDLICH = 1000000000000.0
    _BRUECKE = 0.001
    _WERTE = (
        10,
        11,
        12,
        13,
        15,
        16,
        18,
        20,
        22,
        24,
        27,
        30,
        33,
        36,
        39,
        43,
        47,
        51,
        56,
        62,
        68,
        75,
        82,
        91,
        100,
    )
    _WIDERSTANDSWERTE = [x * f for x in _WERTE for f in (
        1.0,
        10.0,
        100.0,
        1000.0,
        10000.0
    )]
    _WIDERSTANDSWERTE.append(_BRUECKE)  # zusaetzliche Werte anfuegen
    _WIDERSTANDSWERTE = sorted(_WIDERSTANDSWERTE)

    def __init__(self, sollwert: float):
        assert isinstance(sollwert, float)

        kombinationen_ab = [
            (a, b)
            for a in self._WIDERSTANDSWERTE
            for b in self._WIDERSTANDSWERTE
            if a < sollwert * (1 - self._TOLERANZ)
            if a + b > sollwert * (1 + self._TOLERANZ + 0.001)
            if a > b
            if a != self._BRUECKE
            if b != self._BRUECKE
        ]
        if len(kombinationen_ab) > 0:
            loesungen = sorted(
                kombinationen_ab, key=lambda x: abs(x[1] + x[0] - sollwert) / sollwert
            )
            # cmp(x, y)	-1 if x < y, 0 if x == y, or 1 if x > y    +((cmp(200.0, x[1])+1.0)/2.0*sollwert/100.0)+((cmp(x[1], x[0])+1.0)/2.0*sollwert/100.0)
            # while len(loesungen)>2 and loesungen[0][1]<200: # falls kleiner 20 ohm ist schwierig abzugleichen
            #  loesungen.pop(0)
            loesung = loesungen[0]
        else:
            loesung = (self._UNENDLICH, self._UNENDLICH)
        # print("Sollwert    :", int(sollwert)
        # print("Widerstand A:", int(loesung[0]), " bei zwei Widerstaenden der alleinstehende"
        # print("Widerstand B:", int(loesung[1]), " bei zwei Widerstaenden der mit anderen parallele"

        kombinationen_c = [
            c for c in self._WIDERSTANDSWERTE if c > sollwert * (1 + self._TOLERANZ + 0.0003)
        ]
        if len(kombinationen_c) > 0:
            loesung_c = sorted(kombinationen_c)[0]
            if sollwert > max(self._WIDERSTANDSWERTE):
                loesung_c = self._UNENDLICH  # hack, obs wirklich besser ist weiss ich nicht
        else:
            loesung_c = self._UNENDLICH
        # print("Widerstand C:", int(loesung_c), " der parallele"

        kombinationen_d = [(d, abs(1 / d - 1 / sollwert)) for d in self._WIDERSTANDSWERTE]
        if len(kombinationen_d) > 0:
            loesung_d = sorted(kombinationen_d, key=lambda x: x[1])[0][0]
            if sollwert > max(self._WIDERSTANDSWERTE):
                loesung_d = self._UNENDLICH  # hack, obs wirklich besser ist weiss ich nicht
        else:
            loesung_d = self._UNENDLICH

        # print("Widerstand D:", int(loesung_d[0]), ' mit Abweichung von %0.2f' % (loesung_d[1]*100), " %", " der letzte parallele"
        # print(" "
        self.sollwert = sollwert
        self.loesung_a = loesung[0]
        self.loesung_b = loesung[1]
        self.loesung_c = loesung_c
        self.loesung_d = loesung_d

    def toleranzen(self, widerstandswert, toleranz):
        if widerstandswert <= 0:
            return widerstandswert
        else:
            return random.gauss(
                widerstandswert, widerstandswert * toleranz * 0.5
            )  # random.gauss(mu, sigma): mean mu and standard deviation sigma

    @staticmethod
    def fehler(sollwert: float, istwert: float):
        fehler = abs((istwert / sollwert) - 1)
        return fehler

    @staticmethod
    def sollwert_random(min: float, max: float):
        return pow(10, random.uniform(math.log10(min), math.log10(max)))


def main():
    print("Find fix value resistors to adjust a resistor")
    print("2017, Peter Maerki")
    print("")
    while True:
        sollwert = float(input("Measured resistance by potentiometer [Ohm]: "))
        trimmer = IterativeTrimmer(sollwert)

        print(f"Target    : {sollwert:0.0f}")
        print(
            f"Resistor A: {trimmer.loesung_a:0.0f} bei zwei Widerstaenden der Alleinstehende",
        )
        print(
            f"Resistor B: {trimmer.loesung_b:0.0f} bei zwei Widerstaenden der mit anderen Parallele",
        )
        print(f"Resistor C: {trimmer.loesung_c:0.0f} der Parallele")
        print(
            f"Resistor D: {trimmer.loesung_c:0.0f} mit Abweichung von {(trimmer.loesung_d - sollwert) / sollwert * 100:0.2f}% der letzte Parallele",
        )
        print(" ")


if __name__ == "__main__":
    main()
