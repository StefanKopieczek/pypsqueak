import audiotools

BANDS = [(40,   1000, 'LOW'),
         (1000, 4000, 'MEDIUM'),
         (4000, 20000, 'HIGH')]
         
def get_predominant_band(samples, sample_frequency):
    levels = [(audiotools.get_energy_in_range(samples, band[0], band[1], sample_frequency), band) for band in BANDS]
    return max(levels, key = lambda level:level[0])[1][2]