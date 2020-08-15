import shutil
import glob
import os.path

original_dir_glob = os.path.join("pyu-data","new","*")

zips = glob.glob(original_dir_glob)

for z in zips:
    try:
        shutil.unpack_archive(z, "dist")
    except ValueError:
        print("Can't unpack: ", z)