# https://bespokeblog.wordpress.com/2011/07/07/
# basic-data-plotting-with-matplotlib-part-2-lines-points-formatting/

@ok 
def lines(xlabel, ylabel, title, *lines):
  import matplotlib.pyplot as plt
  xs = [x for x in len(lines[0])]
  plt.xlabel(xlabel)
  plt.ylabel(xlabel)
  for line in lines:
    plt.plot(xs, sorted(line.all),
                 label = line.label)
  plt.title(title)
  plt.legend()
  plt.show()
