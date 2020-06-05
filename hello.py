import sys

sys.stdout.write("##[debug] Hello from python!")
sys.stdout.write("##[debug]" + str(sys.argv[1:]))

print("##[2debug] Hello from python!")
print("##[2debug]" + str(sys.argv[1:]))