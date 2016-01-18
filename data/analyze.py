import matplotlib.pyplot as plt


def save(filename):
   plt.savefig("vis/"+filename, format='png')


def histogram(filename,data,title,xaxis):
   plt.clf();
   plt.hist(data);
   plt.title(title)
   plt.xlabel(xaxis)
   plt.ylabel("Number of Fics")  
   save(filename)

def scatter(filename, x, y,title, xlab, ylab):
   plt.clf();
   plt.scatter(x,y);
   plt.title(title)
   plt.xlabel(xlab)
   plt.ylabel(ylab)  
   save(filename)