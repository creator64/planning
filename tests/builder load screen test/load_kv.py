import os
from kivy.lang.builder import Builder

def load_kv(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".kv"):
                 Builder.load_file(os.path.join(root, file))
