Xerblin
=======

General User Interface Metaphor

## Summary

It provides a single metaphor for interacting with computers that's simple enough to teach to children yet provides facilities that are useful to programmers. It integrates all levels of software from the desktop to assembly language.

There are three basic user-facing elements to a Xerblin system.

*    Stack - a place to put objects for user manipulation. This is similar to a Clipboard but it can hold more than one item at a time. Commands operate on the items on the Stack.
*    Dictionary - a place to keep commands. Any command that is inscribed in the Dictionary can be run from the user interface.
*    Interpreter - A very simple command interpreter that takes care of running commands with the Stack.

In addition to the above three UI elements there are discrete commands that provide the basic functionality of the system and that can be composed into more complex commands. They live in the Dictionary and act upon the Stack. They can be composed into compound commands using three primal relations:

*    Sequence - do one thing after another.
*    Loop - do something over again.
*    Branch - do one thing or another.

Using the above three relations compound commands can be composed to perform more involved tasks using the built-in or user-provided "primitives" and other compound commands.  Composition can be done by program, by command line, in the GUI using the mouse and keyboard, or by means of parsing languages.

With a rich set of basic commands and the three kinds of compound commands you have a completely general computer interface that allows for customization and flexibility and can be easily understood and mastered by the average user.

### Some links:

*   The [old project on Google Code][a]. This is still the reference implementation.
*   [Pigeon Computer][b] is a project I have to develop a simple system to teach computer programing. It includes both a low-level version in assembly language and a high-level version in Python with a Tkinter GUI.

### Historical Info

Way back in the day, over a decade ago, the original source for what became "xerblin" was a book ["System Design from Provably Correct Constructs"][c] by [Dr. James Martin][d] [founder, Oxford Martin School][e] ([personal website][f]).

### Must mention:

I need to expand on each of these eventually.

*   Oberon (Wirth, et. al.)
*   Forth (Moore, et. al.)
*   Jef Raskin, "The Humane Interface"
*   Ted Nelson, "Dream Machines"/"Computer Lib"
*   Alan Kay, Dynabook, VPRI et. al.
*   Chris Okasaki, "Purely Functional Data Structures"



[a]: https://code.google.com/p/xerblin/
[b]: http://thinkpigeon.blogspot.com/?view=mosaic

[c]: http://lccn.loc.gov/84016063 "System Design from Provably Correct Constructs"
[d]: https://en.wikipedia.org/wiki/James_Martin_%28author%29 "Dr. Martin on Wikipedia"
[e]: http://www.oxfordmartin.ox.ac.uk/founder/
[f]: http://www.jamesmartin.com/









