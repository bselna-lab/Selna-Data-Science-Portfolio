 # Tidy Data Project

## Overview
This TidyData-Project cleans and explores the Mutant Moneyball dataset, which contains estimated dollar values of comic book collections for 26 X-Men characters, broken out by decade of publication and by valuation source. The original data is in a "messy" or "wide" format, so the goal of the project was to tidy the data. Tidy Data matters because tools like pivot_table and seaborn expect this shape.
The tidy data principles as described by Hadley Wickham are
1. Each variable forms a column.
2. Each observation forms a row.
3. Each type of observational unit forms a table.

## Instructions
1. Open the notebook in Google Colab (the data loads from this repository), or run it locally.
2. Install the dependencies if running locally: `pip install pandas matplotlib seaborn jupyter`
3. Run all cells from top to bottom.

## Dataset Description
The mutant_moneyball.csv dataset has 26 rows and 17 columns. The problem with the data was that the column names contain two variables each (decade and source), so the data is not tidy. My preprocessing steps for tidying were to melt the 16 value columns to long format, split the column names into `decade` and `source`, convert dollar strings to numbers, and drop 132 missing values.

## Visuals
Once the data was tidy, I visualized it. 1 way I did this was through a box plot, which compares the average collection value for each decade, with a bar for each source. I formed this using the sns.barplot function. The y-axis uses a log scale due to the large ranges. See the Figure Below.
<img width="849" height="547" alt="image" src="https://github.com/user-attachments/assets/46071200-092a-4e25-a516-a70777629a30" />

## Sources
To complete this project, I referenced these 2 sources:
- [Tidy Data (Wickham, 2014)](https://vita.had.co.nz/papers/tidy-data.pdf)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

