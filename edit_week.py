#!/bin/env python3

# tui to make edits to the existing week schedule
# same as new week just loads the old schedule

import json
import modifyclosedjson

def main():
  file = "weekly_closed_times.json"
  fp = open(file, 'r')
  try:
    s = json.load(fp)
  except json.decoder.JSONDecodeError:
    s = {
        'sunday': [],
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': [],
        'saturday': []
      }
  fp.close()
  fp = open(file, 'w')

  # input loop
  err = modifyclosedjson.inputLoop(s)

  if err:
    return

  print(f"Now saving to {file}")
  json.dump(s, fp)

if __name__ == "__main__":
  main()
