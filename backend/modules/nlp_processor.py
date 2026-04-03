import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import logging

# Ensure NLTK datasets are available (download if not present)
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

class ISLConverter:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        # Custom ISL stop words (articles, auxiliary verbs, etc.)
        self.stop_words = set(stopwords.words('english'))
        # Additional words to remove for strict ISL grammar
        self.stop_words.update(['am', 'is', 'are', 'was', 'were', 'be', 'being', 'been', 'to', 'the', 'a', 'an'])
        
    def english_to_isl(self, text: str) -> list[str]:
        """
        Converts English text into an ISL-compatible list of fundamental words/signs.
        E.g. "I am going to school" -> ["I", "GO", "SCHOOL"]
        """
        if not text:
            return []
            
        try:
            # Tokenize words
            words = word_tokenize(text.lower())
            
            isl_words = []
            for word in words:
                # Remove punctuation
                if not word.isalnum():
                    continue
                    
                # Skip stop words & auxiliary verbs
                if word in self.stop_words:
                    if word not in ['i', 'we', 'you', 'he', 'she', 'they', 'it']: # Keep pronouns despite them being in stopwords sometimes
                        if word != 'i': # NLTK puts 'i' in stopwords
                            pass
                
                # If word is 'i' but it's in NLTK stop words, keep it.
                if word in self.stop_words and word not in ['i', 'we', 'you', 'he', 'she', 'they', 'it']:
                    continue
                    
                # Lemmatize the word (convert to root form, e.g., going -> go, goes -> go)
                root_word = self.lemmatizer.lemmatize(word, pos='v') # Lemmatize as verb
                
                # Convert to uppercase for display consistency
                isl_words.append(root_word.upper())
                
            return isl_words
        except Exception as e:
            logging.error(f"Error in ISL conversion: {e}")
            # Fallback to simple split
            return [w.upper() for w in text.split()]
            
isl_converter = ISLConverter()
