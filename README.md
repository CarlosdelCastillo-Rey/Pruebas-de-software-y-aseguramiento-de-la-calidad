# Activities 4.2 and 5.2 – Programming Exercises

**Course:** Software Testing and Quality Assurance  
**Student:** Carlos Fernando Del Castillo Rey  
**Student ID:** A01796595  

---

## Project Description

This repository contains the solutions for **Activity 4.2 – Programming Exercise 1** and **Activity 5.2 – Programming Exercise**, developed in Python.

The objective of these activities is to implement command-line Python programs that process file-based input using **basic algorithms only**, include **robust error handling**, measure **execution time**, and comply with **PEP8 coding standards**.

All programs:
- Are executed from the command line
- Read input data from files or folders
- Print results to the console
- Save results to output files
- Continue execution even when invalid data is detected

---

## Project Structure

```
├── Archivos de apoyo/
│   ├── A4.2 Archivos de Apoyo - 06-02-26/
│   └── A5.2 Archivos de Apoyo/
├── Data/
│   ├── A4.2/
│   └── A5.2/
│       ├── TC1/
│       ├── TC2/
│       └── TC3/
├── Output/
│   ├── A4.2/
│   └── A5.2/
│       └── SalesResults.txt
├── src/
│   ├── A4.2/
│   │   ├── compute_statistics.py
│   │   ├── convert_numbers.py
│   │   └── word_count.py
│   └── A5.2/
│       └── compute_sales.py
├── SS of score/
│   └── PyLint_Score.png
├── .gitattributes
├── .gitignore
└── README.md
```

---

## Activity 4.2 – Programming Exercise 1

### Program 1: Descriptive Statistics  
**File:** `compute_statistics.py`

#### Description
Reads numeric data from a text file and computes descriptive statistics using basic algorithms:
- Mean  
- Median  
- Mode  
- Variance  
- Standard Deviation  

Invalid data is detected, reported to the console, and skipped without interrupting execution.

#### Execution
```bash
python src/A4.2/compute_statistics.py Data/A4.2/P1
```

**Output**
- Printed to the console  
- Saved to `Output/A4.2/StatisticsResults.txt`

---

### Program 2: Number Conversion  
**File:** `convert_numbers.py`

#### Description
Reads integer values and converts each number to:
- Binary  
- Hexadecimal  

All conversions are implemented manually without using built-in functions such as `bin()` or `hex()`.

Invalid data is reported and execution continues.

#### Execution
```bash
python src/A4.2/convert_numbers.py Data/A4.2/P2
```

**Output**
- Printed to the console  
- Saved to `Output/A4.2/ConvertionResults.txt`

---

### Program 3: Word Count  
**File:** `word_count.py`

#### Description
Processes text files to identify:
- All distinct words  
- Frequency of each word  

The program supports processing a single file or all `TC*.txt` files contained in a folder.

Empty lines and invalid input are reported as errors, but execution continues.

#### Execution
```bash
python src/A4.2/word_count.py Data/A4.2/P3
```

**Output**
- Printed to the console  
- Saved to `Output/A4.2/WordCountResults.txt`

---

## Activity 5.2 – Sales Processing Program

### Program: Sales Cost Calculator  
**File:** `compute_sales.py`

#### Description
This program processes sales data using:
- A base product catalogue located in `TC1`
- Multiple sales records located in `TC1`, `TC2`, `TC3`, etc.

The program:
- Loads the product catalogue once from `TC1`
- Processes all test cases automatically
- Computes total sales cost per product
- Detects and reports invalid data without stopping execution
- Measures execution time per test case

#### Execution
From the project root:
```bash
python src/A5.2/compute_sales.py Data/A5.2
```

**Output**
- Results printed to the console  
- Consolidated output saved to:
  `Output/A5.2/SalesResults.txt`

---

## Execution Time

All programs measure execution time using `time.perf_counter()`.

The elapsed time:
- Is displayed in the console  
- Is included in the corresponding output file  

---

## Code Quality

All programs comply with **PEP8**.

Static code analysis performed using:
- `pylint` (10.00 / 10)
- `flake8` (no errors)

Evidence of static analysis scores is included in:
```
SS of score/
```

---

## Requirements Compliance

- Command-line execution  
- File-based input  
- Basic algorithms only  
- Error handling with continued execution  
- Support for hundreds to thousands of input items  
- Results written to output files  
- Execution time measurement and reporting  
