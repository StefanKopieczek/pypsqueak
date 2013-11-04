# I'm so sorry for writing this class. I was in a hurry and I didn't have time
# to refactor the PeakListener to block properly. So much state and threadbadness!

import letterstats
import sys
from peaklistener import PeakListener, RATE
from random import shuffle
from time import sleep

def save_and_quit(stats, fname):
    letterstats.save_stats_to_file(stats, fname)
    print "Quitting now."
    sys.exit()

if __name__ == "__main__":
    fname = sys.argv[1]
    training_set = list('abcdefghijklmnopqrstuvwxyz0123456789') * 1
    is_listening = True
    stats = []
    current_idx = 0
    shuffle(training_set)
    def handle_peak(samples):
        # Horrendous hack - should use a blocking Listener.
        global is_listening
        global stats
        global current_idx
        if is_listening and len(samples) > 0: # Unsure why this is rqd, but it is.
            print "Got letter data."
            is_listening = False
            stats.append({
                'letter'    : training_set[current_idx],
                'analysis'  : letterstats.analyse(samples, RATE)
            })
            print "Wrote stats."
            current_idx += 1
            if current_idx >= len(training_set):
                save_and_quit(stats, fname) 
            print "\nSay '%s'." % training_set[current_idx]
            is_listening = True
        
    print "Say '%s'." % training_set[0]
    listener = PeakListener(handle_peak)
    listener.start()

    while True:
        # Sit on listener thread.
        # Hack - better to expose a 'join'.
        sleep(0.1)
