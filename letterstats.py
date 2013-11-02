import audiotools

BANDS = [(40,   1000, 'LOW'),
         (1000, 4000, 'MEDIUM'),
         (4000, 20000, 'HIGH')]
         
def get_predominant_band(samples, sample_frequency):
    levels = [(audiotools.get_energy_in_range(samples, 
                                              band[0], 
                                              band[1], 
                                              sample_frequency), 
               band) for band in BANDS]
    return max(levels, key = lambda level:level[0])[1][2]


def analyse(samples, sample_frequency):
    """Produces a data vector describing the characteristics of this sample.
       The vector is composed of the length of the sample, followed by three
       equal-length sections containing the fingerprint of the first, middle,
       and last segments of the sample - see 'analyse_segment' for details."""
    n = len(samples)
    overall_energy = audiotools.get_energy(samples)

    analysis = [n]
    for ii in xrange(3):
        analysis.extend(analyse_segment(samples[ii:int(ii*n/3.0)],
                                        sample_frequency,
                                        overall_energy))

    return analysis

def analyse_segment(samples, sample_frequency, overall_energy):
    analysis = []
    energy = audiotools.get_energy(samples)
    analysis.append(energy * 1.0 / overall_energy)
    for band in bands:
        band_energy = audiotools.get_energy_in_range(samples, 
                                                     band[0], 
                                                     band[1], 
                                                     sample_frequency)
        analysis.append(band_energy * 1.0 / overall_energy)

    return analysis
