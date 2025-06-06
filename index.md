# Invitation to Computability 

This is a textbook on the basics of computability theory, originating in classes given by the author 
at Indiana University for quite a few years.  In some way, the content is standard, and in some ways it is 
not. It treats the basic topics of the subject: the concept of computability, primitive recursion, 
mu-recursion, universal functions, the Enumeration Theorem, the Recursion Theorem, and undecidability in 
computability theory, mathematics, and logic.  Of course we are living decades past the original proofs of 
these results, and so the presentation here will differ.  This book will try to make pointers to many of the 
developments in computability theory and computer science that have come from the classical material.  

## Why a Jupyter book?

We are also living in the wake of several revolutions in society coming from the advent of computers and the 
worldwide web.  This is on my mind front and center as I prepare this book.  It should not be strange that a 
book about computation theory should use up-to-date computational tools. This book uses Python and various 
packages, Jupyter notebooks and everything needed to work with them, $\LaTeX$, github, and more.  In the 
course of working on the book I became interested in using all of these computational artifacts, mainly as a 
way of seeing what would work in a textbook, and what would not. Since working in this medium is new to me 
(and pretty much everyone), I became as interested in those aspects of the project as in the content. Here are some of the things found here which are not in a traditional book are:  executable Python code, especially in the beginning chapters; a variety of pictures and charts; the ability to hide technical passages and to otherwise structure a text; and clickable references to discussions, papers,
[and even poems](http://www.lel.ed.ac.uk/~gpullum/loopsnoop.html), both inside and outside of the book  itself. In time I will consider adding animations to illustrate some of the dynamism that I sense with computably enumerable sets which is arrested in any print presentation.  I also would like to incorporate tools for readers to annotate and discuss matters, enabling a community of  readers.  In short, I am aiming for something which is both a short textbook and an intellectual version of a coffee-table book.

# Intended audience

The intended readers are students of certain areas of computer science, mathematics, philosophy, or other fieds.
It it aimed at anyone who frequently encounters the topics of the book and has the needed mathematical background to
read it.  That background is a working familiarity with mathematical notation and discourse.   One should know
how to read mathematics.  This would be the wrong place to learn basic abstract mathematics; the pace and level would be too much.   But if you can read mathematics, that is enough: nothing else is really assumed.  There are places where it would be good to have seen some induction on the natural numbers and even some basic topics in areas like logic, set theory, and computer programming.  But one could do without the background, I think.  And I hope to have provided enough background on those topics to make what is here accessible.

Here is another way to describe the intended audience: people in the broad area of interdisciplinary logic but who are not specialists in computability theory per se.


# Distinctive features

The are three distinctive features of the book.   The first half of the book is mainly an online resource.  For this part of the book, this more important than the printed book.    Most of the chapters in that part of the book are Jupyter notebooks. Rather than simply read, these chapters are intended to  be *run*. One way to use them is to save them and then run them locally.  Alternatively, one could open them on a hosting service like CoCalc, Binder, or Google Colab.  The Jupyter book format is not so important for the material that comes after the first sections, and for those a traditional print book is going to be available.


## Text register machines

Compared to the many other books on the subject, the treatment here is in some ways more concrete and in some ways more abstract and sophisticated.  How can this be?  It is more concrete in the beginning than other books, and more abstract later on. 

The concrete part in the beginning develops a model of computation which is a variant of a register machine called a *text register machine*.  The "text" in "text register machine" is the feature (orignal here) that the programming language of the machine is the same as the language of programs.  This language the set of words on the two letter alphabet ```{1,#}```.  So the language is called ```1#```. This text comes with two interpreters for ```1#```, so the programs can be run.  The programs themselves are unreadable; that is, they are not intended to be human readable but rather to be used in this presentation of computabililty (and nowhere else).  The book comes with tool support to help people to write long programs in ```1#```; for example, one can turn a flowchart into a  ```1#``` program.  Another tool turns a decription of a primitive recursive function into ```1#``` code.   Those tools are in Python, and while one need not read the programs to use them, a class for computer science students could indeed do so.  Using ```1#``` and the accompanying tools, the main first theorems of computability theory are presented constructively in full detail, with no coding and no hand-waving.    One can write explicit universal programs, $s^m_n$ programs, self-writing programs, the T-predicate, and similar artifacts that essentially *are* the main first results in computability theory.   One can prove Kleene's Second Recursion Theorem in full detail, too.


The use of ```1#``` is why the treatment here is much more explicit than usual.   The way the book works is that those main first results are presented in full detail, and then after doing so it becomes more "hand wavy".  Probably every book on the topic is going becomes "hand wavy" at some point.  But this one does so much later, due to our use of ```1#``` and the extra tools.

## Unsolvable problems

The book also presents quite a bit on undecidability matters and the main negative results of 20th century mathematical logic such as Church's Theorem that satisfiability in first-order logic is undecidable.   In this, we use other interesting undecidability results such as tiling and also matrix mortality.  Our treatment is fuller than any source we know of on these topics.  The reason that we can provide a full treatment is that we build on work done with ```1#``` earlier.  For example, the work done in writing the universal program gets called back when we prove the undecidability of tiling, and the undecidability of tiling leads to a fairly easy proof of Church's Theorem.   


## Recursion principles and the categorical treament of recursion

Another way to make the point about the book being both more concrete and also more sophisticated: the text goes into details about coding in a fair amount of detail -- much more so than usual, since we can illustrate much of the coding work using actual programs.  But at the same time it discusses the overall issues of coding in an abstract way, using ideas originating in abstract data types.

We include pointers to, and digressions on, topics such as recursion principles in very general settings, combinatory logic, and term rewriting.  For example, we discuss recursion on well-founded well-ordered sets.  This all comes in the second part of the book.   That part demands more mathematical maturity than the concrete work.  But the book is also designed so that the first part provides some help to students at beginning levels.

The final distinctive feature of the book is a "gentle introduction" to areas of theoretical computer science related to *algebra* and *coalgebra*.   The goal here is to understand Lawvere's point that ordinary recursion on the natural numbers is equivalent to the initiality of the the natural numbers in a certain category.  Doing this leads to a deeper understanding of the relation of recursion and induction.  So all of this is presented from scratch.  The payoff comes when we "turn the arrows around" to see corecursion and bisimulation, matching recursion and induction.  These are not traditional topics for an introductory course on this subject, but I no reason why they would not be.   And for my intended audicence, they make more sense than the traditional topics which I have chosen to omit, such as oracle computation, c.e. sets and priority arguments, and complexity theory.  These all are the main focus topics of other textbooks and do not fit with what I am trying to do here.

  



# Using it in a classroom or for self-study


There are a number of ways the book could be used in courses for students in several disciplines. Of course instructors would have to be happy with register machines as a vehicle to introduce the subject;  I know that not everyone feels this way.  In fact, quite a few books seem to imply that asking students to write programs for machine models like Turing machines and register machines is a form of torture.   I have found that students really like the challenge of writing the universal program in complete detail. (See {ref}`content:firstGroupProject`.) They turn in short papers on what they did; for some it is their first experience of this kind.   However, if an instructor wants to omit this experience, they could do so.

For computer science students, the subjects here are often taught as one of several topics in a computability theory course.  Indeed, in computer science settings, "theory of computation" includes automata theory and complexity theory, two subjects that we do not cover.   For such courses, one would have not have a whole term for this book.  The instructor would need to select the topics judiciously.  But many of the later chapters are mostly independent, and so it could be done.     The same for philosophy courses aiming to cover the Incompleteness Theorem.  This is possible, but the treatment of first-order logic is, well, incomplete: we don't do the full work on the syntax of first-order logic, or on any proof system for it.  On the other hand, we prove the undecidability of satisfiability without mentioning a proof system for first-order logic, and this can be appreciated by students without a logic background.  As of now (June 2025), the book does not have the Incompleteness Theorem and related matters, but eventually this will be part of the book.

Much of the action in this book is in the exercises.   So for a student working on their own, it would be important to do a fair number of them and also to have be able to talk to others about their solutions.  I hope that the book would be useful that way.

Overall, there will eventually be enough material for a one-semester course.  At the time of this writing (June 2025), there already is close to that.   It is likely that an intstuctor would would want to choose some part of the material here based on their own interests and experience, and also on who exactly their students are.  The book is designed with this in mind.  Probably everyone should use the basic material on ```1#```, but after that there are various ways to go.   The topic of computability has many connections and developments, far too many for an "invitation" book.  My hope is that instructors would use this book for part of their courses and to provide other material as well.   

# Status report: Summer 2025

The book that you see here has a ways to go before anyone besides me could use it.  (But if you are interested in doing so, please let me know: I have material that could help, and I would like to know others' opinions about what is here.)   There are a few things in the ```1#``` section that ought to change: 
[the tool called "sanity" that turns flowcharts into programs](content:firstSanity) should be improved so as to have a more forgiving syntax. There needs to be a glossary of the many Python tools that exist that help people write long ```1#``` programs.   

Some of the sections of the book here (c.e. sets) are placeholders.  Others are not even that (Church-Turing Thesis, and also models of computation beyond register machines).

I would like to explore animation as a tool for presenting aspects of this subject.

The section on the Godel Incompleteness Theorem is yet to come.  This might expand to a chapter on its own.

I would like to add sections on combinatory logic, partly to compare the fixed-point combinators there with what we see in the Recursion Theorem, and partly to discuss it as another model of computation.

I mentioned above material on recursion principles and on the categorical treament of recursion.  All of this material exists in the form of notes or lecture slides.  So it needs to be set in a proper form and added to the book.


# Art

The illustrations in the book are by  <a href="https://www.jeffreyfineart.com/">Jeffrey Fine</a>.  I was fortunate to work with him on a <a href="https://www.youtube.com/watch?v=0cH3rB8dIVo">logic-related video</a>.  It's a pleasure to do this again.

The pictures signify.  For example, 

<img src="https://github.com/lmoss/onesharp/blob/main/beaver.jpg?raw=1" width="200" height="160">

is the [Busy Beaver](busyBeaver.ipynb).

The ouroboros

<img src="https://github.com/lmoss/onesharp/blob/main/ourboros1.jpg?raw=1" width="200" height="160">

indicates that we are seeing an interesting example related to self-reference, suggestive of infinity.   

<img src="https://github.com/lmoss/onesharp/blob/main/questions.jpg?raw=1" width="200" height="160">


tells us that we are in the territory of unsolvable problems.

<img src="https://github.com/lmoss/onesharp/blob/main/hopeless.jpg?raw=1" width="200" height="160">


This is used mainly to separate sections of a notebook.

