import sys

from app import application

if __name__ == "__main__":
    debug = False
    for arg in sys.argv[1:]:
        if arg in ("-d", "--debug"):
            debug = True
    application.run(debug=debug)