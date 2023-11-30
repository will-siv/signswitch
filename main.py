import RPi.GPIO as GPIO
import time
import json
import modifyclosedjson

closed_pin = 19
open_pin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(closed_pin, GPIO.OUT)
GPIO.setup(open_pin, GPIO.OUT)

GPIO.output(open_pin, False)
GPIO.output(closed_pin, True)

# returns True if open
def status():
  print(f"closed pin: {GPIO.input(closed_pin)}")
  print(f"open pin: {GPIO.input(open_pin)}")

def switch():
  GPIO.output(open_pin, not GPIO.input(open_pin))
  GPIO.output(closed_pin, not GPIO.input(closed_pin))

def sign_open():
  GPIO.output(open_pin, True)
  GPIO.output(closed_pin, False)

def sign_closed():
  GPIO.output(closed_pin, True)
  GPIO.output(open_pin, False)

def main():
  while True:
    t = time.localtime()
    file = "weekly_closed_times.json"
    fp = open(file, 'r')
    try:
      s = json.load(fp)
    except json.decoder.JSONDecodeError:
      print("json file not valid!")
      return
    day = time.ctime()[0:3].lower()
    day = modifyclosedjson.completeDay(s, day)
    hour = t.tm_hour
    minute = t.tm_min

    currentDay = s[day]
    closed = False
    for t1, t2 in currentDay:
      if t1 <= [hour, minute] and [hour, minute] < t2:
        sign_closed()
        closed = True
        break

    # if none of the times line up, then it's open
    if not closed:
      sign_open()

    time.sleep(1)
    fp.close()

if __name__ == "__main__":
  main()
