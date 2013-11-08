# I'm so sorry for writing this class. I was in a hurry and I didn't have time
# to refactor the PeakListener to block properly. So much state and threadbadness!

import letterstats
import sys
from peaklistener import PeakListener, RATE
from random import shuffle
from time import sleep

def save_and_quit(stats, fname):
    letterstats.save_samples_to_file(stats, fname)
    print "Quitting now."
    sys.exit()

if __name__ == "__main__":
    fname = sys.argv[1]
    training_set = list('abcdefghijklmnopqrstuvwxyz0123456789') * 3
    is_listening = True
    stats = []
    current_idx = 0
    def handle_peak(samples):
        # Horrendous hack - should use a blocking Listener.
        global is_listening
        global stats
        global current_idx
        if is_listening and len(samples) > 0:  # Unsure why this is rqd, but it is.
            print "Got letter data."
            is_listening = False
            redo_input = raw_input("Hit n to retry")
            redo = (len(redo_input) > 0 and redo_input[0] == 'n')
            if not redo:
                stats.append({
                    'letter'    : training_set[current_idx],
                    'samples'  : samples
                })
                print "Wrote stats."
                current_idx += 1
                if current_idx >= len(training_set):
                    save_and_quit(stats, fname)
            print "\nSay '%s' (%d/%d)." % (training_set[current_idx], current_idx, len(training_set))
            is_listening = True

    print "Say '%s'." % training_set[0]
    listener = PeakListener(handle_peak)
    try:
        listener.start()

        while True:
            # Sit on listener thread.
            # Hack - better to expose a 'join'.
            sleep(0.1)

    finally:
        listener.stop()
