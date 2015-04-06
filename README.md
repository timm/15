# Structure

If the directory is inst/repo/file.py then this
code is on-line at http://github.com in the `org` 
organization in the `repo` repository at the `file.py` file.

Also, it can
be cloned on your local machine using

    git clone https://github.com/timm/15.git

## Inside my Directories

Files often come in pairs of `X.py` and `Xok.py` as seen here:

+ X.py is some source code
+ Xok.py are some tests and demos of X.py and can
  be called using

    python Xok.py

## Inside my Files

Files source code can contain a magic `@ok` in front 
of a function; e.g.  

    @ok
    def mathsok():
      assert nearly(0.19333, normpdf(10,2,9.5))

Any file marked in this way is run at load time and, if any
asserts fail, some counter `unittest.fails` is updated.

This `@ok` trick can also be used to denote startup actions.

## Working with my Repos

I have a standard `Makefile` holding all my standard 
Python/git idioms.

+ to do XXX

Always start with an update. Always end with a commit.

If working in a group, consider a double clone (note the following can be overkill for small groups):

+ If you and someone else share a repo X
+ Then clone a branch from X  to X2
+ Then clone a branch from X2 to X3
+ Then do you work in X3.

Several times a day, commit to X3 (just for safety). Then, when you have something cool to show your team mates, migrate the changes
back to X.

+ Do a practice merge from X3 back to X2. Retire any merge issues between X3 and X2.
+ Now, you should be able to do a simple merge X3 back to X
