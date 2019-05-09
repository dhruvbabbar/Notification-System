#flask modules
from flask import Flask 

import os

#initialize app
application = Flask(__name__)

#import configurations
application.config.from_pyfile('config.cfg')

application.secret_key=os.urandom(24)

#import all views
from emailController import*

import json



if __name__ == "__main__":
    
    
    application.debug = True
    application.run()