import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep

if __name__ == "__main__":
    fname = sys.argv[1]
    print fname
    training_samples = letterstats.load_samples_from_file(fname)
    stats = []
    for sample in training_samples:
        stats.append({
            'letter': sample['letter'],
            'analysis': letterstats.analyse(sample['samples'], RATE)
        })
    print stats

    def handle_peak(samples):
        global RATE
        global stats
        print "Processing input"
        best_match = letterstats.get_best_match(samples, RATE, stats)
        print "I think you said '%s'." % best_match

    listener = PeakListener(handle_peak)
    try:
        listener.start()

        while True:
            sleep(0.1)  # Horrendous hack - should expose a join.

    finally:
    	listener.stop()
