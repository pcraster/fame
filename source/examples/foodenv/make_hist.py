import matplotlib.pyplot as plt
import numpy
import os
import io
import math
import argparse


def generate_histogram(directory, filename, roundy):
    """ Simple script to generate histogram """
    w=25
    h=12

    ts = 200

    props = ''
    cols = 0
    for t in range(1, ts + 1):
      try:
        fname = os.path.join(directory, '{}{:03d}.csv'.format(filename, t))
        data = numpy.loadtxt(fname, delimiter=',')
        values = data[:,2]
        cols = values.shape[0]
        props += ','.join(map(str,values))
        props += '\n'
      except Exception as e:
        props += ',' * (cols-1)
        props += '\n'

    a = numpy.genfromtxt(io.StringIO(props), delimiter=',')

    y_max = 0
    m_bins = 50
    x_min = -1.0
    x_max = 1.0

    # First iteration to get y max
    plt.figure(figsize=(5,3), dpi=72)
    for row in range(0, a.shape[0]):
      n, bins, patches = plt.hist(a[row,:], m_bins, range=(x_min, x_max))
      y_max = max(y_max, max(n))

    y_max = roundy * math.ceil(y_max/roundy)
    plt.close()

    for row in range(0, a.shape[0]):
      plt.figure(figsize = (w/2.54,h/2.54), dpi=72)
      n, bins, patches = plt.hist(a[row,:], m_bins, range=(x_min, x_max), facecolor='g', alpha=0.5)
      plt.xlabel('Propensity')
      plt.ylabel('Occurrence')
      plt.title('Time step {:3d}'.format(row + 1))
      plt.text(0.98 * x_min, 0.95 * y_max, r'N={}'.format(a.shape[1]))
      plt.xlim(x_min, x_max)
      plt.ylim(0, y_max)

      fname = '{}{:03d}.png'.format(filename, row + 1)
      plt.savefig(fname)

      plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('directory', type=str, help='Directory ')
    parser.add_argument('filename', type=str, help='Filename prefix to process')
    parser.add_argument('--roundy', type=int, default=100, help='Round up to multiple of')

    args = parser.parse_args()
    generate_histogram(args.directory, args.filename, args.roundy)
