# GAME DESCRIPTION #

INSERTION-SORT is a puzzle solving game in the setting an undercover hacking infiltrating a company. The company, SORT, is concealing some secret, evil scheme, that you must uncover and halt. Your tools include deduction, programs for hacking, and your crafted facade of an innocent employee. But can you maintain your reputation in the company while simultaneously breaking into the employees' laptops? That is the challenge. By socializing with your fellow employees during the day and hacking their computers at night, you may eventually breach the top level of security - your boss's laptop. What secret is the company hiding in all of its information? What secrets about the nature of your task, INSERTION-SORT, could be uncovered in SORT's <?>evil-scheme<?>.


# RUNNING THE GAME #

To run the game, run main.py (which is in the "game" directory) with at least python version 3.4. The program will save your games in saves/ and reference assets such as images, texts, etc. in assets/.

Note: after the beginning sequence of the game, you will be presented with a terminal prompt that looks very similar to a normal terminal prompt. Do not be confused! The game did not quit; this new terminal prompt is actually a part of the game (you are on an in-game computer).

Note: the game will sometimes open tkinter windows (which will appear behind your terminal) that displays various visuals, including images and an interactive (and very challenging) minigame.


# POINTS #

The sources of the points that I planned to earn wiht this project are included in the "pr4points.pdf" file, which is in the same directory as this file.

# SAVES #

You can delete all stored saves with CTRL-c when you are in the main menu (where you are prompted whether to start a new game or continue an saved one). This will make the game reload the SavesManager object when you next start up the game right afterward (when you run main.py and make a new game), so creating a new game will fail right after deleting all the old files (only this one time). The next time you restart (run main.py again), everything should work as expected (you won't get the option to choose a saved game, of course).


# SKIPPING INTRO SCENE#

You can skip the beginning title animation with CTRL-c (if you get tired of seeing it over and over).


# CODE NOTES #

Frequent used abbreviations in my code:
- t: target
- suc: success
