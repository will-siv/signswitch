import RPi.GPIO as GPIO
import time

closed_pin = 19
open_pin = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(closed_pin, GPIO.OUT)
GPIO.setup(open_pin, GPIO.OUT)

def status():
  print(f"closed pin: {GPIO.input(closed_pin)}")
  print(f"open pin: {GPIO.input(open_pin)}")

def setup():
  GPIO.output(closed_pin, True)
  GPIO.output(open_pin, False)

def switch():
  GPIO.output(open_pin, not GPIO.input(open_pin))
  GPIO.output(closed_pin, not GPIO.input(closed_pin))
  
def main():
  setup()
  while True:
    time.sleep(1)
    switch()

if __name__ == "__main__":
  main()
