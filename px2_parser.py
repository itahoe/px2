import time, threading
import os
import sys
from configparser import ConfigParser
import string


###############################################################################
# PARSE
def parse_str( s ):
    print('0103' + s)

###############################################################################
# MAIN
def main( logfile ):
    with open( logfile, 'r' ) as f:
        for s in f.read().split('0103'):
            if len(s):
                parse_str( s )

###############################################################################
#
if __name__ == "__main__":
    name, _ = os.path.splitext(os.path.basename(__file__))

    if len( sys.argv ) < 2:
        print ("Usage: %s <csv_file>" % name )
        sys.exit()

    main( sys.argv[1] )
