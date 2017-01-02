#! /usr/bin/env python
import sys
import numpy
import math
import gzip

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('counts_files', nargs='+')
    p.add_argument('-o', '--output')
    args = p.parse_args()

    counts_files = args.counts_files
    D = numpy.zeros([ len(counts_files), len(counts_files) ])
    numpy.set_printoptions(precision=3, suppress=True)

    counts_list = []
    for filename in counts_files:
        print('reading:', filename)
        if filename.endswith('.gz'):
            fp = gzip.open(filename)
        else:
            fp = open(filename)

        counts = fp.readlines()[1:]
        counts = [ int(x.split()[1]) for x in counts ]
        counts = numpy.array(counts)
        counts = counts / math.sqrt(numpy.dot(counts, counts))

        counts_list.append(counts)

    i = 0
    labeltext = []
    for i, C1 in enumerate(counts_list):
        for j, C2 in enumerate(counts_list):
            prod = numpy.dot(C1, C2)
            prod = min(1.0, prod)
            distance = 2*math.acos(prod) / math.pi
            D[i][j] = 1.0 - distance

        labeltext.append(counts_files[i])
        i += 1

    if args.output:
        labeloutname = args.output + '.labels.txt'
        print('saving labels to:', labeloutname, file=sys.stderr)
        with open(labeloutname, 'w') as fp:
            fp.write("\n".join(labeltext))

        print('saving distance matrix to:', args.output,
              file=sys.stderr)
        with open(args.output, 'wb') as fp:
            numpy.save(fp, D)


if __name__ == '__main__':
    main()
