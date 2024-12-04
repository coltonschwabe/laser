import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit

t_total = 0.0 # total time (seconds)
pw = 110.0*(10.0**-9) # pulse width
N_total = 0 # total number of events

# gets intervals
intervalsarr = []
with open("daylongdata.txt", "rt") as cont:
    for line in cont:
       N_total += 1
       i = pw + float(line[0:8])*10**(int(line[9:]))
       intervalsarr.append(i)
       t_total += i

print(N_total)
print(t_total)

b = []
fakeintervals = []
#dt = 0.01
mu = float(N_total) / t_total

print(mu)

edges = np.linspace(2.0 * 10**-7, 10**-5, 50)
dt = edges[1:]-edges[:-1] # creates array of size of intervals
t = edges[:-1]
tc = (edges[1:]+edges[:-1])/2

H_model = N_total*(np.exp(-1*mu*t) - np.exp(-1*mu*(t + dt)))
#H_model = N_total*mu*np.exp(-1*mu*tc)*dt

data = []

for a in range(0, H_model.size):
    for j in range(0, round(H_model[a])): # adds expected number of intervals
        data.append(tc[a])

#for i in range(0, 51):
#    ti = float(i)*(1.96*(10.0**-7)) + 2.0 * (10.0**-7)
#    b.append(t)

#    num = N_total*(math.exp(-1*mu*ti) - math.exp(-1*mu*(t + dt)))

#    for j in range(0, round(num)): # adds expected number of intervals
#        fakeintervals.append(t + dt/2)

counts1 = np.histogram(data, bins=edges)[0]
counts2 = np.histogram(intervalsarr, bins=edges)[0]

diff = counts2 - counts1

def exponential_func(x, a, b):
    return a * np.exp(-b * x)

popt, pcov = curve_fit(exponential_func, tc, diff)
a, b = popt

print(b)
print(a)

#print(diff)
dat2 = []

for k in range(0, len(diff)):
    if diff[k] >= 0:
        for j in range(0, diff[k]):
            dat2.append(tc[k])

plt.hist(dat2, bins=edges)
plt.xlabel('Interval Length (seconds)')
plt.title('Difference in distribution of interval time length')

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


