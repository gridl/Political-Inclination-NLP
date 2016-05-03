categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier #SVM Linear
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
#print twenty_train.filenames
#print twenty_train.target
#print twenty_train.target_names
#count_vect = CountVectorizer()
#X_train_counts = count_vect.fit_transform(twenty_train.data)
#tfidf_transformer = TfidfTransformer()
#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#print X_train_tfidf.shape
#clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
#text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),])
text_clf = text_clf.fit(twenty_train.data, twenty_train.target)
docs_new = ['God is love', 'OpenGL on the GPU is fast']
#X_new_counts = count_vect.transform(docs_new)
#X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = text_clf.predict(docs_new)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
#print X_train_counts.shape
#print count_vect.vocabulary_.get(u'gdfsfgfdsgdfg')