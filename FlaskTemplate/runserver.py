"""
This script runs the FlaskTemplate application using a development server.
"""

from os import environ
from FlaskTemplate import app


def testName() -> int:
    #print("hhh")
    pass


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 80
    PORT = 80
    app.run('0.0.0.0', PORT)
