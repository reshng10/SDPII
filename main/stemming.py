from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import lovins
#from nltk.corpus import wordnet



porter = PorterStemmer()
lancaster = LancasterStemmer()

#getting input here
s = "Cats are going into troubling"

print(porter.stem(s))
print(lancaster.stem(s))


# stemming sentence

def stemmingSentence(sentence):
    token_words =  word_tokenize(sentence)
    stemmed_sentence = []

    for words in token_words:
        stemmed_sentence.append(porter.stem(word))
        stemmed_sentence.append(" ")
    
    return "".join(stemmed_sentence)

x = stemmingSentence(sentence)
print(x)

#Snowball 

englishStemmer = SnowballStemmer("english")
englishStemmer.stem(sentence)


#Wordnet Lemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

#Lovins stemmer

sent_split = sentence.split()

for wrd in sent_split:
    print(w, lovins.stem(wrd))