# BMI Calculator

A simple and interactive BMI (Body Mass Index) Calculator developed using Python and Tkinter as part of the Oasis Infobyte Python Programming Internship – Task 2.

## About the Project

The BMI Calculator is a desktop application that calculates a person's Body Mass Index based on their height and weight.

It provides the calculated BMI value along with its corresponding category through a clean and user-friendly graphical interface.

## Features

- User-friendly graphical interface using Tkinter.
- Height input in centimeters.
- Weight input in kilograms.
- Automatic BMI calculation.
- BMI category detection.
- Color-coded BMI results.
- Input validation and error handling.
- Reset functionality.
- Keyboard support using the Enter key.

## BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal Weight |
| 25 – 29.9 | Overweight |
| 30 and above | Obese |

## Technologies Used

- Python 3
- Tkinter
- VS Code

## Project Structure

```text
Python-Task2-BMICalculator/
│
├── main.py
└── README.md
```

## How to Run

1. Install Python 3 on your computer.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Open the terminal.
5. Execute the following command:

```bash
python main.py
```

6. Enter your height and weight.
7. Click the Calculate BMI button to view your result.

## BMI Formula

BMI is calculated using:

```text
BMI = Weight (kg) / Height (m)²
```

Example:

Height = 170 cm  
Weight = 65 kg

BMI = 65 / (1.70 × 1.70)

BMI = 22.49

Category = Normal Weight

## Validation

The application handles:

- Empty input fields.
- Invalid numeric values.
- Negative and zero values.
- Height outside the accepted range.
- Weight outside the accepted range.

## Internship

**Organization:** Oasis Infobyte  
**Internship:** Python Programming Internship  
**Task:** Task 2 – BMI Calculator

## Disclaimer

BMI is a screening measure and is not a substitute for professional medical advice or diagnosis.