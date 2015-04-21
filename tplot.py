
import matplotlib.pyplot as plt
x=[1,2,3,4,5]
y=[10,21,32,44,55]

fig = plt.figure()
axes = fig.add_subplot(1,1,1)
axes.plot(x, y, marker='o')
fig.savefig('tplot.png')

