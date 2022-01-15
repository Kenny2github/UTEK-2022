import sys
from optimizer import run1, run2, run3, run4, run5

if len(sys.argv) > 2:
    sys.stdin = open(sys.argv[2])
if len(sys.argv) > 3:
    sys.stdout = open(sys.argv[3], 'w')

globals()['run' + sys.argv[1]]()