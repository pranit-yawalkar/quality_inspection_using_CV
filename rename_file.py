import os

path = "C:\\My Data\\Project\\code\\realtime\\custom_cascade\\p"

files = os.listdir(path)

for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, "".join([str(index), '.jpg'])))