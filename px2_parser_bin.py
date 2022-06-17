import time, threading
import os
import sys
from configparser import ConfigParser
import string


###############################################################################
# PARSE STR
def parse_str( s ):
    print('01 03 ' + s)

###############################################################################
# MAIN
def main( logfile ):
    with open( logfile, 'rb' ) as f:
        for s in f.read():
            print( format(s,'02X'), end='' )

###############################################################################
#
if __name__ == "__main__":
    name, _ = os.path.splitext(os.path.basename(__file__))

    if len( sys.argv ) < 2:
        print ("Usage: %s <csv_file>" % name )
        sys.exit()

    main( sys.argv[1] )

