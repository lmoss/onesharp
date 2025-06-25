# Invitation to Computability 

This is a textbook on the basics of computability theory, originating in classes given by the author 
at Indiana University for quite a few years.  My students are mainly graduate students in either mathematics or computer science, always with a few undergraduates and a few grad students from philosophy and other disciplines.

In some ways, the content of the book is standard, and in some ways it is not. It treats the basic topics of the subject: the concept of computability, primitive recursion, mu-recursion, universal functions, the Recursion Theorem, and undecidability in computability theory, mathematics, and logic.  Of course we are living decades past the original proofs of these results, and so the presentation here will differ.  This book will try to make pointers to many of the developments in computability theory and computer science that have come from the classical material.  

## Why a Jupyter book?

We are also living in the wake of several revolutions in society coming from the advent of computers and the 
worldwide web.  This is on my mind front and center as I prepare this book.  It should not be strange that a 
book about computation theory should use up-to-date computational tools. This book uses Python and various 
packages, Jupyter notebooks and everything needed to work with them, $\LaTeX$, github, and more.  In the 
course of working on the book I became interested in using all of these computational artifacts, mainly as a 
way of seeing what would work in a textbook, and what would not. Since working in this medium is new to me 
(and pretty much everyone), I became as interested in those aspects of the project as in the content. Here are some of artifacts found here but not in a traditional book on computability theory: a executable Python code, especially in the beginning chapters; a variety of pictures and charts; the ability to hide technical passages and to otherwise structure a text; and clickable references to discussions, papers,
[and even poems](http://www.lel.ed.ac.uk/~gpullum/loopsnoop.html), both inside and outside of the book  itself. In time I will consider adding animations to illustrate some of the dynamism that I sense with computably enumerable sets which is arrested in any print presentation.  I also would like to incorporate tools for readers to annotate and discuss matters, enabling a community of  readers.  In short, I am aiming for something which is both a short textbook and an intellectual version of a coffee-table book.

# Intended audience

This book is aimed at anyone who frequently encounters the very basic parts of computability theory and has the needed mathematical background to read it.  That background is a working familiarity with mathematical notation and discourse.   One should know how to read mathematics.  This would be the wrong place to learn basic abstract mathematics; the pace and level would be too much.   But if you can read mathematics, that is enough: nothing else is really assumed.  There are places where it would be good to have seen some induction on the natural numbers and even some basic topics in areas like logic, set theory, and computer programming.  But one could do without the background, I think.  And I hope to have provided enough background on those topics to make what is here accessible.

Some of the people who will benefit from the book: those in the broad area of interdisciplinary logic but who are not specialists in computability theory per se; computer scientists in areas like programming languages and theory of computation; philosophers interested in areas like the philosophy of logic or philosophy of mathematics.  For others, such as those pursuing any area of mathematics, the subject will probably be an "extra".  But "extras" are important, too.  I really have in mind a broad audience of people who might find the topics here intersting.

(content:DistinctiveFeatures)=
# Distinctive features

The are three distinctive features of the book.   Theree of the first four chapters are mainly an online resource.  For this part of the book, this more important than the printed book.    Most of the chapters in that part of the book are Jupyter notebooks. Rather than simply read, these chapters are intended to be *run* and *programmed*. One way to use them is to save them and then run them locally.  Alternatively, one could open them on a hosting service like CoCalc, Binder, or Google Colab.  The Jupyter book format is not so important for the material that comes after the first sections, and for those a traditional print book is going to be available.


## Text register machines

Compared to the many other books on the subject, the treatment here is in some ways more concrete and in some ways more abstract and sophisticated.  How can this be?  It is more concrete in the beginning than other books, and more abstract later on.  It is more concrete in that it comes with a dedicated computer implementation and because it goes into full details on coding.  But later it is more abstract because it discusses matters like recursion on induction on a fairly abstract level and because it also discusses corecursion alongside recursion.

The concrete part in the beginning develops a model of computation which is a variant of a register machine called a *text register machine*.  The "text" in "text register machine" is the feature (orignal here) that the programming language of the machine is the same as the language of programs.  This language the set of words on the two letter alphabet ```{1,#}```.  So the language is called ```1#```. This text comes with two interpreters for ```1#```, so the programs can be run.  The programs themselves are unreadable; that is, they are not intended to be human readable but rather to be used in this presentation of computabililty (and nowhere else).  The book comes with tool support to help people to write long programs in ```1#```; for example, one can turn a flowchart into a  ```1#``` program.  Another tool turns a decription of a primitive recursive function into ```1#``` code.   Those tools are in Python, and while one need not read the programs to use them, a class for computer science students could indeed do so.  Using ```1#``` and the accompanying tools, the main first theorems of computability theory are presented constructively in full detail, with no coding and no hand-waving.    One can write explicit universal programs, $s^m_n$ programs, self-writing programs, the T-predicate, and similar artifacts that essentially *are* the main first results in computability theory.   One can prove Kleene's Second Recursion Theorem in full detail, too.


The use of ```1#``` is why the treatment here is much more explicit than usual.   The way the book works is that those main first results are presented in full detail, and then after doing so it becomes more "hand wavy".  Probably every book on the topic is going becomes "hand wavy" at some point.  But this one does so much later, due to our use of ```1#``` and the extra tools.

## Unsolvable problems

The book also presents quite a bit on undecidability matters and the main negative results of 20th century mathematical logic such as Church's Theorem that satisfiability in first-order logic is undecidable.   In this, we use other interesting undecidability results such as tiling and also matrix mortality.  Our treatment is fuller than any source we know of on these topics.  The reason that we can provide a full treatment is that we build on work done with ```1#``` earlier.  For example, the work done in writing the universal program gets called back when we prove the undecidability of tiling, and the undecidability of tiling leads to a fairly easy proof of Church's Theorem.   


## Recursion principles and the categorical treament of recursion

Another way to make the point about the book being both more concrete and also more sophisticated: the text goes into details about coding in a fair amount of detail -- much more so than usual, since we can illustrate much of the coding work using actual programs.  But at the same time it discusses the overall issues of coding in an abstract way, using ideas originating in abstract data types.

We include pointers to, and digressions on, topics such as recursion principles in very general settings, combinatory logic, and term rewriting.  For example, we discuss recursion on well-founded well-ordered sets.  This all comes in the second part of the book.   That part demands more mathematical maturity than the concrete work.  But the book is also designed so that the first part provides some help to students at beginning levels.

The final distinctive feature of the book is a "gentle introduction" to areas of theoretical computer science related to *algebra* and *coalgebra*.   The goal here is to understand Lawvere's point that ordinary recursion on the natural numbers is equivalent to the initiality of the the natural numbers in a certain category.  Doing this leads to a deeper understanding of the relation of recursion and induction.  So all of this is presented from scratch.  The payoff comes when we "turn the arrows around" to see corecursion and bisimulation, matching recursion and induction.  These are not traditional topics for an introductory course on this subject, but I no reason why they would not be.   And for my intended audicence, they make more sense than the traditional topics which I have chosen to omit, such as oracle computation, c.e. sets and priority arguments, and complexity theory.  These all are the main focus topics of other textbooks and do not fit with what I am trying to do here.

# Using it in a classroom or for self-study


There are a number of ways the book could be used in courses for students in several disciplines.  An instructor would have to be happy with the {ref}`content:DistinctiveFeatures` in the book, especially with the use of ```1#``` and the Jupyter book format.  But one would not have to do everything in the book that uses ```1#``` in order to teach a course.   The chapter that covers the basics of the language could be taught in a week (two or three lectures).  After that, the book contains a tool that help in writing programs by converting flow charts to programs, and then it uses the tool to give explicit ```1#``` programs for the basic primitive recursive functions of numbers and also the universal program.   One could decide that it is enough to know that such programs exist without having students work on the topic.  (On the other hand,  I have found that students really like the challenge of writing the universal program in complete detail. (See {ref}`content:firstGroupProject`. They turn in short papers on what they did; for some it is their first experience of this kind.)  Again, if an instructor wants to omit this experience, they could do so.  

Returning to the book as it stands, there is almost enough here now for a one-semester course.  The topics that are missing are largely those where a traditional printed book would be as good as an online resource.  With the addition of the foundational material at the end, there will be more material here than what would cover in a semester.  The topic of computability has many connections and developments, far too many for an "invitation" book.  My hope is that instructors would use this book for part of their courses and to provide other material as well.   

Much of the action in this book is in the exercises.   So for a student working on their own, it would be important to do a fair number of them and also to have be able to talk to others about their solutions.  I hope that the book would be useful that way.


### Units rather than complete courses

Our subjects are often taught as one of several topics in a course that is mainly about other things.  In computer science settings, "theory of computation" includes automata theory and complexity theory, two subjects that we do not cover.  In philosophy settings, a course might well contain a more thorough discussion of first-order logic.
For all such courses, it would be possible to use this book for a unit in a course as opposed to an entire course.
Here are ideas for units that are roughly four weeks long.

Week 1: basics of ```1#```.

Week 2: Algorithmic problems, and reduction of one problem to another.

Week 3: Mention universal programs and comptuable functions of numbers, but in a way that omits many of the details.

Week 4: Undecidabile problems, including the halting problem, tiling, and satisfiability in first-order logic (Church's Theorem).
As of now (June 2025), the book does not quite have the Incompleteness Theorem and related matters, but eventually this will be part of the book.  Another route to Church's Theorem would be via Post's Correspondence and then matrix mortaility.



# Summer 2025 Status report

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

