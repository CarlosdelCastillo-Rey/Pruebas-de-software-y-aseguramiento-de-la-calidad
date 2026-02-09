# Activity 4.2 – Programming Exercise 1

Course: Software Testing and Quality Assurance  
Student: Carlos Fernando Del Castillo Rey  
Student ID: A01796595  

---

## Project Description

This repository contains the solution for Activity 4.2 – Programming Exercise 1.

The objective of this activity is to develop Python programs that process text files from the command line using basic algorithms only, with proper error handling and compliance with PEP8 coding standards.

Each program reads input data from files, performs the required computation, prints results to the console, and stores the results in output files.

---

## Project Structure

├─ Data/  
│ ├─ P1/  
│ │ ├─ TC1.txt  
│ │ ├─ TC2.txt  
│ │ └─ ...  
│ ├─ P2/  
│ └─ P3/  
├─ Output/  
│ ├─ StatisticsResults.txt  
│ ├─ ConvertionResults.txt  
│ └─ WordCountResults.txt  
├─ src/  
│ ├─ compute_statistics.py  
│ ├─ convertNumbers.py  
│ └─ word_count.py  
├─ SS of/  
│ └─ PyLint_Score.png  
└─ README.md  

---

## Program 1: Descriptive Statistics

File: compute_statistics.py

### Description

This program reads numeric data from a file and computes descriptive statistics using basic algorithms:

- Mean  
- Median  
- Mode  
- Variance  
- Standard Deviation  

Invalid data is detected, reported in the console, and skipped without interrupting execution.

### Execution

python src/compute_statistics.py Data/P1

### Output

- Printed to the console  
- Saved to Output/StatisticsResults.txt  

---

## Program 2: Number Conversion

File: convertNumbers.py

### Description

This program reads integer values from a file (or multiple test cases) and converts each number to:

- Binary  
- Hexadecimal  

All conversions are implemented manually using basic algorithms, without using built-in conversion functions such as bin() or hex().

Invalid data is reported and execution continues.

### Execution

python src/convertNumbers.py Data/P2

### Output

- Printed to the console  
- Saved to Output/ConvertionResults.txt  

---

## Program 3: Word Count

File: word_count.py

### Description

This program reads words from text files and identifies:

- All distinct words  
- The frequency of each word  

The program supports processing a single file or all TC*.txt files contained in a folder.

Empty lines and invalid input are reported as errors, but the program continues execution.

### Execution

python src/word_count.py Data/P3

### Output

- Printed to the console  
- Saved to Output/WordCountResults.txt  

---

## Execution Time

Each program measures the total execution time using time.perf_counter().  
The elapsed time is displayed in the console and included in the output file.

---

## Code Quality

- All programs follow PEP8 guidelines  
- Static code analysis was performed using PyLint  
- Evidence of PyLint scores is included in the folder:

SS of/

---

## Requirements Compliance

- Command-line execution  
- File-based input  
- Use of basic algorithms only  
- Error handling with continued execution  
- Support for hundreds to thousands of input items  
- Results written to output files  
- Execution time measurement and reporting  
