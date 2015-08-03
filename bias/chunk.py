#from __future__ import division

"""

#<<
###################################################

CHUNK: near-linear time recursive clustering.
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the following conditions are met:

1. Redistributions of source code must retain the
above copyright notice, this list of conditions and
the following disclaimer.

2. Redistributions in binary form must reproduce the
above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the
names of its contributors may be used to endorse or
promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###################################################
#>>


## License

CHUNK is released under the BSD 3-clause license
that allows proprietary use and allows the software
released under the license to be incorporated into
proprietary products. Works based on CHUNK may be
released under a proprietary license as closed
source software.

## Installing CHUNK

Download _chunk.py_ from  http://unbox.org/open/tags/sharing/chunk/1.0/chunk.py

## Testing Your Installation

Test the code using

    python chunk.py

That call will automatically run a function 
that recursively clusters _nasa93_.
That data from 93 NASA software projects
from the years 1971 to 1987:

    def nasa93():
      return [
        [1980,4,2,4,6,6,2,4,4,4,4,3,4,4,4,3,7.5,72]
      ,[1980,3,2,4,3,3,2,2,4,5,5,3,4,3,3,3,20,72]
      ,[1984,3,2,4,3,3,2,2,4,5,4,3,4,3,3,3,6,24]
      ,[1980,3,2,4,3,3,2,2,4,5,5,3,4,3,3,3,100,360]
      ,[1985,3,2,4,3,3,2,2,4,5,3,3,2,3,3,3,11.3,36]
      ,[1980,3,2,4,3,3,4,2,4,4,4,2,1,3,3,3,100,215]
      # lines deleted from view
      ]

In this data, each row is one project and the first
column is the year of the project.  Also, the second
last column is the known size of the project
(measured in thousands of lines of code).  Finally,
the last column is the known effort for that project
(respectively).
As to the other columns, these are the standard
variables from the COCOMO model such as _rely_
(required reliability), _data_ (database size),
_cplx_ (product complexity) and many others
(e.g. _virt, turn, acap, aexp,
pcap,vexp,vecp,modp,too,sced_).  

"""

#<<


def nasa93():
  """year,rely,data,cplx,time,stor,virt,turn,acap,
  aexp, pcap,vexp,vecp,modp,too,sced,kloc,effort"""
  return [
   [1980,4,2,4,6,6,2,4,4,4,4,3,4,4,4,3,7.5,72]
  ,[1980,3,2,4,3,3,2,2,4,5,5,3,4,3,3,3,20,72]
  ,[1984,3,2,4,3,3,2,2,4,5,4,3,4,3,3,3,6,24]
  ,[1980,3,2,4,3,3,2,2,4,5,5,3,4,3,3,3,100,360]
  ,[1985,3,2,4,3,3,2,2,4,5,3,3,2,3,3,3,11.3,36]
  ,[1980,3,2,4,3,3,4,2,4,4,4,2,1,3,3,3,100,215]
  ,[1983,3,2,4,3,3,2,2,4,5,4,3,4,3,3,3,20,48]
  ,[1982,3,2,4,3,3,2,2,4,3,3,3,1,3,3,3,100,360]
  ,[1980,3,2,4,3,6,2,2,4,5,5,3,4,3,3,3,150, 324]
  ,[1984,3,2,4,3,3,2,2,4,4,4,3,4,3,3,3,31.5,60]
  ,[1983,3,2,4,3,3,2,2,4,5,4,3,4,3,3,3,15,  48]
  ,[1984,3,2,4,3,6,2,2,4,4,3,3,4,3,3,3,32.5,60]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,25.9,117.6]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,24.6,117.6]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,7.7,31.2]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,8.2,36]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,9.7,25.2]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,2.2,8.4]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,3.5,10.8]
  ,[1982,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,66.6,352.8]
  ,[1985,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,19.7,60]
  ,[1985,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,66.6,300]
  ,[1985,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,29.5,120]
  ,[1986,4,3,3,4,3,3,3,3,4,4,3,3,3,3,3,15,90]
  ,[1986,4,3,4,3,3,3,3,3,4,4,3,3,3,3,3,38,210]
  ,[1986,3,3,3,3,3,3,3,3,4,4,3,3,3,3,3,10,48]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,15.4,70]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,48.5,239]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,16.3,82]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,12.8,62]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,32.6,170]
  ,[1982,3,5,4,5,5,2,4,5,4,3,2,4,5,5,2,35.5,192]
  ,[1985,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,5.5,18]
  ,[1987,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,10.4,50]
  ,[1987,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,14,60]
  ,[1986,4,3,4,3,3,3,3,3,3,3,3,3,3,3,3,6.5,42]
  ,[1986,3,3,4,3,3,3,3,3,3,3,3,3,3,3,3,13,60]
  ,[1986,3,3,4,3,3,3,3,3,3,4,3,4,4,4,3,90,444]
  ,[1986,3,3,4,3,3,3,3,3,3,3,3,3,3,3,3,8,42]
  ,[1986,3,3,4,4,3,3,3,3,3,3,3,3,3,3,3,16,114]
  ,[1980,3,4,4,5,4,2,4,4,3,4,2,4,4,3,2,177.9,1248]
  ,[1979,5,4,4,5,5,3,3,5,5,5,3,4,4,4,2,227,1181]
  ,[1977,3,4,5,3,3,2,3,4,3,5,2,3,4,3,2,70,278]
  ,[1979,4,2,4,3,3,2,2,3,3,3,3,4,4,3,2,0.9,8.4]
  ,[1980,4,5,5,6,6,4,4,3,3,3,2,2,3,3,4,32,1350]
  ,[1980,4,4,4,5,6,4,4,4,4,4,4,4,4,3,3,53,480]
  ,[1983,4,3,5,5,5,4,4,3,3,3,2,2,3,3,4,16.3,480]
  ,[1983,4,3,5,5,5,4,4,3,3,3,2,2,3,3,4,6.2,12]
  ,[1983,4,3,5,5,5,4,4,3,3,3,2,2,3,3,4,3,38]
  ,[1977,4,2,5,5,6,2,3,5,5,5,1,1,4,4,3,41,599]
  ,[1977,4,2,5,5,6,2,3,5,5,5,1,1,4,4,3,24,430]
  ,[1982,3,4,2,3,3,4,3,4,4,3,3,3,4,4,3,282.1,1368]
  ,[1982,4,4,2,3,3,3,4,4,4,3,3,3,4,3,3,284.7,973]
  ,[1982,4,4,3,3,3,2,2,3,4,4,3,4,3,3,3,79,400]
  ,[1977,2,3,3,3,3,2,2,4,4,5,3,4,2,2,4,423,2400]
  ,[1977,3,3,3,3,3,2,3,4,5,5,2,4,4,3,3,190,420]
  ,[1984,3,3,4,3,4,3,3,4,4,3,3,4,4,3,4,47.5,252]
  ,[1980,5,3,6,4,4,2,2,3,4,3,3,3,2,4,3,21,107]
  ,[1983,3,4,4,5,3,3,4,4,4,4,3,4,2,2,4,78,571.4]
  ,[1984,3,4,4,5,3,3,4,4,4,4,3,4,2,2,4,11.4,98.8]
  ,[1985,3,4,4,5,3,3,4,4,4,4,3,4,2,2,4,19.3,155]
  ,[1979,4,3,5,4,4,2,4,4,3,3,4,4,2,5,4,101,750]
  ,[1979,4,3,4,4,4,2,4,3,4,3,3,3,2,5,3,219,2120]
  ,[1979,4,3,4,4,4,2,4,3,4,3,3,3,2,5,3,50,370]
  ,[1976,4,3,6,4,4,2,2,4,3,3,4,4,4,4,3,70,458]
  ,[1979,4,3,6,4,4,2,2,4,3,3,4,4,4,4,3,271,2460]
  ,[1971,3,3,3,3,3,2,2,4,4,4,3,4,3,2,3,90,162]
  ,[1980,3,3,3,3,3,2,2,4,4,4,3,4,3,2,3,40,150]
  ,[1979,4,3,4,4,3,2,2,4,4,4,3,4,3,3,3,137,636]
  ,[1977,4,3,4,4,3,4,2,4,4,4,3,4,3,1,3,150,882]
  ,[1976,5,3,4,4,3,2,2,4,4,4,3,4,3,3,3,339,444]
  ,[1983,2,4,2,3,3,4,2,4,4,4,3,4,3,2,3,240,192]
  ,[1978,4,3,4,3,5,2,3,4,4,4,4,4,2,2,2,144,576]
  ,[1979,3,2,3,3,5,2,3,4,4,4,4,4,2,2,2,151,432]
  ,[1979,3,2,4,3,5,2,3,4,4,4,4,4,2,2,2,34,72]
  ,[1979,3,3,4,3,5,2,3,4,4,4,4,4,2,2,2,98,300]
  ,[1979,3,3,4,3,5,2,3,4,4,4,4,4,2,2,2,85,300]
  ,[1982,3,2,3,3,5,2,3,4,4,4,4,4,2,2,2,20,240]
  ,[1978,3,2,3,3,5,2,3,4,4,4,4,4,2,2,2,111,600]
  ,[1978,4,5,4,3,5,2,3,4,4,4,4,4,2,2,2,162,756]
  ,[1978,4,4,5,3,5,2,3,4,4,4,4,4,2,2,2,352,1200]
  ,[1979,4,3,5,3,5,2,3,4,4,4,4,4,2,2,2,165,97]
  ,[1984,4,3,5,4,4,2,5,4,3,3,4,4,4,5,4,60,409]
  ,[1984,4,3,5,4,4,2,5,4,3,3,4,4,4,5,4,100,703]
  ,[1977,5,4,5,6,6,3,3,4,4,4,4,4,4,3,4,165,4178.2]
  ,[1977,5,4,5,6,6,3,3,4,4,4,4,4,4,3,4,65,1772.5]
  ,[1977,5,4,5,6,6,3,2,4,4,4,4,4,4,3,4,70,1645.9]
  ,[1977,5,4,6,6,6,3,3,4,4,4,4,4,4,3,4,50,1924.5]
  ,[1982,5,2,5,5,6,2,2,4,2,3,1,2,2,4,4,7.25,648]
  ,[1980,5,4,5,6,6,3,3,4,4,4,4,4,4,3,4,233,8211]
  ,[1975,4,2,4,3,3,2,2,3,3,4,3,3,4,1,3,302,2400]
  ,[1974,5,2,6,6,5,2,2,4,5,4,1,4,1,1,4,980,4560]
  ,[1975,3,2,4,3,3,2,2,5,3,5,4,4,3,2,3,350,720]
  ]
#>>

"""

When _chunk.py_ is loaded into Python, it prints the following tree.
Note that the 93 projects
in _nasa93_ where first sub-divided into two groups of 47 items.
This division repeated to find 16 leaf clusters of size five of six.

        93
        ...                 # <== [some lines omitted]
        |.. 47
        |.. |.. 23
        |.. |.. |.. 11
        |.. |.. |.. |.. 5.
        |.. |.. |.. |.. 6.  #<=== clusterX
        |.. |.. |.. 12
        |.. |.. |.. |.. 6.
        |.. |.. |.. |.. 6.
        |.. |.. 24
        |.. |.. |.. 12
        |.. |.. |.. |.. 6.
        |.. |.. |.. |.. 6.
        |.. |.. |.. 12
        |.. |.. |.. |.. 6.
        |.. |.. |.. |.. 6.  #<=== clusterY

Just to show that the clustering works, we note that some of these
clusters are very uniform. For example, _clusterY_ contains six
projects, all from 1979, and all with mostly
repeated values. In the following, the columns marked
_rdctsvTaApvlmTS_, these  hold values for
_rely,data,cplx,time, stor,virt,turn,acap,aexp,
 pcap,vexp,lexp,modp, tool,sced_ (respectively). Also,
if a value is the same as the one above, this is shown with a
 "ditto" mark, _"."_.

                    year rdctsvTaApvlmTS ksloc effort
                    ==== =============== ===== =====
        project 88: 1979 424332233334432 9.7 = 25.2
        project 89:    . ............... 8.2 =   36
        project 90:    . ............... 7.7 = 31.2
        project 91:    . ............... 3.5 = 10.8
        project 92:    . ............... 2.2 =  8.4
        project 93:    . ............... 0.9 =  8.4

Other clusters are more diverse. For example, _clusterX_
contains data from nearly ten years of software development.
As might be expected,  those projects are not all similar so
there
are fewer ditto marks:

                    year rdctsvTaApvlmTS  ksloc  effort
                    ==== ===============  =====  =====
        project 52: 1977 345332343523432    70 =  278
        project 53: 1979 5.4553.55.34.4.   227 = 1181
        project 54:    . 43.4424343.3253    50 =  370
        project 55: 1980 34.5...43424432 177.9 = 1248
        project 56: 1984 .2.36.2.433.3.3  32.5 =   60
        project 57: 1986 .3.433333..3...    16 =  114

## Applying CHUNK to Other Models

CHUNK recursively divides data in the format of
the _nasa93()_ function show above.
So, to apply CHUNK to different data, write
another function like _nasa93_.

Also, CHUNK needs to know some meta-knowledge about the data.
For example, column of data,
CHUNK needs to knows the low and high value:

"""


def lohi(m,x):
  if m == nasa93:
    if   x==16: return 0,1000    # range of KLOC
    elif x==0 : return 1971,1987 # years
    else      : return 1,6 # 1..6 = vlow,low,nom,
                           #        hi,vhi,xhi
  else:
    raise Exception('[%s] unknown' % m.__name__)

"""

Sometimes, there is knowledge that some variables
are more important than others. In the case of
_nasa93_, we have no such knowledge so everything
has the same weight.

"""
def weight(m,x):
  if m == nasa93:
    return 1
  else:
    raise Exception('[%s] unknown' % m.__name__)

"""

CHUNK groups together projects with similar
decisions.  To do that, CHUNK isolates those
decisions (which it calls _dec_) from the objectives
(which it calls _obj_).

"""

def project2Slots(project = nasa93()):
  "Returns 'Slots'- a struct with named fields."
  return [Slots( nums = [],
                 syms = [col[1]]+col[3:7],
                 obj = [col[-1]
         ]) for col in project]

"""


In summary, to apply CHUNK to other data,
write a new model function (like _nasa93_) then
modify _lohi_ and _weight_ to add in the meta-knowledge.
Optionally, you may also need to modify _project2Slots_ to convert your
model's data format into the  _Slots_ needed by CHUNK.




# Inside CHUNK

## Roadmap to Functions.

As shown below, _chunk_ is the main function that
recurively divides the data.
In that division, the _dist_ function reports the
distance between data items (and that function is
helped by _normalize_ and _squaredDifferences_).

To divide the data, we use _fastdiv_ which in turn
uses _twoDistantPoints_ to separate the data.  Note
that the main _chunk_ function recurses on the
divisions generated by _fastdiv_.  That recursion is
controlled by the parameters initialized in
_settings_.

After that, this code is all low-level Python tricks
such as _align_, which pretty prints columns of
data.  Two other important tricks are the _leafs_
iterator (that walks over the tree of clusters found
by _chunk_) and _Slots_ which is a generic Python
struct that supports reading and writing to names
fields.

Finally, the function _\_nasa93_ shows an example of
how to chunk the _nasa93_ data, shown above.

All these functions are detailed, below.

## Distance Calculations

CHUNK finds groups of similar things.  But what does
"similar" mean?

To answer that questions, CHUNK uses the following
_dist_ function. This function excepts two examples
_i,j_ from some model _m_. It then decides _how_ to
compare them (the default is to use decisions _dec_
collected together by _project2Slots_ - see above).
Next, _dist_ sums the squares of the differences
between each part of the example. Finally, _dist_
returns the square root of that sum, normalized to
the range zero to one.


"""

def dist(m,i,j):
  "Euclidean distance 0 <= d <= 1 between decisions"
  deltas, n = 0, 0
  d1,d2 = i.nums, j.nums
  for d,x in enumerate(d1):
    y  = d2[d]
    v1 = normalize(m, d, x)
    v2 = normalize(m, d, y)
    w  = 1
    deltas,n = squaredDifference(m,v1,v2,w,deltas,n)
  d1,d2 = i.syms,j.syms
  for d,x in enumerate(d1):
    y = d2[d]
    w = 1
    n += 1
    deltas += (0 if x == y else 1)
  return deltas**0.5 / (n+0.0001)**0.5

"""

(Aside: the last line adds in 0.0001 to avoid any
divide-by-zero errors.)

### Normalize

When computing distances, it is standard practice to
_normalize_ all numeric values to the range zero to one,
min to max.  To do that, CHUNK uses the _lohi_
function described above.

"""

def normalize(m,x,value) :
  if not The.normalize     : return value
  if value == The.missing  : return value
  if isinstance(value,str) : return value
  lo, hi = lohi(m,x)
  return (value - lo) / (hi - lo + 0.0001)
"""
As seen above, _normalize_ has some special cases.
Firstly, if some global flag has disabled
normalization, we just return the unaltered value.
Similarly, if we are trying to normalize some
missing value or some non-numeric value, we also
return the unaltered value.

### SquaredDifference

The _dist_ function needs to compute the square of
the differences between two values _v1,v2_ from some
model _m_.  It is assumed that each value is
weighted; i.e.  it can add up to some amount _most_
to the distance measure.  This is done using the
_squaredDifference_ function- which uses some
distance heuristic first proposed by David Aha
\cite{aha91}.  For example, if in doubt, assume the
maximum distance. Such doubts arise if (e.g.) we are
comparing missing values.

"""
def squaredDifference(m,v1,v2,most,sum=0,n=0):
  def furthestFromV1() : 
    return  0 if v1 > 0.5 else 1
  if not v1 == v2 == The.missing: 
    if v1 == The.missing: 
      v1,v2 = v2,v1 # at the very least, v1 is known
    if isinstance(v1,str) and isinstance(v2,str):
      if v2 == The.missing or v1 != v2 : 
        inc = 1
    else:
      if v2 == The.missing: v2 = furthestFromV1()  
      inc = (v1 - v2)**2
  return (sum + most*inc, # sum of incs, so far 
          n   + most) # sum of max incs, so far
"""
Note that the _squaredDifference_ function knows how
to handle numerics as well as non-numerics
differently to numerics. Two non-numerics have zero
distance if they are the same (and distance equal to
max, otherwise).

## Dividing the Data

### FastDiv

With the above machinery, we can very quickly
recursively divide some training data in half using
_fastdiv_. This function finds the distance _c_
between two distance items _west,east_. All data has
some distance _a,b_ to _west,east_.  Using _a,b,c_,
the _fastdiv_ function uses the cosine rule to sort
the data along where it falls on a line running from
_west_ to _east_.  This function then returns the
data, divided on the median value.

"""

def fastdiv(m,data,details, how):
  "Divide data at median of two distant items."
  west, east = twoDistantPoints(m,data,how)
  c    = dist(m, west, east)
  for i in data:
    a   = dist(m,i, west)
    b   = dist(m,i, east)
    i.x = (a*a + c*c - b*b)/(2*c) # cosine rule
  data = sorted(data,key=lambda i: i.x)
  n    = len(data)/2
  details.also(west=west, east=east, c=c, cut=data[n].x)
  return data[:n], data[n:]

"""

### TwoDistantPoints

CHUNK is fast since it uses the linear-time
"FastMap" heuristic \cite{fal95} to find the
_twoDistantPoints_.  This heuristic starts by
picking any item at random. Next, it finds the
furthest item from the first pick. Finally, it finds
the furthest item from the second item. Note that
this is fast since this
requires only one scans of the data for each pick.
While the two found items may not be the most
distant points, they are far enough away to guide
data division.


"""

def twoDistantPoints(m,data,how):
  def furthest(i):
    out,d= i,0
    for j in data:
      tmp = dist(m,i,j)
      if tmp > d: out,d = j,tmp
    return out
  one  = any(data)      # 1) pick any thing
  west = furthest(one)  # 2) far from thing
  east = furthest(west) # 3) far from west
  return west,east

"""

While _twoDistantPoints_ looks
simple, it actually offers a profound summation of
important aspects of a data set. According to John
Platt, this FastMap heuristic belongs to a class of
algorithms that find approximations to the
eigenvectors of a data set \cite{platt05}.  Spectral
learners \cite{kamvar03} use these eigenvectors to
reason along the most important dimensions in a data
set.

### Settings

By applying _fastdiv_ recursively, we can build a
binary tree whose leaves contain similar
examples. That tree generation is controlled by the
following _settings_. By default, we will stop when
any leaf has less than _minSize=10_ or if we have
recursed more that _depthMax=10_ items.  Also, just
to make sure we get at least a few branches in the
tree, we will recurse at least _minSize=2_ times.
Further, when we recurse, if _verbose=True_, we will
trace the traversely by printing one _b4_ string for
each level of the recursion. Finally, when computing
distances, this code uses _how=x.dec_; i.e. the
decisions of each item in the data.

"""

def settings(**has):
  "Return control settings for recursive descent."
  return Slots(minSize  = 10,    # min leaf size
               depthMin= 2,      # no pruning till depthMin
               depthMax= 10,     # max tree depth
               b4      = '|.. ', # indent string
               verbose = False,  # show trace info?
               how= lambda x:x.dec # how to measure distance
   ).override(has)

"""

### Chunk (main function)

Finally, we arrive at the main _chunk_ function.
This function uses the above _settings_ to build a
tree that recursively divides the data.  The _chunk_
function holds those _settings_ in its _slots_
variable (which is set on the first line of the
function, if it is not already known).  Local
functions within _chunk_ use these _slots_ to
control how the tree is built.

"""

def chunk(m,data,slots=None, lvl=0,up=None):
  "Return a tree of split data."
  slots = slots or settings()
  def tooFew() :
    return len(data) < slots.minSize
  def tooDeep():
    return lvl > slots.depthMax
  def show(suffix):
    if slots.verbose:
      print slots.b4*lvl + str(len(data)) + suffix
  tree= Slots(_up=up,value=None,_left=None,_right=None)
  if tooDeep() or tooFew():
    num = Nums()
    for row in data: num += row.obj[0]
    show(".  " + str(num.has()))
    tree.value = data
  else:
    show("")
    wests,easts = fastdiv(m, data, tree, slots.how)
    if not worse(wests, easts, tree) :
      tree._left  = chunk(m, wests, slots, lvl+1, tree)
    if not worse(easts, wests, tree) :
      tree._right = chunk(m, easts, slots, lvl+1, tree)
  return tree

def worse(down1,down2,here): return False

"""

Note some subtleties in the above code. Firstly,
since we use _fastdiv_, our _chunk_ function is a
very fast method to divide data.

Secondly, the function _worse_ is a hook for any
clever pruning you might want to add to this process
(this _chunk_ function only recurses on subtrees
that are not _worse_).  While we do not use _worse_
here, this function could be used to prune sub-trees
that fail some test; e.g.  that do not reduce the
variance of the current tree.

Thirdly, _chunk_ returns a tree of _Slots_ where
each node contains pointers to its _\_left_ and
_\_right_ kids as well as a pointer _\_up_ to the
parent node (which, for the root node, points to
_None_). Note that all leaves of this tree have
empty child pointers.  Such childless leaves hold
the items that fall into that leaf in the _value_
field.


## Support Utilities



### Some Standard Tricks

"""

import sys,math,random
sys.dont_write_bytecode = True # disable writing .pyc files
seed = random.seed     # convenient shorthand
any  = random.choice   # another convenient shorthand

def say(x):
  "Output a string, no trailing new line."
  sys.stdout.write(x)

def showd(d):
  """Catch key values to string, sorted on keys.
     Ignore hard to read items (marked with '_')."""
  return ' '.join([':%s %s' % (k,v)
                   for k,v in
                   sorted(d.items())
                   if not "_" in k])
"""

_Slots_ is based on a Peter Norvig trick from
http://norvig.com/python-iaq.html. When all you want
to do is create an object that holds data in several
fields, the following will do. For an example of
using _Slots_, see _settings_ (above).

"""

class Slots():
  "Place to read/write named slots."
  id = -1
  def __init__(i,**d) :
    i.id = Slots.id = Slots.id + 1
    i.override(d)
  def override(i,d): i.__dict__.update(d); return i
  def also(i, **d) : i.override(d)
  def __eq__(i,j)  : return i.id == j.id
  def __ne__(i,j)  : return i.id != j.id
  def __repr__(i)  : return '{' + showd(i.__dict__) + '}'

"""

Note that _Slots_ can pretty print themselves using
the _showd_ function (shown above).  Also, since our
_Slots_ have a unique _id_, then we can quickly test
for equality and inequality.

### Tree Iterators

To simplify the processing of trees, we define some
iterators to return all _nodes_ or just the _leafs_
of the tree.

"""

def nodes(t,lvl=0):
  "Iterator. Return all nodes."
  if t:
    yield lvl,t
    for t1 in [t._left,t._right]:
      for lvl1,leaf in nodes(t1,lvl+1):
        yield lvl1,leaf

def leafs(t):
  "Iterator: returns all leaf nodes."
  for lvl,node in nodes(t):
    if not node._left and not node._right:
      yield lvl,node

"""

### Pretty Printing

The _ditto_ function marks repeated entries in a column 
with a "_._".

"""

def ditto(lst,old,mark="."):
  """Show 'mark' if an item of  lst is same as old.
     As a side-effect, update cache of 'old' values."""
  out = []
  for i,now in enumerate(lst):
    before = old.get(i,None) # get old it if exists
    out   += [mark if  before == now else now]
    old[i] = now # next time, 'now' is the 'old' value
  return out # the lst with ditto marks inserted

"""

Once we "ditto" a list of lists, we have to lay it
out and pretty print it for the users.

"""

def align(lsts):
  "Print, filled to max width of each column."
  widths = {}
  for lst in lsts: # pass1- find column max widths
    for n,x in enumerate(lst):
      w = len('%s' % x)
      widths[n] = max(widths.get(n,0),w)
  for lst in lsts: # pass2- print to max width
    for n,x in enumerate(lst):
      say(('%s' % x).rjust(widths[n],' '))
    print ""
  print ""

"""

# Putting it all Together

The following code is an example of how to use
_chunk_.

## _nasa93 

The following code initializes some globals then
builds a tree of clusters from _nasa93_ using
_chunk_.  Then, using the _leafs_ iterator, this
code traverses the leaf clusters of the tree to
pretty prints the clusters in aligned columns (using
ditto marks).

"""

class Nums:
  def __init__(i, inits=[],lo=10**32, hi=-10**32):
    i.lo, i.hi, i.lst,i._has  = lo,hi, [],None
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    assert isinstance(x,(float,int))
    i._has = None
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
    i.lst += [x]
    return i
  def has(i):
    if not i._has:
      i.lst  = sorted(i.lst)
      q      = len(i.lst)/4
      i._has = Slots(med=i.lst[q*2],
                     iqr=i.lst[q*3] - i.lst[q])
    return i._has

The = Slots(normalize=True,missing="?")

def _chunkDemo(model=nasa93):
  seed(1)
  data   = project2Slots( model() )
  options= settings(verbose = True,
                    minSize = 25)
  tree   = chunk(model,  data ,options)
  #exit()
  eg,cid = 0,0
  exit()
  for lvl,leaf in leafs(tree):
    context = leaf.value
    cid += 1
    print "----| cluster",cid,"|","-"*35
    lines  = []
    dittos = {}
    num = Nums()
    for row in sorted(context,key=lambda x:x.syms[0]):
      num += row.obj[0]
      eg += 1
      pre = ["project ", eg,": "]
      params     = ditto(row.syms,dittos)
      params[0]  = str(params[0]) + " "
      params[-1] = " " + str(params[-1])
      lines     += [pre + params + [" = "] + row.obj]
    align(lines)
    if num.lst: print num.has()

 
from bias import data

_chunkDemo(data)



"""

Note that we override the default _settings_ to
offer control values that make more sense for small
data sets like _nasa93_ (see the _minSize_ setting).

To change the default load behavior, change the last line
of _chnunk.py_ (which is currently _\_chunkDemo()_). 

"""
