from googletrans import Translator
import deepl
from sudachipy import tokenizer, dictionary
import pandas as pd
import wikipedia
import stanza
import sys

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
key = "" # API key for DeepL
translator = deepl.Translator(key)


def convert_query(query, tokenizer, mode, mapping, lemma=False, normalize=False):
    '''
    Preprocesses a Japanese query. Replaces Pokemon names with their English equivalents, and lemmatizes and normalizes the
    words.
    
        Parameters:
            query (string): the Japanese query to be preprocessed
            tokenizer: the sudachi tokenizer
            mode: the mode for the sudachi tokenizer
            mapping (pandas.core.frame.DataFrame): the mapping from English to Japanese names
            lemma (bool): whether or not to lemmatize the words in the query
            normalize (bool): whether or not to normalize the words in the query
            
        Returns: 
            query (string): the preprocessed query
    '''
    mapping_eng = list(mapping['English'])
    mapping_jpn = list(mapping['Japanese'])
    tokens = [m.surface() for m in tokenizer.tokenize(query, mode)]
    for m in tokenizer.tokenize(query, mode):
            if '固有名詞' in m.part_of_speech():
                if m.surface() in mapping_jpn:
                    name_idx = mapping_jpn.index(m.surface())
                    translated_name = mapping_eng[name_idx]
                    tokens = list(map(lambda x: x.replace(m.surface(), translated_name), tokens))
            elif lemma == True:
                tokens = list(map(lambda x: x.replace(m.surface(), m.dictionary_form()), tokens))
            if normalize == True:
                tokens = list(map(lambda x: x.replace(m.surface(), m.normalized_form()), tokens))
    return ''.join(tokens)

def convert_query_en(query, mapping, lemma=False):
    '''
    Preprocesses an English query. Replaces Pokemon names with their Japanese equivalents, and lemmatizes the words.
        Parameters:
            query (string): the English query to be preprocessed
            mapping (pandas.core.frame.DataFrame): the mapping from English to Japanese names
            lemma (bool): whether or not to lemmatize the words in the query
            
        Returns: 
            query (string): the preprocessed query
    '''
    mapping_eng = list(mapping['English'])
    mapping_jpn = list(mapping['Japanese'])
    query_split = query.split()
    for word in query_split:
        if word in mapping_eng:
            name_idx = mapping_eng.index(word)
            translated_name = mapping_jpn[name_idx]
            query_split = list(map(lambda x: x.replace(word, translated_name), query_split))
            query = ' '.join(query_split)
    if lemma == True:
        doc = nlp(query)
        for sent in doc.sentences:
            for word in sent.words:
                query_split = list(map(lambda x: x.replace(word.text, word.lemma), query_split))
    return ' '.join(query_split)

def translate_query(query, source_language):
    '''
    Translates a query that has already been preprocessed. Uses the DeepL translator.
        Parameters:
            query (string): the query to be translated
            source_language (string): the language that the query is in. If 'en', translates into Japanese. 
            
        Returns: 
            query (string): the translated query
    '''
    if source_language == 'en':
        return translator.translate_text(query, source_lang='EN', target_lang='JA')
    else:
        return translator.translate_text(query, source_lang='JA', target_lang='EN-US')

def search_en(query, mapping, lemma=True):
    '''
    Performs the entire search process on an English query. First the query is preprocessed, then translated into Japanese, 
    then a search is performed on Japanese wikipedia.
        Parameters:
            query (string): the query 
            mapping (pandas.core.frame.DataFrame): the mapping from English to Japanese names
            lemma (bool): whether or not to lemmatize the query before translation
            
        Returns: 
            results (list[str]): the titles of the top 10 results from Japanese Wikipedia. 
    '''
    query = convert_query_en(query, mapping, lemma)
    query = translate_query(query, 'en')
    wikipedia.set_lang('ja')
    results = wikipedia.search(query)
    return results

def search_ja(query, mapping, tokenizer, mode, lemma=False, normalize=False):
    '''
    Performs the entire search process on an English query. First the query is preprocessed, then translated into Japanese, 
    then a search is performed on Japanese wikipedia.
        Parameters:
            query (string): the query 
            mapping (pandas.core.frame.DataFrame): the mapping from English to Japanese names
            tokenizer: the sudachi tokenizer
            mode: the mode for the sudachi tokenizer
            lemma (bool): whether or not to lemmatize the words in the query
            normalize (bool): whether or not to normalize the words in the query
            
        Returns: 
            results (list[str]): the titles of the top 10 results from English Wikipedia. 
    '''
    query = convert_query(query=query, tokenizer=tokenizer, mode=mode, mapping=mapping, lemma=lemma, normalize=normalize)
    query = translate_query(query, 'ja')
    wikipedia.set_lang('en')
    results = wikipedia.search(query)
    return results

def main():
    query = sys.argv[1]
    source_lang = sys.argv[2]
    lemma = sys.argv[3]
    if source_lang == 'ja':
        normalize = sys.argv[4]
    mapping = pd.read_csv('pokemonmap.csv')
    tokenizer_s = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    if source_lang == 'en':
        results = search_en(query, mapping, lemma)
    elif source_lang != 'ja':
        print("Language not supported. Please use either English (en) or Japanese (ja)")
    else:
        results = search_ja(query, mapping, tokenizer_s, mode, lemma, normalize)

    print('Titles of top 10 retrieved Wikipedia pages: ', results)

if __name__ == '__main__':
    main()
