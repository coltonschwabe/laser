import matplotlib.pyplot as plt
import numpy as np
import math

t_total = 0.0 # total time (seconds)
pw = 110.0*(10.0**-9) # pulse width
N_total = 0 # total number of events

# gets intervals
intervalsarr = []
with open("intervals.txt", "rt") as cont:
    for line in cont:
       N_total += 1
       i = pw + float(line[0:8])*10**(int(line[9:]))
       intervalsarr.append(i)
       t_total += i

print(N_total)
print(t_total)

b = []
fakeintervals = []
dt = 0.01
mu = float(N_total) / t_total

for i in range(0, 101):
    t = float(i) * 0.01
    b.append(t)

    num = N_total*(math.exp(-1*mu*t) - math.exp(-1*mu*(t + dt)))

    for j in range(0, round(num)): # adds expected number of intervals
        fakeintervals.append(t + dt/2)

#plt.hist(fakeintervals, bins=b)

#plt.xlabel('Interval Length (seconds)')
#plt.title('Theoretical distribution of interval time length')

# Creating subplots with multiple histograms
#fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
 
#countsM = axes[0].hist(intervalsarr, bins=b, color='blue', edgecolor='black')[0]
#axes[0].set_title('Measured Intervals')
 
#countsT = axes[1].hist(fakeintervals, bins=b, color='green', edgecolor='black')[0]
#axes[1].set_title('Theoretical Intervals')
 
# Adding labels and title
#for ax in axes:
#    ax.set_xlabel('Interval Length (seconds)')
 
# Adjusting layout for better spacing
#plt.tight_layout()

#display plot
plt.show()

#diff = []

#ind = 0
#while ind < 100:
#    d = countsM[ind] - countsT[ind]

#    if (d == 0): break
#    else:
#        diff.append(int(d.item()))

#    ind += 1

#print(diff)


