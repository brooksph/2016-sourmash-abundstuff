#! /usr/bin/env python
import sourmash_lib
from sourmash_lib import signature as sig
import sys
import argparse

DEFAULT_K=31


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('signatures', nargs='+')
    parser.add_argument('-k', '--ksize', type=int, default=DEFAULT_K, help='k-mer size (default: %(default)s)')
    args = parser.parse_args()

    # load in the various signatures
    siglist = []
    for filename in args.signatures:
        print('loading', filename, file=sys.stderr)
        loaded = sig.load_signatures(filename, select_ksize=args.ksize)
        loaded = list(loaded)
        if not loaded:
            print('warning: no signatures loaded at given ksize from %s' %
                      filename, file=sys.stderr)
        siglist.extend(loaded)

    if len(siglist) == 0:
        print('no signatures!', file=sys.stderr)
        sys.exit(-1)

    vecs = {}
    all_mins = set()
    for ss in siglist:
        name = ss.name()
        mh = ss.estimator.mh

        mins = mh.get_mins(with_abundance=True)
        vecs[name] = mins
        all_mins.update(mins.keys())

    names = []
    for name, mins in vecs.items():
        line = []
        for mm in sorted(all_mins):
            line.append(str(mins.get(mm, 0)))

        print("\t".join(line))
        names.append(name)

    metadata_fp = open('list.txt', 'wt')
    print('name\thour', file=metadata_fp)
    for name in names:
        hour = name.split('_')[0]
        print("{}\t{}".format(name, hour), file=metadata_fp)
    metadata_fp.close()


if __name__ == '__main__':
    main()
