#!/bin/env python3

# helper functions for guiding user through the tui
import json

# converts dumb format i have into human readable
# i will merge the time struct into this soon(tm)
def readableTime(a):
  [h1, m1], [h2, m2] = a
  return f'%02d:%02d-%02d:%02d'% (h1, m1, h2, m2)

def printSchedule(d):
  # prints closed time schedule
  for key in d:
    s = f"{key}: "
    for time in d[key]:
      time = readableTime(time)
      s += f"{time}, "
    if len(d[key]) == 0:
      print(s)
    else:
      print(s[0:-2])

def printHelp():
  msg = """
  format: [time1][+/-][time2]
  a time can be represented like 'xx:xx' or 'xx'
  '-': from time1 to time2
  '+': from time1 for time2 duration

  overflowing times to next day are allowed, but only once
  (eg: 21:00-07:00)

## barely implemented
  to remove times, add a '-' before the time format
  """
  print(msg)

def getNextDay(d, day):
  temp = list(d)
  try:
    return temp[temp.index(day) + 1]
  except (ValueError, IndexError):
    return "sunday"

# TODO not at all done, missing entire features
def removeFromDay(d, day, out):
  print(out)
  tx, ty = out
  if tx[0] > ty[0]:
    # next day - untested btw
    removeFromDay(d, getNextDay(d, day), [[0, 0], ty])
    ty = [23, 59]
  i = 0
  removing = False
  while i < len(d[day]):
    t1, t2 = d[day][i]
    if t1 < tx and t2 > ty:
      # remove is happening between - split
      d[day][i][1] = tx
      d[day].insert(i+1,[ty, t2])
      return
    i += 1

# TODO bug here - does not correctly overwrite sometimes
def addToDay(d, day, out):
  [h1, m1], [h2, m2] = out
  if h1 > h2:
    # next day
    d[day].append([[h1, m1], [23, 59]])
    h1, m1 = 0, 0
    day = getNextDay(d, day)
  d[day].append([[h1, m1], [h2, m2]])
  # refresh added day
  d[day] = sorted(d[day])
  i = 0
  while i < len(d[day]) - 1:
    t1, t2 = d[day][i]
    t3, t4 = d[day][i+1]
    if t3 <= t2:
      d[day][i][1] = t4
      d[day].pop(i+1)
      continue
    i += 1

def parseStmt(stmt):
  # [xx[:xx]][+/-][xx[:xx]]
  # returns 2-list of times, or False if not valid
  ret = []
  if "+" in stmt:
    plus = True
    times = stmt.split("+")
  elif "-" in stmt:
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
    if (len(hourmin[0]) != 2 or len(hourmin[1]) != 2) and not plus:
      print(len(hourmin[0]) != 2)
      print(plus)

      print(f'error: 24 hour format ({t})')
      return False

    try:
      h = int(hourmin[0])
      m = int(hourmin[1])
    except ValueError:
      print('error: time is non numerical')
      return False

    if h < 0 or h > 23:
      print(f'error: 24 hour format ({t})')
      return False
    if m < 0 or m > 59:
      print(f'error: 24 hour format ({t})')
      return False

    ret.append([h, m])

  # add operation deals with carries
  # if i was a better programmer i would have given up and used classes atp
  if plus:
    ret[1][0] += ret[0][0]
    ret[1][1] += ret[0][1]
    if ret[1][1] >= 60:
      ret[1][1] -= 60
      ret[1][0] += 1
    if ret[1][0] >= 24:
      ret [1][0] -= 24
  return ret

def addChange(d, day):
  # guides user through adding a new closed time to the schedule
  print(f"Type the times to close for {day} (24 hour)")
  print("Type ? for operations")
  try:
    stmt = input()
  except EOFError:
    return

  # handle operations
  remove = False
  if stmt == "?":
    printHelp()
    return addChange(d, day)
  if stmt[0] == '-':
    stmt = stmt[1:]
    remove = True
  out = parseStmt(stmt)
  if not out:
    print("Invalid input")
    while True:
      try:
        yn = input("Try again? [y/n] (y): ") or "y"
      except EOFError:
        return
      if yn == 'y' or yn == 'n':
        break
    if yn == 'y':
      return addChange(d, day)
    return 

  if remove:
    removeFromDay(d, day, out)
  else:
    addToDay(d, day, out)

def completeDay(s, day):
  if len(day) > 1:
    for key in s.keys():
      if day == key[0:len(day)]: # does it match the beginning
        day = key
  return day

def inputLoop(s):
  while True:
    printSchedule(s)
    try:
      i = input("What day would you like to change?\nType \"stop\" to save to file.\n")
      day = i.lower()
    except EOFError:
      return "err"
    print()
    if day == 'stop':
      break
    day = completeDay(s, day)
    if day not in s:
      print(f"{i} is not valid.\n")
      continue
    addChange(s, day)

