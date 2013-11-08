import letterstats
import sys
from peaklistener import RATE

if __name__ == '__main__':
    in_fname = sys.argv[1]
    out_fname = sys.argv[2]
    training_samples = letterstats.load_samples_from_file(in_fname)
    step = len(training_samples) / 20
    stats = []
    count = 0
    print 'Analysing data...'
    print '| ' * 20
    for sample in training_samples:
        count += 1
        if count % step == 0:
            print '|',
        stats.append({
            'letter': sample['letter'],
            'analysis': letterstats.analyse(sample['samples'], RATE)
        })
    print '\nAnalysis complete. Saving to %s' % out_fname
    letterstats.save_stats_to_file(stats, out_fname)
