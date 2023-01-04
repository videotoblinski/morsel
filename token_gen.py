from crypt import crypt
import sys
import time
sys.stderr.write("password> ")
pswd = input()
print(crypt(pswd, str(int(time.time()))))
