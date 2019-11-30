"""
This script runs the FlaskTemplate application using a development server.
"""

from os import environ
from FlaskTemplate import app


def testName() -> int:
    #print("hhh")
    pass


if __name__ == '__main__':
    app.run('0.0.0.0', 4004)
