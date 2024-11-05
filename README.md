# Mini Project trying Generators #

disease.py have some notes to the focus area of the program, but i will add them here aswell.
 - Focus: Using the generator to not store any data in memory from the dataset.
 - Using Composition to make single responsibility functions
 - Calculate the fitness of people in the dataset based on their MET score without storing any of the read data in memory.

## How to Run ##
- Download github repo
- I did not make an executable so run the program in the terminal with:
python3 disease.py cardio_train.csv


## Content Files ##
disease.py uses the file cardio_train.csv.

## Extra Applications (Prototype ideas) ##

PythonApplication1.py - Uses any big file (not provided since its just a prototype to test big generators vs readers in a quick plain scenario).

try.py - Evaluates some functional programing aspects to see which would be most comprehensive to use in the implementation.

## Notes ##
I mostly worked in disease becasue the data was more manageable than the chess piece data used in the pythonApplication1.
It's only focus was to see what happened with too large files to store. It's mostly there as a prototype and is why the dataset is not accounted for.


