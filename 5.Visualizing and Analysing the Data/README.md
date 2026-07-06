# Data Visualization and Analysis

## Description

This phase focuses on exploring and understanding the dataset through
visualization and statistical analysis. Various charts, graphs, and
analytical techniques are used to identify patterns, trends, and
relationships within the credit card application data.

## Importing the Libraries

The required Python libraries are imported to perform data manipulation,
visualization, preprocessing, model training, and evaluation tasks.

Libraries used include: - Pandas - NumPy - Matplotlib - Seaborn -
Scikit-learn

## Read the Dataset

The project uses two datasets: - application_record.csv -
credit_record.csv

The datasets are loaded using Pandas:

``` python
app = pd.read_csv('application_record.csv')
credit = pd.read_csv('credit_record.csv')
```

The head() function is used to inspect the first few records.

## Univariate Analysis

Univariate analysis studies each feature independently using: -
Frequency counts - Count plots - Histograms - Box plots

This helps understand the distribution of individual variables.

## Multivariate Analysis

Multivariate analysis explores relationships among multiple variables
using: - Correlation matrices - Heatmaps - Pair plots - Comparative
visualizations

These methods identify interactions between features affecting credit
card approval decisions.

## Descriptive Analysis

Descriptive statistics summarize the dataset using: - Count - Mean -
Standard deviation - Minimum value - Maximum value - Quartiles - Median

Example:

``` python
df.describe()
```
