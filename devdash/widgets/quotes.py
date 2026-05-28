"""Developer quote of the day — deterministic from date, no network."""
from __future__ import annotations
import hashlib
from datetime import date


QUOTES = [
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
    ("Java is to JavaScript what car is to carpet.", "Chris Heilmann"),
    ("Knowledge is power.", "Francis Bacon"),
    ("Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code.", "Dan Salomon"),
    ("Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away.", "Antoine de Saint-Exupery"),
    ("Ruby is rubbish! PHP is phpantastic!", "Nikita Popov"),
    ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("Optimism is an occupational hazard of programming: feedback is the treatment.", "Kent Beck"),
    ("When to use iterative development? You should use iterative development only on projects that you want to succeed.", "Martin Fowler"),
    ("Simplicity is the soul of efficiency.", "Austin Freeman"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("The best way to predict the future is to implement it.", "David Heinemeier Hansson"),
    ("Walking on water and developing software from a specification are easy if both are frozen.", "Edward V Berard"),
    ("It's not a bug — it's an undocumented feature.", "Anonymous"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("The most disastrous thing that you can ever learn is your first programming language.", "Alan Kay"),
    ("The function of good software is to make the complex appear simple.", "Grady Booch"),
    ("One of the best programming skills you can have is knowing when to walk away for a while.", "Oscar Godson"),
    ("Any application that can be written in JavaScript, will eventually be written in JavaScript.", "Jeff Atwood"),
    ("Software and cathedrals are much the same — first we build them, then we pray.", "Anonymous"),
    ("The best programmers are not marginally better than merely good ones. They are an order-of-magnitude better.", "Randall E. Stross"),
    ("Without requirements or design, programming is the art of adding bugs to an empty text file.", "Louis Srygley"),
    ("Measuring programming progress by lines of code is like measuring aircraft building progress by weight.", "Bill Gates"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Progress is possible only if we train ourselves to think about programs without thinking of them as pieces of executable code.", "Edsger Dijkstra"),
]


def quote_of_the_day() -> tuple[str, str]:
    today = date.today().isoformat()
    digest = int(hashlib.md5(today.encode()).hexdigest(), 16)
    idx = digest % len(QUOTES)
    return QUOTES[idx]
