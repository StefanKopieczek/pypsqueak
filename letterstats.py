import audiotools
from collections import Counter
from math import sqrt, log10

BANDS = [(40, 1000, 'LOW'),
         (1000, 4000, 'MEDIUM'),
         (4000, 20000, 'HIGH')]
DEBUG = False
START_WEIGHT = 2

def _dprint(text):
    global DEBUG
    if DEBUG: print text + '\n'

def get_best_match(samples,
                   sample_frequency,
                   training_stats,
                   rejection_threshold=None,  # Todo
                   k=8):
    fingerprint = analyse(samples, sample_frequency)

    # Get k nearest neighbours.
    best_matches = []
    for stat in training_stats:
        best_matches.append((stat['letter'], _get_distance(stat['analysis'], fingerprint)))
        best_matches.sort(key=lambda stat : stat[1])
        best_matches = best_matches[:k]
    for x in best_matches:
        print x[0], x[1]

    # Break ties by choosing closest neighbour.
    counter = Counter([match[0] for match in best_matches])
    counter = Counter()
    values = {}
    for match in best_matches:
        counter[match[0]] += 1
        if match[0] in values:
            values[match[0]].append(match[1])
        else:
            values[match[0]] = [match[1]]

    common_list = [(count[0], values[count[0]]) for count in counter.most_common()
                   if count[1] == counter.most_common(1)[0][1]]
    print common_list
    return common_list[0][0]

    indices = {letterdata[0]:(k - revidx - 1)
                            for revidx, letterdata in enumerate(best_matches[::-1])}
    most_frequent_with_indices = {indices[key[0]]:key[0]
                                               for key in counter.most_common()}
    return min(most_frequent_with_indices.iteritems())[1]

def analyse(samples, sample_frequency):
    """Produces a data vector describing the characteristics of this sample.
       The vector is composed of the length of the sample, followed by three
       equal-length sections containing the fingerprint of the first, middle,
       and last segments of the sample - see 'analyse_segment' for details."""
    n = len(samples)
    overall_energy = audiotools.get_energy(samples)

    analysis = []
    _dprint('Analysing sample with length %d and energy %d' % (n, overall_energy))
    for ii in xrange(3):
        _dprint('\tParsing segment ' + str(ii))
        analysis.extend(_analyse_segment(samples[int(ii * n / 3.0):int((ii + 1) * n / 3.0)],
                                         sample_frequency,
                                         overall_energy))

    return analysis

def load_stats_from_file(fname):
    f = open(fname, 'r')
    stats = []
    for line in f:
        data = line.strip().split()
        letter = data[0]
        analysis = [float(datum) for datum in data[1:]]
        stat = {'letter':letter, 'analysis':analysis}
        stats.append(stat)
    f.close()

    return stats

def save_stats_to_file(stats, fname):
    f = open(fname, 'w')
    _dprint("Saving to file.")
    for stat in stats:
        line = (stat['letter'] + ' ' +
                ' '.join([str(datum) for datum in stat['analysis']]) +
                '\n')
        f.write(line)
    _dprint("Saved.")
    f.close()

def load_samples_from_file(fname):
    samples = []
    with open(fname, 'r') as f:
        for line in f:
            data = line.strip().split()
            letter = data[0]
            letter_samples = [float(datum) for datum in data[1:]]
            sample = {'letter': letter, 'samples': letter_samples}
            samples.append(sample)

    return samples

def save_samples_to_file(stats, fname):
    with open(fname, 'a') as f:
        for stat in stats:
            line = (stat['letter'] + ' ' +
                    ' '.join([str(datum) for datum in stat['samples']]) +
                    '\n')
            f.write(line)

def _get_distance(v1, v2):
    """Calculate the Euclidean distance between two vectors."""
    if len(v1) != len(v2):
        raise ValueError("Cannot get distance between vectors of different " +
                         "dimensions: %d and %d!" % (len(v1), len(v2)))
    return sqrt(sum(((v1[idx] - v2[idx]) ** 2 for idx in xrange(len(v1)))))

def _get_weighted_distance(v1, v2):
    for x in [v1, v2]:
        for ii in range(1, 5):
            x[ii] = x[ii] * START_WEIGHT

    return _get_distance(v1, v2)

def _get_predominant_band(samples, sample_frequency):
    """Test function to make sure that we're detecting bands correctly.
       Slightly unfair, since not all bands are equal in size."""
    levels = [(audiotools.get_energy_in_range(samples,
                                              band[0],
                                              band[1],
                                              sample_frequency),
               band) for band in BANDS]
    return max(levels, key=lambda level:level[0])[1][2]


def _analyse_segment(samples, sample_frequency, overall_energy):
    analysis = []
    energy = audiotools.get_energy(samples)
    analysis.append(log10(energy) * 1.0 / log10(overall_energy))
    for band in BANDS:
        _dprint('\t\tAnalysing band ' + str(band))
        band_energy = audiotools.get_energy_in_range(samples,
                                                     band[0],
                                                     band[1],
                                                     sample_frequency)
        analysis.append(log10(band_energy) * 1.0 / log10(overall_energy))

    return analysis

