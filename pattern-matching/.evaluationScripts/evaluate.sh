#! /bin/bash

# For Testing
INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
LAB_DIRECTORY="/home/labDirectory"


ptcd=$(pwd)

cd $INSTRUCTOR_SCRIPTS
# echo $ptcd

list_of_files="$(ls $LAB_DIRECTORY)"

list_of_modules="$(ls /app)"

cp -r $LAB_DIRECTORY/* autograder/

cd ./autograder/

cp -r /app/* .

chmod -R 777 $list_of_files

# node autograder.js
python3 autograder.py

rm -r $list_of_files

rm -r $list_of_modules

cd "$ptcd"
