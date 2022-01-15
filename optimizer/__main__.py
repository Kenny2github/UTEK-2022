import sys
from optimizer import run1, run2, run3, run4, run5

globals()['run' + sys.argv[1]]()