#!/usr/bin/python
# Autor: Peter Maerki, 2017, Switzerland.

import random
import math

toleranz = 0.015/100.0 # Standardtoleranz meiner Duennfilmwiderstaende 0.5%, gemessen am 17.1.14 anhand von 20 Widerstaenden
unendlich = 1000000000000.0
bruecke = 0.001
werte = (10,11,12,13,15,16,18,20,22,24,27,30,33,36,39,43,47,51,56,62,68,75,82,91,100)

widerstandswerte = []
for faktor in (1.0, 10.0, 100.0, 1000.0, 10000.0):
  widerstandswerte.extend([x*faktor for x in werte])
widerstandswerte.append(bruecke) #zusaetzliche Werte anfuegen
#widerstandswerte.append(unendlich) #zusaetzliche Werte anfuegen
widerstandswerte =  sorted(widerstandswerte)

def widerstandermitteln (sollwert, widerstandswerte):
  if sollwert == '':
    sollwert = 343
  sollwert = float(sollwert)

  kombinationen_ab = [(a, b) for a in widerstandswerte for b in widerstandswerte if a < sollwert*(1-toleranz) if a + b > sollwert*(1+toleranz+0.001) if a > b if a!=bruecke if b!=bruecke]
  if len(kombinationen_ab) > 0:
    loesungen = sorted(kombinationen_ab,key=lambda x: abs(x[1]+x[0]-sollwert)/sollwert)
    # cmp(x, y)	-1 if x < y, 0 if x == y, or 1 if x > y    +((cmp(200.0, x[1])+1.0)/2.0*sollwert/100.0)+((cmp(x[1], x[0])+1.0)/2.0*sollwert/100.0)
    #while len(loesungen)>2 and loesungen[0][1]<200: # falls kleiner 20 ohm ist schwierig abzugleichen
    #  loesungen.pop(0)
    loesung =  loesungen[0]
  else:
    loesung = (unendlich, unendlich)
  #print "Sollwert    :", int(sollwert)
  #print "Widerstand A:", int(loesung[0]), " bei zwei Widerstaenden der alleinstehende"
  #print "Widerstand B:", int(loesung[1]), " bei zwei Widerstaenden der mit anderen parallele"

  kombinationen_c = [c for c in widerstandswerte if c > sollwert*(1+toleranz+0.0003)]
  if len(kombinationen_c) > 0:
    loesung_c = sorted(kombinationen_c)[0]
    if sollwert > max(widerstandswerte):
      loesung_c =  unendlich # hack, obs wirklich besser ist weiss ich nicht
  else:
    loesung_c = unendlich
  #print "Widerstand C:", int(loesung_c), " der parallele"

  kombinationen_d = [ (d, abs(1/d-1/sollwert)) for d in widerstandswerte]
  if len(kombinationen_d) > 0:
    loesung_d =  sorted(kombinationen_d,key=lambda x: x[1])[0][0]
    if sollwert > max(widerstandswerte):
      loesung_d =  unendlich # hack, obs wirklich besser ist weiss ich nicht
  else:
    loesung_d =  unendlich
    
  #print "Widerstand D:", int(loesung_d[0]), ' mit Abweichung von %0.2f' % (loesung_d[1]*100), " %", " der letzte parallele"
  #print " "
  return{'sollwert':sollwert, 'a':loesung[0], 'b':loesung[1], 'c':loesung_c, 'd':loesung_d}

def toleranzen(widerstandswert, toleranz):
  if widerstandswert <= 0:
    return widerstandswert
  else:
    return random.gauss(widerstandswert, widerstandswert*toleranz*0.5) # random.gauss(mu, sigma): mean mu and standard deviation sigma

def fehler(sollwert, istwert):
  fehler = abs((istwert/sollwert)-1)
  return fehler

def sollwert_random(min, max):
  sollwert = pow(10,random.uniform(math.log10(min),math.log10(max)))
  return sollwert

print "Find fix value resistors to adjust a resistor"
print "2017, Peter Maerki"
print ""

if __name__ == "__main__":
  while True:
    sollwert = float(raw_input("Measured resistance by potentiometer, Ohm's?"))
    loesung = widerstandermitteln(sollwert,widerstandswerte)

    print "Target    :", int(sollwert)
    print "Resistor A:", int(loesung['a']), " bei zwei Widerstaenden der alleinstehende"
    print "Resistor B:", int(loesung['b']), " bei zwei Widerstaenden der mit anderen parallele"
    print "Resistor C:", int(loesung['c']), " der parallele"
    print "Resistor D:", int(loesung['d']), ' mit Abweichung von %0.2f' % ((loesung['d']-sollwert)/sollwert*100), "%", " der letzte parallele"
    print " "
