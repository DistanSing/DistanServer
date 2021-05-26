DistanSing Server Code - Ruben Arellano, University of Utah

In order to run the server take these steps in the terminal:

Make sure you have flask and bcrypt using:
pip3 install bcrypt
pip3 install flask

make sure the virtual environment is activated:
from "DistanServer/" run in the terminal:
source auth/bin/activate

setup flask from "DistanServer/":
export FLASK_APP=project
if you want debug mode*
export FLASK_DEBUG=1

run the project:
flask run