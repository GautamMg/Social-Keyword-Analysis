import pandas as pd
import spacy
from tqdm import tqdm
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

nlp = spacy.load("en_core_web_sm")
url_pattern = re.compile(r'http\S+')
non_letter_pattern = re.compile(r'[^a-z\s]')
space_pattern = re.compile(r'\s+')

def clean_text(text):
    """Data cleaning that includes removing URLs, special characters, and multiple spaces."""
    text = text.lower()
    text = url_pattern.sub('', text)
    text = non_letter_pattern.sub(' ', text)
    text = space_pattern.sub(' ', text).strip()
    return text

def extract_noun_adj_combinations(doc):
    """ To Extract adjective + noun and only noun combinations"""
    unique_phrases = set()
    for i, token in enumerate(doc):
        if token.pos_ == "NOUN" and not token.is_stop:
            if i > 0 and doc[i - 1].pos_ == "ADJ" and not doc[i - 1].is_stop:
                adj_noun_pair = f"{doc[i - 1].lemma_} {token.lemma_}"
                unique_phrases.add(adj_noun_pair)
            else:
                unique_phrases.add(token.lemma_)
    return list(unique_phrases)

def process_texts(texts):
    """SpaCy's nlp.pipe is used to process multiple texts more efficiently and in parallel"""
    all_words = []
    for doc in nlp.pipe(texts, batch_size=100):
        all_words.extend(extract_noun_adj_combinations(doc))
    return all_words

def process_category_file_in_parallel(category_file, chunk_size=5000):
    category_name = "Books"
    all_words = Counter()

    total_texts = sum(1 for _ in pd.read_csv(category_file, chunksize=chunk_size))
    with tqdm(total=total_texts * chunk_size, desc="Processing category name") as progress_bar:
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(process_texts, chunk[['title', 'body']].fillna('').apply(lambda row: f"{row['title']} {row['body']}", axis=1).tolist()) for chunk in pd.read_csv(category_file, chunksize=chunk_size)]
            
            for future in futures:
                result = future.result()
                all_words.update(result)
                progress_bar.update(chunk_size)

    top_1000_words = all_words.most_common(1000)
    return pd.DataFrame(top_1000_words, columns=['word', 'frequency']).assign(category=category_name)

def process_single_category():
    category_file = 'reviews_by_categories/Books.csv'
    processed_df = process_category_file_in_parallel(category_file)
    processed_df.to_csv('output/Top_1000_Keywords_forEachCategory/Books_Keyword_Frequencies.csv', index=False)

if __name__ == "__main__":
    process_single_category()