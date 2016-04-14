from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier #SVM Linear

tags=[]
tweets=[]
neutral=[]
tag_names=['trump_positive','trump_negative','hillary_positive','hillary_negative','bernie_positive','bernie_negative','cruz_positive','cruz_negative','republican_positive','republican_negative','democrat_positive','democrat_negative','neutral']

files=['annotated.csv.sortedaa','annotated.csv.sortedab','annotated.csv.sortedac','annotated.csv.sortedad','annotated.csv.sortedae','annotated.csv.sortedaf']
path="../python/annotated2/"
for file in files:
    with open(path+file) as f:
        for line in f:
            parta = line.split(",")
            if parta[8] == "1":
                tags.append(0)  # trump_positive
                tweets.append(parta[14])
            elif parta[8] == "-1":
                tags.append(1)  # trump_negative
                tweets.append(parta[14])
            elif parta[6]=="0" and parta[7]=="0" and parta[8]=="0" and parta[9]=="0" and parta[10]=="0" and parta[11]=="0":
                neutral.append(parta[14])

#text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),])
text_clf = text_clf.fit(tweets, tags)

predicted = text_clf.predict(neutral)
out=[]
print(tags.count(0),tags.count(1),set(predicted))
pos=0
neg=0
for i in range(len(neutral)):
   out.append(neutral[i].strip()+": "+tag_names[predicted[i]])
   if predicted[i]==0:
       pos+=1
   else:
       neg+=1

print pos,neg

open("output.txt",'w').write("\n".join(out))

