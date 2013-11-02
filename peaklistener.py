"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import struct
import wave
import threading
from time import sleep, time
import audiotools, letterstats

CHUNK = 1024 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
MIN_PEAK_DURATION = 0.500

def get_shorts_from_bytes(data):       
    shorts = []    
    for idx in xrange(0, len(data), 2):
        shorts.append(struct.unpack('<h', data[idx] + data[idx+1])[0])    
    return shorts

class PeakListener(object):    
    def __init__(self, peak_data_handler):        
        self._is_high = False                
        self._mic_thread = MicInputThread(lambda data: self._handle_input(data))
        self._buffer = []
        self._last_peak_time = 0
        self._peak_data_handler = peak_data_handler
        self._low_pass = 700
        self._high_pass = 1300
        
    def start(self):
        self._mic_thread.start()
        
    def stop(self):
        self._mic_thread.stop()
        self._buffer = []
        self._last_peak_time = 0
        
    def _handle_input(self, data):
        # Carry out all new processing in a new thread.
        # This stops us dragging the microphone thread, which should be kept 
        # free.        
        threading.Thread(target=self._handle_input_in_thread, args=(data,)).start()

    def _handle_input_in_thread(self, data):                              
        samples = get_shorts_from_bytes(data)     
        energy = sum([abs(sample) for sample in samples]) / len(samples)              
        time_since_last_peak = time() - self._last_peak_time            
        if self._is_high:
            self._buffer.extend(samples)
        if (energy < self._low_pass and 
            self._is_high and 
            time_since_last_peak > MIN_PEAK_DURATION):            
            self._is_high = False         
            self._peak_data_handler(self._buffer[:]) 
        elif (energy > self._high_pass and not self._is_high):
            self._is_high = True
            last_peak_time = time()         
            self._buffer = []
                    
class MicInputThread(threading.Thread):
    def __init__(self, new_sample_callback=None):
        self._is_running = True
        self._new_sample_callback = new_sample_callback
        threading.Thread.__init__(self)
        
    def stop(self):
        self._is_running = False
        
    def run(self):        
        global FORMAT
        global RATE
        global CHANNELS
        global CHUNK
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)                                
        print "MicInputThread begins listening."
        
        try:
            while self._is_running:
                data = []
                data.extend(stream.read(CHUNK))
                if self._new_sample_callback:                
                    self._new_sample_callback(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

def handle_peak(samples):
    print letterstats.get_predominant_band(samples[:], RATE)
    
 
if __name__=="__main__":
    listener = PeakListener(handle_peak)
    listener.start()
