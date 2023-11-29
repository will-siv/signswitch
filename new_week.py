#!/bin/env python3

# tui that replaces the week closed schedule
import json
import sys
import datetime

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

def printHelp():
  msg = """
  usage: [time1][+/-][time2]
  a time can be represented like 'xx:xx' or 'xx'
  '-': from time1 to time2
  '+': from time1 for time2 duration
  """
  print(msg)

def parseStmt(stmt):
  # [xx[:xx]][+/-][xx[:xx]]
  # returns 2-list of times, or False if not valid
  ret = []
  if "+" in stmt:
    plus = True
    times = stmt.split("+")
  else if "-" in stmt:
    plus = False
    times = stmt.split("-")
  else:
    print('error: missing operator')
    return False

  if len(times) != 2:
    print('error: invalid operation')
    return False

  for t in times:
    # make sure time is in correct format, standardize, and add to list
    hourmin = t.split(":")
    if len(hourmin) == 1:
      hourmin.append("00")
    if len(hourmin[0]) != 2 or len(hourmin[1]) != 2:
      # error for invalid time t

def addNew(d, day):
  # guides user through adding a new closed time to the schedule
  print("Type the times to close (24 hour)")
  print("Type ? for operations")
  try:
    stmt = input()
  except EOFError:
    return

  # handle operations
  if stmt == "?":
    printHelp()
    addNew(d, day)
    return
  out = parseStmt(stmt)
  if not out:
    print("Invalid input")

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
