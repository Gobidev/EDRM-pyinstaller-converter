from tkinter import filedialog
import tkinter as tk

config_filepath = "files.yml"


def write_to_yaml(key, value):

    old_content = {}
    new_content = {}

    file = open(config_filepath, "r")
    content = file.readlines()
    lines = []

    # remove \n
    for i in content:
        i = i.replace("\n", "")
        lines.append(i)

    # convert content to dictionary
    for n in lines:
        content_list = n.split(": ")
        old_content[content_list[0]] = content_list[1]

    if key in old_content:
        new_content[key] = value
        del old_content[key]
    else:
        new_content[key] = value

    for f in old_content:
        new_content[f] = old_content[f]

    file.close()

    # actual writing
    new_file = open(config_filepath, "w")

    # creating new string
    final_string = ""
    for element in new_content:
        final_string += element
        final_string += ": "
        final_string += new_content[element]
        final_string += "\n"

    new_file.write(final_string)
    new_file.close()


def read_yaml(key):

    file_content = {}
    file = open(config_filepath, "r")
    content = file.readlines()
    lines = []

    # remove \n
    for i in content:
        i = i.replace("\n", "")
        lines.append(i)

    # convert content to dictionary
    for n in lines:
        content_list = n.split(": ")
        file_content[content_list[0]] = content_list[1]

    try:
        return file_content[key]
    except:
        return "key not found in config"


def run():

    files = []

    file_index = 0
    while 1:
        path = read_yaml("file" + str(file_index))
        print(path)
        if path == "key not found in config":
            break
        else:
            files.append(path)
        file_index += 1

    content = []

    for file in files:

        x = open(file, "r")
        content.append(x.read())

    delete = ["../views/", "../config/", "from utils.edsm import get_commander_system", "from views.mainview import *",
              "from views.inputview import *", "from config.config import *", "from utils.clipboard import *",
              "from utils.csv_reader import *", "from utils.edsm import is_known",
              "from views.inputview import start_input_window", "from main.EDRouteManager import loop_refresh",
              "import threading", "import time", "import os", "from urllib.request import urlopen", "import json",
              "import tkinter as tk", "from tkinter import messagebox", "from tkinter import filedialog"
              ]

    replace = {"file='../views/logo.gif'": "file='logo.gif'", "../config/config.yml": "config.yml",
               "default='../views/logo.gif'": "default='logo.gif'"
               }

    content_string = ""

    for i in content:
        content_string += (i + "\n")

    for element in delete:
        content_string = content_string.replace("        " + element + "\n", "")
        content_string = content_string.replace("    " + element + "\n", "")
        content_string = content_string.replace(element + "\n", "")

    for element in replace:
        content_string = content_string.replace(element, replace[element])

    imports = ["import threading", "import time", "import os", "from urllib.request import urlopen", "import json",
               "import tkinter as tk", "from tkinter import messagebox", "from tkinter import filedialog"]

    final_string = ""
    for n in imports:
        final_string += n + "\n"
    final_string += "\n\n"
    final_string += content_string

    output = open("output.py", "w")
    output.write(final_string)
    output.close()


def select_files(amount=7):
    root = tk.Tk()

    files = []

    for n in range(int(amount)):
        root.filename = filedialog.askopenfilename(
            initialdir="/", title="Select python file", filetypes=(("Python files", "*.py"), ("all files", "*.*"))
        )

        files.append(root.filename)
    for file in files:
        write_to_yaml("file" + str(files.index(file)), file)


# select_files()
run()
