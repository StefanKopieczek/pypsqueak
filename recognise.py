import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep
import time
import speech
prev_phrase = ''

if __name__ == "__main__":
    # Handle a specific set of heard phrases with a callback.
    
    def formdict(file_name):
        dict = {}
        list = []
        prefix = 'call '
        input_file = open(file_name, "r")
        for line in input_file.readlines():
            splint = line.split(", ")
            list.append(prefix+splint[0])
            list.append(prefix+splint[1])
            dict[prefix+splint[0]] = splint[2]
            dict[prefix+splint[1]] = splint[2]
        input_file.close()    
        return dict, list
    
    fname = sys.argv[1]
    dict, list = formdict(fname)
    list.append('call')
    
    def response(phrase, listener):
        print("You said %s" % phrase)
        listener.stoplistening()
        output_file = open('output.num', "w")
        output_file.write('+'+dict[phrase][1:])
        output_file.close()

    listener = speech.listenfor(list,response)
    while listener.islistening():
        time.sleep(1)

        
