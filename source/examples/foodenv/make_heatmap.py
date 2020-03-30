import matplotlib.pyplot as plt
import numpy
import os
import io
import argparse


def generate_heatmap(directory, filename):
    """ Simple script to generate heat map """
    w=25
    h=12
    plt.figure(figsize = (w/2.54,h/2.54), dpi=300)

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


    aspect = 'auto'

    cmap = 'RdYlGn'
    plt.imshow(a, cmap=cmap, interpolation='none', aspect=aspect)

    plt.colorbar(orientation='horizontal')

    plt.xlabel('Object ID')
    plt.ylabel('Time steps')

    plt.savefig('{}hm.png'.format(filename))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate heatmap.')
    parser.add_argument('directory', type=str, help='Directory ')
    parser.add_argument('filename', type=str, help='Filename prefix to process')

    args = parser.parse_args()
    generate_heatmap(args.directory, args.filename)
