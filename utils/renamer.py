#!/usr/bin/env python
# this python script renamed directories based on the contents of the module.json file
# this was originally intended for czepeku scenes but can be used for any foundry module dir
import json
import glob
import os
import pathlib

def main():
    # each directory has a json file called module.json
    # open each json file and get the .name keys value
    # rename the directory to the name
    directory = pathlib.Path(os.getcwd())
    print(directory)
    for dir in os.listdir(directory):
        dir = pathlib.Path(dir)
        print(dir)
        if dir.is_dir():
            with open(f'{dir}/module.json', 'r') as f:
                data = json.load(f)
                #print(data)
                id = data.get('name') or data.get('id')
                print(f"Renaming {dir} to {id}")
                dir.rename(f"{id}")

if __name__ == "__main__":
    main()
