from cmath import exp, pi

def get_energy_at_frequency(samples, frequency, sample_frequency):
    # Calculate the length of the sample in seconds.
    sample_duration = len(samples) * 1.0 / sample_frequency

    # Calculate the frequency in terms of the duration of the sample, 
    # rather than in terms of seconds.
    adjusted_frequency = frequency * sample_duration

    energy = abs(sft(samples, adjusted_frequency)) 
    return energy
    
def get_energy_in_range(samples, low, high, sample_frequency, points=10):
    """ Use Simpson's rule to approximate the integral of the fourier transform
        over the given range."""
    # Hacky - fix!
    delta = int((high-low)*1.0/points)
    f0 = get_energy_at_frequency(samples, low, sample_frequency)
    odd_contribution = sum((get_energy_at_frequency(samples, f, sample_frequency) for f in xrange(low + delta, high - delta, delta)))
    even_contribution = sum((get_energy_at_frequency(samples, f, sample_frequency) for f in xrange(low + 2 * delta, high - delta, delta)))
    final_freq = int((high-low)* 1.0 / delta) * delta + low
    f2n = get_energy_at_frequency(samples, final_freq, sample_frequency)
    
    approximation = (delta / 3.0) * (f0 + 4 * odd_contribution + 2 * even_contribution + f2n)    
    return approximation

def sft(a, k):
    result = 0
    N = len(a)
    for n in xrange(N):        
        try:
            result += a[n] * exp(2 * pi * 1j * k * n * 1.0 / N)
        except IndexError:
            print "%d/%d/%d" % (n, N, len(a))

    return (1.0 / N) * result 
