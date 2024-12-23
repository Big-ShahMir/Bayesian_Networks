# Naive Bayesian Salary Prediction and Fairness Evaluation

This project implements a **Naive Bayesian Model** and the **Variable Elimination algorithm** to predict salaries based on demographic attributes from the 1994 US Census dataset. Additionally, the project evaluates the fairness of the model's predictions, particularly with respect to gender, exploring concepts such as demographic parity and sufficiency.

## Table of Contents

- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Implementation Details](#implementation-details)
- [How to Run the Project](#how-to-run-the-project)
- [Dataset](#dataset)
- [Evaluation of Fairness](#evaluation-of-fairness)
- [Conclusion](#conclusion)

---

## Introduction

The purpose of this project is to build a machine learning model using Bayesian Networks to predict whether an individual earns more or less than $50K annually, based on demographic and professional attributes. The model uses a Naive Bayesian approach and incorporates fairness evaluations to assess and address potential biases in its predictions.

---

## Problem Statement

The 1994 US Census dataset provides various attributes about individuals, such as their education, marital status, and occupation. The problem is to:
1. Predict salaries based on these attributes using a Naive Bayesian model.
2. Evaluate the fairness of the predictions with respect to gender, ensuring that the model does not inadvertently introduce or perpetuate bias.

---

## Solution Overview

This project solves the problem by:
1. Constructing a **Naive Bayesian Network** with salary as the root node and other attributes as conditional nodes.
2. Implementing the **Variable Elimination algorithm** to perform probabilistic inference and make salary predictions.
3. Training the model on `adult-train.csv` and testing it on `adult-test.csv`.
4. Evaluating fairness using measures like demographic parity and sufficiency.

---

## Key Features

- **Naive Bayesian Model**: Models salary predictions based on conditional probabilities of demographic attributes.
- **Variable Elimination Algorithm**: Implements probabilistic inference for query variables and evidence.
- **Fairness Evaluation**: Assesses fairness using demographic parity, separation, and sufficiency metrics.
- **Exploratory Analysis**: Compares predictions across genders using core and extended evidence sets.

---

## Implementation Details

### Key Functions

The following functions are implemented in `naive_bayes_solution.py`:

1. **normalize**: Normalizes a Factor object without modifying the input.
2. **restrict**: Restricts a factor based on a variable and its value.
3. **sum_out**: Sums out a variable from a factor.
4. **multiply**: Multiplies a list of factors into a single factor.
5. **ve**: Performs variable elimination to compute probabilities for query variables.
6. **naive_bayes_model**: Constructs the Naive Bayesian Network using training data.
7. **explore**: Evaluates fairness metrics and answers exploratory questions.

---

## How to Run the Project

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/naive-bayes-salary-prediction.git
cd naive-bayes-salary-prediction
```
### 2. Run the Training and Testing
```bash
python naive_bayes_solution.py
```

### 3. View the Results
Results should be printed into the terminal and answer the following questioned in order:
1. What percentage of the women in the test data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
2. What percentage of the men in the test data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
3. What percentage of the women in the test data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
4. What percentage of the men in the test data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
5. What percentage of the women in the test data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
6. What percentage of the men in the test data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?

## Dataset

The project uses the 1994 US Census dataset, which is split into two files:

- **`adult-train.csv`**: This file contains training data, including demographic attributes and salary information.
- **`adult-test.csv`**: This file is used to evaluate the performance of the model and its fairness.

## Evaluation of Fairness

### Metrics for Fairness Assessment

1. **Demographic Parity**:  
   The probability of predicting a salary above $50K should be the same for both genders. For instance:  
   - ( P({Salary} > 50K {Gender} = {Male}) = P({Salary} > 50K {Gender} = {Female}) )

2. **Separation**:  
   The predictions should be conditionally independent of gender when evidence is provided. This ensures fairness when considering additional factors.

3. **Sufficiency**:  
   The predictions should be equally accurate for individuals of all genders, reflecting true salary levels accurately.

## Conclusion

This project highlights the potential of Bayesian Networks for predictive tasks while addressing fairness concerns in machine learning. By incorporating fairness metrics, the project emphasizes the importance of equitable AI systems in real-world applications.

Future improvements include:
1. Exploring advanced Bayesian Network structures.
2. Adding fairness-aware modifications to the model.
3. Testing on larger and more diverse datasets.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve this solver.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
