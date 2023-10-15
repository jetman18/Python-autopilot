
lat = []
lon = []
import matplotlib.pyplot as plt
f = open("data.txt",'r')
dd=f.read()
p = dd.split('\n')
print(len(p))

for i in range(len(p)):
    a,b = p[i].split('   ')
    lat.append(float(a))
    lon.append(float(b))

plt.axis('equal')
plt.plot(lat,lon)
plt.show()

