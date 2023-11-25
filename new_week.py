#!/bin/env python3

# tui that replaces the week closed schedule
import json
import sys

def printSchedule(d):
  # prints closed time schedule
  for key in d:
    s = f"{key}: "
    for time in d[key]:
      s += f"{time}, "
    if len(d[key]) == 0:
      print(s)
    else:
      print(s[0:-2])

def addNew(d, day):
  # guides user through adding a new closed time to the schedule
  print("not implemented yet, but will be soon!")


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

  while True:
    printSchedule(s)
    try:
      i = input("What day would you like to change?\nType \"stop\" to end input loop.\n")
      day = i.lower()
    except EOFError:
      sys.exit(0)
    print()
    if day == 'stop':
      break
    if day not in s:
      print(f"{day} is not valid.\n")
      continue
    addNew(s, day)

  print("Final schedule:\n")
  printSchedule(s)
  print(f"Now saving to {file}")
  json.dump(s, fp)

if __name__ == "__main__":
  main()
