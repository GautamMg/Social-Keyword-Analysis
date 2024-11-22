import pandas as pd
import os
import re

def process_combined_keywords_from_files(keywords, directory='directory/subdirectory'): #Add relevant directories
    result = []
    
    # Loop through each CSV file in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df_keywords = pd.read_csv(file_path)
                        
            if 'word' not in df_keywords.columns or 'frequency' not in df_keywords.columns:
                print(f"Skipping {filename} due to missing required columns.")
                continue
            
            category_name = filename.replace('_Keyword_Frequencies.csv', '')
            
            total_count = 0
            for keyword in keywords:
                pattern = f"^{re.escape(keyword)}$"
                total_count += df_keywords[df_keywords['word'].str.match(pattern, case=False, na=False)]['frequency'].sum()
            
            result.append([category_name, total_count])
    
    return pd.DataFrame(result, columns=['category', 'total_count'])

def main():
    keywords = [
        'social network', 'social networking', 'networking', 'social', 'social apps', 'social app', 
        'social life', 'social media', 'social sports', 'friends', 'friend', 'family', 
        'buddies', 'buddy', 'players', 'group', 'network marketing', 'marketing'
    ]
    
    combined_results = process_combined_keywords_from_files(keywords)

    combined_results.to_csv('Task1/Aggregated_Keyword_Counts.csv', index=False)
    print("Output saved to 'Aggregated_Keyword_Counts.csv'.")

if __name__ == "__main__":
    main()