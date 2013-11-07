import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep
import speech

if __name__ == "__main__":
    fname = sys.argv[1]
    stats = letterstats.load_stats_from_file(fname)

    def handle_peak(samples):
        global RATE
        global stats
        """
        http://www.renuncln.com/blog/2012/05/28/python-speech-recognition-and-tts-part-i-pyspeech/
        """
        spoken = speech.input("Processing input")
        print "I think you said '%s'." % spoken
        #print "Processing input"
        #best_match = letterstats.get_best_match(samples, RATE, stats) 
        #print "I think you said '%s'." % best_match 
    
    
    listener = PeakListener(handle_peak)
    listener.start()

    while True:
        sleep(0.1) # Horrendous hack - should expose a join.
