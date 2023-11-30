#!/bin/env python3

# tui that replaces the week closed schedule

import json
import modifyclosedjson

def main():
  file = "weekly_closed_times.json"
  fp = open(file, 'w')
  s = {
        'sunday': [],
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': [],
        'saturday': []
      }

  # input loop
  err = modifyclosedjson.inputLoop(s)

  if err == "err":
    return

  print(f"Now saving to {file}")
  json.dump(s, fp)

if __name__ == "__main__":
  main()
