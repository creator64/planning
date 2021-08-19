import os

#path = "bet/ap/huhu.py"

#if not os.path.exists(path):
#    os.makedirs(path)

#with open("bet/ap/a.py", "w"):pass

#path2= "jdjdkdkd/kidjdkdk/akxkxkdod.py"
#path2 = os.path.normpath(path2)
#list_path = path2.split(os.sep)
#print(list_path)

#print(os.path.join("", "vet", "shsjsjksj"))
#print(os.path.join("aap\\vet", "lol"))

def fix_path(path):
    # checks if path exists; if not it will create the path
    path = os.path.normpath(path).replace("\data.db", "") # fixing the path and removing file from path
    pathlist = path.split(os.sep) # get the list of dirs and subdirs
    current_path = ""
    for p in pathlist:
        new_path = os.path.join(current_path, p) # the path of the new directory
        if not os.path.exists(new_path): # check if directory exists
            os.mkdir(new_path) # creare dir if not
        current_path = new_path # update current path
    with open(os.path.join(current_path, "data.db"), "a"):pass # create the file data.db

fix_path("sn/kasjmsks/apenzijndik\data.db")
