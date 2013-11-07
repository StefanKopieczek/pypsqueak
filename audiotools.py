from cmath import exp, pi

def get_energy(samples):
    return sum([abs(sample) for sample in samples]) * 1.0 / len(samples)

def get_energy_at_frequency(samples, frequency, sample_frequency):
    """Calculates the contribution of the given frequency to the overall energy
       of the sample. Takes the sample as a list of ints, the frequency whose
       contribution we wish to determine, and the frequency at which the given
       samples were taken (in Hz)."""
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
    # Horrendously hacky - fix!
    delta = int((high-low)*1.0/points)
    f0 = get_energy_at_frequency(samples, low, sample_frequency)
    odd_contribution = sum((get_energy_at_frequency(samples, f, sample_frequency) 
                              for f in xrange(low + delta, high - delta, delta)))
    even_contribution = sum((get_energy_at_frequency(samples, f, sample_frequency) 
                              for f in xrange(low + 2 * delta, high - delta, delta)))
    final_freq = int((high-low)* 1.0 / delta) * delta + low
    f2n = get_energy_at_frequency(samples, final_freq, sample_frequency)
    
    approximation = ((delta / 3.0) * 
                       (f0 + 4 * odd_contribution + 2 * even_contribution + f2n))
    return approximation

def sft(a, k):
    """Calculates the semidiscrete fourier transform of the array a at frequency
       k, relative to the length of a."""
    result = 0
    N = len(a)
    prec = 2 * pi * k * 1.0 *1j / N
    acc = -prec
    for n in xrange(N):
        acc += prec
        result += a[n] * exp(acc)
    return result / N
