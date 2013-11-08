import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep
import time
import speech
prev_phrase = ''

if __name__ == "__main__":
    # Handle a specific set of heard phrases with a callback.
    def response(phrase, listener):
        print("You said %s" % phrase)
        if phrase == 'turn off':
            #print prev_phrase
            listener.stoplistening()
        #prev_phrase = phrase    
        """
        http://www.renuncln.com/blog/2012/05/28/python-speech-recognition-and-tts-part-i-pyspeech/
        
        spoken = speech.input("Processing input", ['ABC', 'AWL', 'TJC2', 'turn off'])
        print "I think you said '%s'." % spoken
        if spoken == "turn off":
            listener.stoplistening()"""
        #print "Processing input"
        #best_match = letterstats.get_best_match(samples, RATE, stats)
        #print "I think you said '%s'." % best_match
    listener = speech.listenfor(
    ['AWL', 'TJC2', 'RG3', 'Killer', 'Sneezy', 'Bashful', 'Doc', 'turn off'],
    response)

    while listener.islistening():
        time.sleep(1)
