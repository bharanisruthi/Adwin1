from AutoML3_sample_code_submission.Adwin2 import Adwin2
import random


adwin = Adwin2()
l = [0.6,0.8,0.7,0.5,0.4,0.1,0.9,0.7,0.1,0.3,0.3]
for i in range(0,500):
    j=random.uniform(0,1)
    l.append(j)
for j in range(0,500):
    l.append(random.uniform(1,100))

for i in range(0,999):
    print('iteration',l[i])
    print(adwin.insertInput(l[i]))