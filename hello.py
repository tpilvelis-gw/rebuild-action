import sys

sys.stdout.write("##[debug] Hello from python!")
sys.stdout.write("##[debug]" + str(sys.argv[1:]))