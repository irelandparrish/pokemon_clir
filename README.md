# pokemon_clir

## About
In this project, I attempted to perform Japanese-English Cross Language Information Retrieval within a Jupyter Notebook. I took Japanese for three years in college, and translation has always been an interest of mine, so I wanted to do a project related to Japanese-English translation.

In order to challenge myself, I focused on a specific topic that isn't as straightforward as it may seem: Pokemon. The Japanese and English names of Pokemon characters and Pokemon themselves aren't usually the same. For example, Ash is Satoshi in Japanese, Bulbasaur is Fushigidane, Piplup is Pocchama, so on and so forth. When you think of translation, you might think of a mapping of words from one language to another. Love becomes 愛 (ai), thanks becomes ありがとう (arigatou). Thus, one might expect that translation services such as Google Translate would translate English Pokemon names into their correct Japanese equivalents, and vice versa. However, upon trying out some queries in Google Translate and DeepL, I found out that the names were often transliterated. While this might be okay for some situations, it wasn't going to work well for information retrieval, so I had to come up with a way to remedy that issue. 

My solution was to create a spreadsheet that had English Pokemon names in one column and Japanese Pokemon names in the other, to serve as a mapping between the two. I utilized [this list from Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/List_of_Japanese_Pok%C3%A9mon_names) when making the spreadsheet, and added a few extra names of well known characters. I then imported the spreadsheet into the notebook as a Pandas dataframe. 
I tried two different approaches for using the mapping. For Japanese to English translation, I used a Japanese morphological analyzer called SudachiPy to identify proper nouns in sentences. If a given sentence contained a proper noun, I compared that proper noun to the list of Japanese Pokemon names in the Pandas dataframe. If the proper noun was in the list, I directly replaced it within the sentence with the English equivalent, then used Google Translate or DeepL to translate the entire sentence. For English to Japanese translation, I used a more basic approach of just comparing every word in the sentence to the list of English Pokemon names, then replacing with the Japanese names before translating the whole sentence.

## How to use

To run the Jupyter notebook and use the DeepL translator in the script, you'll need to request an API key [here](https://support.deepl.com/hc/en-us/articles/360020695820-API-Key-for-DeepL-s-API). It's a pretty quick process with no wait. 

To run the pokemonclir Python script, run 
> ` $ python pokemonclir.py <QUERY STRING> <SOURCE LANGUAGE> <LEMMATIZE?> <NORMALIZE?> `

For example,
> ` $ python pokemonclir.py "Pokemon Diamond release date" "en" True `

The descriptions of each parameter are as follows:
* Query string (required): The search query
* Source language (required): 'en' or 'ja'. Use 'en' if your query is in English.
* Lemmatize (required): True or False; whether or not to lemmatize the query before translation. Recommended for English, but not for Japanese.
* Normalize (required for Japanese, leave blank for English): True or False; whether or not to normalize the words in the query before translation. Not recommended.

