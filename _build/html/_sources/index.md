# Invitation to Computability 

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
(and pretty much everyone), I became as interested in those aspects of the project as in the content.  Some of the featues of  this presentation which are not present in a traditional book are: many more pictures than
a traditional printed book contains, especially ones in color;  executable Python code, especially in the beginning chapters; and clickable references to discussions and papers both inside and outside of the book 
itself. In time I hope to add animations to illustrate some of the dynamism that everyone feels with computably 
enumerable sets which is arrested in any print presentation.
I also would like to incorporate tools for readers annotate and discuss matters, enabling a community of 
readers.  I am not primarily a computability theorist, and so these features of the work are just as 
compelling to me as the content.  In short, I am aiming for something which is both a short textbook and 
an intellectual version of a coffee-table book.

## Intended audience

The intended readers are students of certain areas of computer science, mathematics, philosophy, or other fieds.
It it aimed at anyone who frequently encounters the topics of the book and has the needed mathematical background to
read it.  That background is a standard familiarity with mathematical notation and discourse.   One should know
how to read mathematics.  But beyond that, nothing is really assumed.  There are places where it would be good to
have seen some basic topics in areas like logic, set theory, and computer programming; I hope to have provided
enough background on those to make what is here accessible.

## Distinctive features

The main feature of the book is that it is an online resource rather than a printed book.
Most of the chapters in the book are Jupyter notebooks. (Some others are markdown files.)
Rather than simply read, these chapters are intended to  be *run*. One way to use them is to save them and then run them locally.  Alternatively, one could open them  on a hosting service like CoCalc, Binder, or Google Colab. At the present time, I don't have buttons to run it on CoCalc, and the best option is to run them on Colab.  For this, one starts by clicking on the button at the top. 

Compared to the many other books on the subject, the treatment here is in some ways more concrete and in some ways more abstract and sophisticated.  The particular model of computation developed here is a variant of register machines called *text register machines*.  A "text" register machine is a register machine whose programming language alphabet is the same as the alphabet written into the registers.  For us, the programming language is a set of words on the two letter alphabet ```{1,#}```.  So the language is called ```1#```. This text comes with a Python interpreter for ```1#```, so the programs can be run.  The programs themselves are unreadable.  But the book comes with tool support to enable people to write programs; for example, one can turn a flowchart into a  ```1#``` program.      The main first theorems of computability theory are presented constructively in full detail.   So one can write explicit universal programs, $s^m_n$ programs, self-writing programs, the T-predicate, and similar artifacts that essentially *are* the main first results in computability theory.  This is why the treatment here is much more explicit than usual. 

The ways in which the text are more sophisticated include pointers to, and digressions on, topics such as recursion principles in very general settings, combinatory logic, term rewriting, etc. 
Another way to make the point about being both more concrete and also more sophisticated: the text goes into details about coding in a fair amount of detail, but at the same time it discusses the overall issues of coding in an abstract way that owes a lot to abstract data types.  Returning to the book, it also presents quite a bit on concrete undecidability matters and the main negative results of 20th century mathematical logic such as 
Church's Theorem that satisfiability in first-order logic is undecidable.


## Using it in a classroom or for self-study


There are a number of ways the book could be used in courses for students in several disciplines. Of course instructors would have to be happy with register machines as a vehicle to introduce the subject;  I know that not everyone feels this way.    For computer science students, the subject is often taught as an end-of-semester topic in a theory course.  For this, one would need to select the topics judiciously.   The same for philosophy courses aiming to cover the Incompleteness Theorem.  This is possible, but the treatment of first-order logic is, well, incomplete: we don't do the full work on the syntax of first-order logic, or on any proof system for it.

Much of the action in this book is in the exercises.   So for a student working on their own, it would be important to do a fair number of them and also to have be able to talk to others about their solutions.  I hope that the book would be useful that way.

Overall, there is enough material for a course, but probably one would would want to supplement it based on the interests of the students and instructor.  At the same time, the topic of computability has many connections and developments, far too many for an "invitation" book.  My hope is that instructors would use this book for part of their courses and to provide other material as well.   


