import time

def print_animation1():
     # Print animation in console
     print('loading...')
     for i in range(5):
          print("/", end="\r")
          time.sleep(0.1)
          print("\\", end="\r")
          time.sleep(0.1)

def print_animation2():
     # Print animation in console
     for i in range(1):
          print("---", end="\r")
          time.sleep(0.15)
          print("--_ ", end="\r")
          time.sleep(0.15)
          print("-__", end="\r")
          time.sleep(0.15)
          print("___", end="\r")
          time.sleep(0.15)
          print("__-", end="\r")
          time.sleep(0.15)
          print("_--", end="\r")
          time.sleep(0.15)
