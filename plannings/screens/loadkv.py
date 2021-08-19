import os
from kivy.lang.builder import Builder

def LoadKv(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".kv"):
                 Builder.load_file(os.path.join(root, file))
                 print("loaded kv file: %s" %(os.path.join(root, file)))
