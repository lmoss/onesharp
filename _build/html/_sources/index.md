# Invitation to Computability 

Lawrence S. Moss

This is an online textbook on the basics of computability theory, originating in classes given by the author at Indiana University for quite a few years.  In some way, the content is standard, and in some ways it is not. It treats the basic topics of the subject: the concept of computability, primitive recursion, mu-recursion, universal functions, the Enumeration Theorem, the Recursion Theorem, and undecidability in computability theory, mathematics, and logic.

On the other hand, aspects of the presentation are new.  This is mainly due to the online format using Jupyter notebooks.  The first part of the course uses a variant of register machines using two symbols and a "programming language" using those same two symbols, called 1#.  This text comes with a Python interpreter for 1# and with tool support to enable students to learn to write programs.  In addition, it is possible to write explicit universal programs, self-writing programs, and similar artifacts.  So the course is much more explicit than most treatments.   At the same time, it enables one to go further, showing the undecidability of tiling using 1#, and then deriving as a corollary Church's Theorem that satisfiability in first-order logic is undecidable.

```{tip}
Most of the chapters in the book are [Jupyter notebooks](https://docs.jupyter.org/en/latest/index.html).  So rather than simply
read, they are intended to be *run*. One way to use them is to save them and then run them locally.  Alternatively, one could open
them on a hosting service like CoCalc, Binder, or Google Colab. At the present time, I don't have buttons to run it on CoCalc, and
the best option is to run them on Colab.  For this, one starts by clicking on the button at the top.
```


## Status as of December 15, 2022

I am in the process of adding materials to the book.  The original [source](https://iulg.sitehost.iu.edu/trm) for the course had 
much of the material, and the centerpiece was the Javascript interpreter for 1# developed by my former PhD students Robert Rose and 
David Sprunger. In 2022, I re-wrote the interpreter in Python and turned the website into notebooks.  The rest of the course exists 
in lecture slides.  So much of what I am doing now is revising them and adding them here.

```{admonition} Credits
:class: warning
Only a tiny fraction of the results here is due to the author.
Most are standard in the literature.   In time, I willl add proper credits.
```


## Using the book

There are a number of ways the book could be used in courses for students in several disciplines.  For computer science students,
the subject is often taught as an end-of-semester topic in a theory course.  For this, one would need to select the topics
judiciously and skip some of the beginning material. The book does not currently have much on complexity theory, but this might
change. For mathematics courses aiming at undecidability results in logic, the book has a fair amount of advanced material, leading
up to Church's Theorem on the undecidability of first-order logic.  Overall, there is more than enough material for a course. At the
same time, the topic of computability has many connections and developments, far too many for an "invitation" book. Instructors
might prefer to use this book for some of their courses and to provide other material as well.


