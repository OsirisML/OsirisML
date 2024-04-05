import sys
import pathlib

# Get file paths
paths = list(pathlib.Path(sys.argv[1]).rglob('*.pcap'))
for path in paths:
    # Build label
    tokens = str(path.stem).split('-')
    label = '{0}-{1}'.format(tokens[0],tokens[1])
    print ('{0},{1}'.format(path,label))
