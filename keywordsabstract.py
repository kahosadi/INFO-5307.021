import re
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    # Remove stopwords
    text = ' '.join([token.text for token in doc if not token.is_stop])

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Stemming
    stemmer = PorterStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])

    return text

def calculate_similarity(keyword, abstract):
    keyword = preprocess_text(keyword)
    abstract = preprocess_text(abstract)

    # Combine keyword and abstract for vectorization
    documents = [keyword, abstract]

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similarity[0][0]

# Example usage student’s perception;teachers’ written feedback;academic writing
#keyword = "speaking Strategy"
#abstract = "This study aims to unpack factors that cause high school students to be anxious when speaking English and how to overcome the anxiety in a public high school in Java, Indonesia. The participants of this study are Grade Twelve students in SMA Negeri 1 Tengaran for the academic year 2022/2023. The study is conducted using observation and interview methods to elicit their anxiety and strategies to deal with speaking English. The findings indicate that the internal causes of English-speaking anxiety are participants' lack of confidence in their pronunciation and fluency in speaking English, limited vocabulary and grammar competence, and a lack of preparation and practice. External causes include a negative learning environment and peers' understanding of spoken English, which affect learners' feelings, confidence, and willingness to keep learning and speaking English. In dealing with anxiety, some preparations for the material used in the activities are reported, but peers’ reactions are not usually anticipated. This study provides experience-based information indicating that when designing and participating in English-speaking activities, potential anxiety should be considered."
#similarity_score = calculate_similarity(keyword, abstract)

#print(f"Similarity Score: {similarity_score}")

# Determine suitableness based on a threshold
#threshold = 0.1
#if similarity_score >= threshold:
#    print("The keyword is suitable for the abstract.")
#else:
#    print("The keyword is not suitable for the abstract.")
