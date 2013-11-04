import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep

if __name__ == "__main__":
    fname = sys.argv[1]
    stats = letterstats.load_stats_from_file(fname)

    def handle_peak(samples):
        global RATE
        global stats
        print "Processing input"
        best_match = letterstats.get_best_match(samples, RATE, stats) 
        print "I think you said '%s'." % best_match 
    
    listener = PeakListener(handle_peak)
    listener.start()

    while True:
        sleep(0.1) # Horrendous hack - should expose a join.
