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
MIN_PEAK_DURATION = 0.500
DEBUG = True 

def _dprint(text):
    global DEBUG
    if DEBUG: print text + '\n'

def get_shorts_from_bytes(data):       
    """Converts a string of byte values into an array of (short) int values,
       assuming Little Endian format."""
    shorts = []    
    for idx in xrange(0, len(data), 2):
        shorts.append(struct.unpack('<h', data[idx] + data[idx+1])[0])    
    return shorts


class PeakListener(object):    
    """The PeakListener listens on the computer's default input device, and
       listens for any periods of audio that are louder than a certain
       threshold.
       When a peak has ended, it calls the peak_data_handler it was given when
       constructed, passing the sample data as a list of ints."""

    def __init__(self, peak_data_handler, low_pass=1100, high_pass=1400):        
        self._last_sample = [0] * 100
        # Are we currently in a peak?
        self._is_high = False 

        # Thread used by the mic listener.
        self._mic_thread = MicInputThread(lambda data: self._handle_input(data))

        # Stores audio from the current peak.
        self._buffer = []

        # Time since last peak, to prevent 'bouncing'.
        self._last_peak_time = 0

        # The callback function to which we pass peak audio.
        self._peak_data_handler = peak_data_handler

        # The value at which we consider a peak to have ended.
        # Will need tweaking for a given mic.
        self._low_pass = low_pass 

        # The value at which we consider a peak to have started.
        # Will need tweaking for a given mic.
        self._high_pass = high_pass 
        
    def start(self):
        """Start listening to input."""
        _dprint("Peak Listener starts.")
        self._mic_thread.start()
        
    def stop(self):
        """Stop listening to input, and clean up all state."""
        self._mic_thread.stop()
        self._buffer = []
        self._last_peak_time = 0
        _dprint("Peak Listener stopped.")
        
    def _handle_input(self, data):
        """Internal method to handle a new chunk of audio from the mic."""
        # Carry out all new processing in a new thread.
        # This stops us dragging the microphone thread, which should be kept 
        # free.        
        threading.Thread(target=self._handle_input_in_thread, 
                         args=(data,)).start()

    def _handle_input_in_thread(self, data):                              
        """Internal method to handle a new chunk of audio from the mic.
           Should be called in its own thread to not block the input thread."""
        samples = get_shorts_from_bytes(data)     
        energy = audiotools.get_energy(samples) 
        time_since_last_peak = time() - self._last_peak_time            
        if self._is_high:
            # We're in a peak, so record off the latest audio.
            self._buffer.extend(samples)
        if (energy < self._low_pass and 
            self._is_high and 
            time_since_last_peak > MIN_PEAK_DURATION):            
            # We're in a peak, but it's just ended. Handle the audio.
            _dprint("Peak ends.")
            self._is_high = False         
            self._peak_data_handler(self._buffer[:]) # Shallow copy
            if self._buffer[:100] == self._last_sample[:100]: print "CONSPIRACY!!!"
            self._last_sample = self._buffer[:100]
            self._buffer = []
        elif (energy > self._high_pass and not self._is_high):
            print energy
            # We weren't in a peak, but one just started. Begin recording.
            _dprint("Peak starts.")
            self._is_high = True
            last_peak_time = time()         
            self._buffer = []
                    
class MicInputThread(threading.Thread):
    """Thread used to listen to mic input, and pass on each sample to a given
       callback function."""

    def __init__(self, new_sample_callback=None):
        self._is_running = True
        self._new_sample_callback = new_sample_callback
        threading.Thread.__init__(self)
        
    def stop(self):
        """Terminate the listener thread."""
        self._is_running = False
        
    def run(self):        
        """Overrides Thread.run()."""
        global FORMAT   # Bitness/endianism of audio samples.
        global RATE     # Sample rate in samples/sec. 
        global CHANNELS # Num channels
        global CHUNK    # Samples to get in one go.
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
            # We've ended or crashed. Either way, tidy up. 
            stream.stop_stream()
            stream.close()
            p.terminate()

def handle_peak(samples):
    """Demo function to be called when we get a peak.
       Put something awesome here."""
    print "Got peak!" 
    
if __name__=="__main__":
    listener = PeakListener(handle_peak)
    listener.start()
