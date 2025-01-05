# Invitation to Computability 

Lawrence S. Moss

This is an online textbook on the basics of computability theory, originating in classes given by the author 
at Indiana University for quite a few years.  In some way, the content is standard, and in some ways it is 
not. It treats the basic topics of the subject: the concept of computability, primitive recursion, 
mu-recursion, universal functions, the Enumeration Theorem, the Recursion Theorem, and undecidability in 
computability theory, mathematics, and logic.  Of course we are living decades past the original proofs of 
these results, and so the presentation here will differ, and this book will try to make pointers to many of the 
developments in computability theory and computer science that have come from the clasical material.

We are also living in the wake of several revolutions in society coming from the advent of computers and the 
worldwide web.  This is on my mind front and center as I prepare this book.  It should not be strange that a 
book about computation theory should use up-to-date computational tools. This book uses Python and various 
packages, Jupyter notebooks and everything needed to work with them, $\LaTeX$, github, and more.  In the 
course of working on the book I became interested in using all of these computational artifacts, mainly as a 
way of seeing what would work in a textbook, and what would not. Since working in this medium is new to me 
(and pretty much everyone), I became as interested in those aspects of the project.  Some of the featues of 
this presentation which are not present in a traditional book are: executable Python code, especially in the 
beginning chapters; and clickable references to discussions and papers both inside and outside of the book 
itself. In time I hope to add abilities to for readers annotate and discuss matters, enabling a community of 
readers.  I am not primarily a computability theorist, and so these features of the work are just as 
compelling to me as the content.


The first part of the book uses a variant of register machines using two symbols and a "programming 
language" using those same two symbols, called 1#.  This text comes with a Python interpreter for 1# and 
with tool support to enable students to learn to write programs.  In addition, it is possible to write 
explicit universal programs, self-writing programs, and similar artifacts.  So the course is much more 
explicit than most treatments.  At the same time, it enables one to go further, showing the undecidability 
of tiling using 1#, and then deriving as a corollary Church's Theorem that satisfiability in first-order 
logic is undecidable.

```{note}
Most of the chapters in the book are Jupyter notebooks.
(Some others are markdown files.)
Rather than simply read, these chapters are intended to 
be *run*. One way to use them is to save them and then run them locally.  Alternatively, one could open them 
on a hosting service like CoCalc, Binder, or Google Colab. At the present time, I don't have buttons to run 
it on CoCalc, and the best option is to run them on Colab.  For this, one starts by clicking on the button 
at the top. 
```

## Using the book

There are a number of ways the book could be used in courses for students in several disciplines.  For computer science students,
the subject is often taught as an end-of-semester topic in a theory course.  For this, one would need to select the topics
judiciously and skip some of the beginning material. The book does not currently have much on complexity theory, but this might
change. For mathematics courses aiming at undecidability results in logic, the book has a fair amount of advanced material, leading
up to Church's Theorem on the undecidability of first-order logic.  Overall, there is more than enough material for a course. At the
same time, the topic of computability has many connections and developments, far too many for an "invitation" book. Instructors
might prefer to use this book for some of their courses and to provide other material as well.


