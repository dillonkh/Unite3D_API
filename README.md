# Unite3d REST API

**Reach out to Brian if you need help with any of these steps**

## Environement Setup

1. Create a virtual environment with Python 3.7
    - **If the virtual environment is contained inside the project folder, be sure to gitignore it either globally on your computer or locally in this project's gitignore**
    - 3.7 recommended because of possible pip package compatibility issues with other versions of Python (IE 3.6, 3.8, or 3.9)
    - Most tools to create virtual environments have a flag to specify a path to the desired python executable. If your system globally uses 3.7, there isn't a need for this
    - To install other versions of Python, I recommend using pyenv. This can be installed with homebrew (`brew install pyenv`) and then you can install any version of Python you want. These installed versions won't automatically supercede your global system version of python, but you then can provide a path to their executable for specific virtual environments. See [https://realpython.com/intro-to-pyenv/](https://realpython.com/intro-to-pyenv/) for docs on how to do this.

2. Move into the project folder, and run: `pip install -r requirements.txt`
    - Be sure that the pip you are using the virtual environment one, not your system's global pip (Use `which pip` to determine). You shouldn't need to use `pip3`, typically upon creation of the virtual environment it links up both the `pip` and `pip3` commands to the same `pip3` executable
    - This installs all the necessary packages, reading from the committed `requirements.txt` file. When pulling down from main, watch to see if this file changes, and if so, just re-run `pip install -r requirements.txt` to install the new packages.


## Project Setup

1. Now that all the packages are installed, run `python manage.py migrate`. This command will run through all the migration files and apply them to your database. This creates, edits, and deletes tables depending on what the migration files specify. This is the middle man between you and the database, making it so you hopefully don't ever actually have to run direct SQL commands.
    - When pulling down from main, watch to see if any new files appear in any of the migrations folders, and if so, just re-run `python manage.py migrate`. You will also need to re-run that command if you ever delete your SQLite 3 database file (common/easy way to reset your DB).
    - Migration files are created based on the Model classes in the project. Changes to existing Model classes or creation of new Model classes will require you to run the following command: `python manage.py makemigrations -n <SHORT_DESCRIPTIVE_NAME>`. This will create a new migration file, and then is to be followed by the above `migrate` command to apply the new migration to the DB.

2. Register yourself as a superuser by running `python manage.py createsuperuser` in your terminal. Fill in the fields and remember your password. You can use this account to log into the Django Administration page (explained below) and populate, edit, or delete entries in the DB.

3. Run the server by running `python manage.py runserver` in your terminal. By default this will start the server on port 8000, and should print out the base url for you to copy and paste in your browser.
    - All endpoints have a browser GUI to access them, just visit the URL. I like to use Postman to test out endpoints, and you can also use any terminal tool (like `curl`) as well to test them out.

4. To access the Django Administration page, go to [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) while the server is running and log in using your superuser account. You can now view and manage the DB entries using Django's nice GUI.
