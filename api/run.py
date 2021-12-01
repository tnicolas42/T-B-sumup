import sys

from app import application, RUNNING_PORT

if __name__ == "__main__":
    debug = False
    for arg in sys.argv[1:]:
        if arg in ("-d", "--debug"):
            debug = True
    # application.run(debug=debug)
    application.run(host='0.0.0.0', debug=debug, port=RUNNING_PORT)