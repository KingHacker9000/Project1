import sys
import subprocess
p = subprocess.getoutput("{} ./adventure.py < gameover.txt".format(sys.executable), encoding='utf-8')
print(p)