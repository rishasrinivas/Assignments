# STEP 1: Install required libraries
!pip install spacy textblob text2emotion nltk gensim matplotlib seaborn wordcloud networkx

# STEP 2: Imports
import os
import spacy
import nltk
from textblob import TextBlob
from gensim import corpora, models
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# STEP 3: Create results directories
os.makedirs("results/plots", exist_ok=True)
os.makedirs("results/reports", exist_ok=True)

# STEP 4: Load spaCy model
nlp = spacy.load("en_core_web_sm")

# STEP 5: Load abstracts
with open("colorectal_cancer_abstracts.txt", "r", encoding="utf-8") as f:
    abstracts = f.read().split("\n\n---\n\n")

# STEP 6: Initialize containers
entity_freq = {}
sentiments = []
emotions = {"Happy":0, "Angry":0, "Surprise":0, "Sad":0, "Fear":0}
tokenized_texts = []
co_occurrence = {}

# STEP 7: Process each abstract
for abstract in abstracts:
    doc = nlp(abstract)
    
    # Named Entity Recognition
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "DISEASE", "DRUG", "GENE", "PROTEIN", "CHEMICAL"]]
    for ent in entities:
        entity_freq[ent] = entity_freq.get(ent, 0) + 1
    
    # Co-occurrence mapping
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            pair = tuple(sorted([entities[i], entities[j]]))
            co_occurrence[pair] = co_occurrence.get(pair, 0) + 1
    
    # Sentiment
    blob = TextBlob(abstract)
    sentiments.append(blob.sentiment.polarity)
    
    # Emotion
    emo = te.get_emotion(abstract)
    for key in emotions:
        emotions[key] += emo.get(key, 0)
    
    # Tokenization for topic modeling
    tokens = word_tokenize(abstract.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    tokenized_texts.append(tokens)

# STEP 8: Save entity frequencies
with open("results/reports/entity_frequencies.txt", "w", encoding="utf-8") as f:
    for ent, freq in sorted(entity_freq.items(), key=lambda x: x[1], reverse=True):
        f.write(f"{ent}: {freq}\n")

# STEP 9: Topic Modeling with LDA
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=10)

with open("results/reports/topics.txt", "w", encoding="utf-8") as f:
    for i, topic in lda_model.print_topics():
        f.write(f"Topic {i}: {topic}\n")

# STEP 10: Visualizations

# Entity Frequency Plot
top_entities = sorted(entity_freq.items(), key=lambda x: x[1], reverse=True)[:10]
labels, counts = zip(*top_entities)
plt.figure(figsize=(10,6))
sns.barplot(x=list(counts), y=list(labels), palette="viridis")
plt.title("Top Named Entities")
plt.xlabel("Frequency")
plt.ylabel("Entity")
plt.tight_layout()
plt.savefig("results/plots/top_entities.png")
plt.close()

# Sentiment Distribution
plt.figure(figsize=(8,5))
sns.histplot(sentiments, bins=20, kde=True, color="skyblue")
plt.title("Sentiment Distribution")
plt.xlabel("Polarity")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("results/plots/sentiment_distribution.png")
plt.close()


# Word Cloud of Entities
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(entity_freq.keys()))
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Entity Word Cloud")
plt.tight_layout()
plt.savefig("results/plots/entity_wordcloud.png")
plt.close()

# Co-occurrence Network
G = nx.Graph()
for (e1, e2), weight in co_occurrence.items():
    if weight > 2:  # filter weak links
        G.add_edge(e1, e2, weight=weight)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
plt.title("Entity Co-occurrence Network")
plt.tight_layout()
plt.savefig("results/plots/cooccurrence_network.png")
plt.close()
