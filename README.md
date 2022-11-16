# onesharp
This is a collection of files and notebooks related either to running 1# or to educational material related to computability theory using those tools.  The goal is to turn these notebooks into an online textbook on computatbility theory.  The target audience are advanced undergraduates and beginning graduate students in either mathematics or computer science, or anyone who has the background and interest to pursue the subject.
I have taugh a class on the subject given at Indiana University for quite a few years.  The previous version is https://iulg.sitehost.iu.edu/trm. I expect to write more on the content and overall approach and to put that in an introductory chapter.

Here is more on the individual files here.

The .ipynb files are Juypter notebooks.   The run on Colab, and upon opening one you might well be asked if you want to run it on Colab.  You probably can run it on any platform that allows Jupyter notebooks, such as CoCalc.

evaluator.ipynb provides a bare-bones interpreter for 1#, allowing the user to enter programs and up to three registers.  One can run things 'step by step' or 'all in one fell swoop'.  There is a bit of error correction for wrong inputs.  But there is very little else in the way of functionality here.

getting_started.ipynb contains two Python programs that run 1#.  For the rest of our work on 1#, this notebook is probably more useful
than evaluator.ipynb.  This is because working in Python also gives us extra tools that make life easier.

sanity.ipynb is a tool to help with writing 1# programs.   It shortens the distance from an algorithm or flowchart to an actual program.
One doesn't have to use it at all, but I think most people would be relieved to see it.

primitive_recursion.ipynb is intended to eventually be a standalone lesson on primitive recursive functions.  It's not completely done.  But it does allow one to enter primitive recursive terms (with a syntax checker), and then it automatically converts them to 1# programs. Before (or while) reading that, one could also look at the general discussion of coding numbers by terms found in arithmetic.ipynb.

self_writing.ipynb contains the write program, then diagonal program, and the self-writing 1# program, and exercise on these.

universal.ipynb is a discussion of the universal 1# program.  My plan is to expand the notebook two_by_two.ipynb into a more detailed discussion of the programming technique that is involved in the universal program.
