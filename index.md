# Invitation to Computability 

Lawrence S. Moss

This is an online textbook on the basics of computability theory, originating in classes given by the author 
at Indiana University for quite a few years.  In some way, the content is standard, and in some ways it is 
not. It treats the basic topics of the subject: the concept of computability, primitive recursion, 
mu-recursion, universal functions, the Enumeration Theorem, the Recursion Theorem, and undecidability in 
computability theory, mathematics, and logic.  Of course we are living decades past the original proofs of 
these results, and so the presentation here will differ, and we will try to make pointers to many of the 
developments in computability theory and computer science that have come from the clasical material.

We are also living in the wake of several revolutions in society coming from the advent of computers and the 
worldwide web.  This is on my mind front and center as I prepare this book.  It should not be strange that a 
book about computation theory should use up-to-date computational tools. This book uses Python and various 
packages, Jupyter notebooks, $\LaTeX$, github, and various tools needed to make Jupyter books.  In the course 
of working on the book I became interested in using all of these tools, mainly as a way of seeing what would 
work in a textbook, and what would not.

The first part of the book uses a variant of register machines using two symbols and a "programming 
language" using those same two symbols, called 1#.  This text comes with a Python interpreter for 1# and 
with tool support to enable students to learn to write programs.  In addition, it is possible to write 
explicit universal programs, self-writing programs, and similar artifacts.  So the course is much more 
explicit than most treatments.  At the same time, it enables one to go further, showing the undecidability 
of tiling using 1#, and then deriving as a corollary Church's Theorem that satisfiability in first-order 
logic is undecidable.


```{tip} Most of the chapters in the book are [Jupyter 
notebooks](https://docs.jupyter.org/en/latest/index.html).
(Some others are markdown files.)
So rather than simply read, these chapters are intended to 
be *run*. One way to use them is to save them and then run them locally.  Alternatively, one could open them 
on a hosting service like CoCalc, Binder, or Google Colab. At the present time, I don't have buttons to run 
it on CoCalc, and the best option is to run them on Colab.  For this, one starts by clicking on the button 
at the top. ```

## Status as of January 15, 2023

I am in the process of adding materials to the book.  The original 
[source](https://iulg.sitehost.iu.edu/trm) for the course had much of the material, and the centerpiece was 
the Javascript interpreter for 1# developed by my former PhD students Robert Rose and David Sprunger. In 
2022, I re-wrote the interpreter in Python and turned the website into notebooks.  The rest of the course 
exists in lecture slides.  So much of what I am doing now is revising them and adding them here.

```{admonition} Credits
:class: warning
Only a tiny fraction of the results here is due to the author.
Most are standard in the literature.   In time, I willl add proper credits.
```

## Wish List

If anyone sees this and wants to help, here are a few things which I would like.

1. These notebooks open on Colab, but doing that loses the LaTeX macros that are in my _conf.yml file.  It also loses the nice "admonition" boxes, like the "Tip" above.   I would like to rectify this,
and the help on the web doesn't address it.

2. The way I get pictures in discussions such as tiling is very painstaking.  I would like to find some tools that make this easier.

3. Once nice feature of the [Javascript interpreter for 1#](http://rrose1.github.io/jsonesharp/) is that one could 
run it slowly.  In this book as it stands, one can't quite do this.  One can run a program "step-by-step", 
but this means looking at the trace.  It would be nice to have an animation the way the Javascript program 
had it.  For that matter, someone might want to animate some of the proofs in computability theory which 
make use of "movable markers" or other such devices.

4. I don't yet have things set up to get feedback and correction from readers.


## Using the book

There are a number of ways the book could be used in courses for students in several disciplines.  For computer science students,
the subject is often taught as an end-of-semester topic in a theory course.  For this, one would need to select the topics
judiciously and skip some of the beginning material. The book does not currently have much on complexity theory, but this might
change. For mathematics courses aiming at undecidability results in logic, the book has a fair amount of advanced material, leading
up to Church's Theorem on the undecidability of first-order logic.  Overall, there is more than enough material for a course. At the
same time, the topic of computability has many connections and developments, far too many for an "invitation" book. Instructors
might prefer to use this book for some of their courses and to provide other material as well.


