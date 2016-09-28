HOW TO USE MOODLE SCRAPER

1.  Place the get_files.py script inside of a folder where you want to store all files.
    For example, I place mine in a google drive folder named '4th Year'.

2.  Run in terminal/command prompt the way you would normally run a python script.

3.  When asked, enter number of modules you're doing and copy the entire module title 
    from moodle and paste it into terminal/command prompt.
    This will create a file called 'module_list.txt', dont delete this until you start
    the next semester.
    
4.  Sit back and watch it add all those files.


Run this file whenever you feel you dont have all the slides. It will look and see what
you've already got and download any files that you are missing.

Also depending on your python environment, you may have to pip install some packages.
The packages I use are: requests, lxml
