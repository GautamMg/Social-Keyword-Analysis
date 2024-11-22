# Social-Keyword-Analysis

Requirements:
Python Version: 3.8 or higher
	Libraries:
	•	pandas: For data manipulation.
	•	nltk: For text analysis (if used for tokenization or stopwords).
	•	spacy: For advanced NLP tasks like entity recognition and phrase parsing.
	•	numpy: For numerical computations.
	Additional dependencies can be installed using requirements.txt.

 Step 1: Keyword Extraction

	Script: Top_Category_Keywords_Extraction.py
	Task:
	•	Processes raw review data.
	•	Identifies and ranks the top 100 keywords for each category.
	•	Outputs two variables: keyword and frequency.

Step 2: Keyword Aggregation and Social Analysis

	Script: Category_Keyword_Aggregator.py
	Task:
	•	Aggregates keyword counts for all categories.
	•	Cross-references with a dictionary of “social” keywords.
	•	Outputs:
	•	total_frequency of social keywords for each category.
	•	normalized_frequency by dividing total frequency by the number of apps in the category.
