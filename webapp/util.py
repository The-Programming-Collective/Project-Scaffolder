import random, string, os


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def getFrameworks():
   dirs = os.listdir(os.path.join(os.path.dirname(__file__), "engine", "templates"))
   
   all = {}
   
   for dir in dirs:
      if os.path.isdir(os.path.join(os.path.dirname(__file__), "engine", "templates", dir)):
         all[dir] = os.listdir(os.path.join(os.path.dirname(__file__), "engine", "templates", dir))
   
   return all