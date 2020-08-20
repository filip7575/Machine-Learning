# -*- coding: utf-8 -*-
import requests

# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

from bs4 import BeautifulSoup

import os

def read_all_documents(root):
    labels = []
    docs = []
    for r, dirs, files in os.walk(root):
        for file in files:
            with open(os.path.join(r, file), "r") as f:
                docs.append(f.read())     
            labels.append(r.replace(root, ''))
    return dict([('docs', docs), ('labels', labels)])

data = read_all_documents('training')
documents = data['docs']
labels = data['labels']

print(labels)

import re
from collections import defaultdict

def tokens(doc):
    return (tok.lower() for tok in re.findall(r"\w+", doc))

def frequency(tokens):
    f = defaultdict(int)
    for token in tokens:
        f[token] += 1
    return f

def tokens_frequency(doc):
    return frequency(tokens(doc))

from sklearn.feature_extraction import DictVectorizer, FeatureHasher

vectorizer = DictVectorizer()
vectorizer.fit_transform(tokens_frequency(d) for d in documents)

hasher = FeatureHasher(n_features=2**8, input_type="string")
X = hasher.transform(tokens(d) for d in documents)

print(X.toarray())


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors

prepositions =['a','ante','bajo','cabe','con','contra','de','desde','en','entre','hacia','hasta','para','por','según','sin','so','sobre','tras']
prep_alike = ['durante','mediante','excepto','salvo','incluso','mas','menos']
adverbs = ['no','si','sí']
articles = ['el','la','los','las','un','una','unos','unas','este','esta','estos','estas','aquel','aquella','aquellos','aquellas']
aux_verbs = ['he','has','ha','hemos','habeis','han','había','habías','habiamos','habiais','habian']
tfid = TfidfVectorizer(stop_words=prepositions+prep_alike+adverbs+articles+aux_verbs)

X_train = tfid.fit_transform(documents)
y_train = labels

clf = KNeighborsClassifier(n_neighbors=10)
clf.fit(X_train, y_train)

test = read_all_documents('test')
X_test = tfid.transform(test['docs'])
y_test = test['labels']
pred = clf.predict(X_test)

print('accuracy score %0.3f' % clf.score(X_test, y_test))

def predict_category(url, classifier):
  hrf = url 
  print(hrf)
  url = hrf
  req = requests.get(url, headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  # Scrapy load
  #titulo=soup.find('h1', class_='titulo').getText()
  #print(soup.find('h1', class_='titulo'))
    
  article = 'El proceso de Bankia para devolver el dinero a los pequenos accionistas que suscribieron su salida a Bolsa supone'\
               ' un varapalo a los grandes despachos de abogados que aglutinan miles de demandas contra el banco. Si esos clientes'\
               ' se adhieren a la via extrajudicial y desisten antes de la sentencia, estos bufetes dejaran de ingresar el 100% de'\
               ' las cuantias de una condena en costas y los intereses legales. Por eso, algunos de estos despachos han empezado a'\
               ' esgrimir las clausulas de sus contratos, avisando a sus clientes de que en caso de renunciar a la via judicial'\
               ' deberan abonar igualmente los honorarios'
  #if soup.find('h1', class_='titulo') != None:
  #  titulo=soup.find('h1', class_='titulo').getText()
  #  detalle=soup.find('div', class_='detalle').getText()
  #  post=soup.find('div', class_='cuerpo fullpost__cuerpo').getText()
  #  post = post.encode('utf8')
  #  #post = post.replace('"', '').replace('“', '').replace('”', '')
  #  #titulo = titulo.replace('"', '').replace('“', '').replace('”', '')
  #  #detalle = detalle.replace('"', '').replace('“', '').replace('”', '')
  #  print(detalle)
  #  print(titulo)
  #  article = titulo.encode('utf8')
    
  X_test = tfid.transform([article])
  return clf.predict(X_test)[0]

def show_predicted_categories(urls, classifier):
    for url in urls:
        print('\npredicted category: ' + predict_category(url, clf))
        print('\n')
        print('--------------------------------------------------------------------------------------')

show_predicted_categories(
    [
        'https://thetimes.cl/contenido/6480/curico-unido-volvio-a-los-triunfos-a-costa-del-complicado-deportes-iquique'],
    clf)

