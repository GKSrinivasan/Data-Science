# coding: utf-8
import os
import pandas
import shutil
import tom_lib.utils as utils
from flask import Flask, render_template, make_response
from tom_lib.nlp.topic_model import NonNegativeMatrixFactorization
from tom_lib.nlp.topic_model import LatentDirichletAllocation
from tom_lib.nlp.topic_model import TruncatedSVD
from tom_lib.structure.corpus import Corpus
import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pickle
from tom_lib.visualization.visualization import Visualization

from sklearn.decomposition import LatentDirichletAllocation as LDA

from nltk.corpus import stopwords
import pdfkit
from xhtml2pdf import pisa
#from cStringIO import StringIO
from io import BytesIO

def create_pdf(pdf_data):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(pdf_data.encode('utf-8')), pdf)
    return pdf


__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

# Flask Web server
app = Flask(__name__, static_folder='browser/static', template_folder='browser/templates')

# Parameters
max_tf = 0.5
min_tf = 4
num_topics = 30
vectorization = 'tfidf'

# Load corpus
#corpus = Corpus(source_file_path='input/egc_lemmatized_.csv',

#corpus = Corpus(source_file_path='input/amazon_eng.csv',
corpus = Corpus(source_file_path='input/egc_lemmatized_.csv',
                language='english',
                vectorization=vectorization,
                max_relative_frequency=max_tf,
                min_absolute_frequency=min_tf)
print('corpus size:', corpus.size)
print('vocabulary size:', len(corpus.vocabulary))

# Infer topics
topic_model = NonNegativeMatrixFactorization(corpus=corpus)
#topic_model = LatentDirichletAllocation(corpus=corpus)
#topic_model = TruncatedSVD(corpus=corpus)
"""viz = Visualization(topic_model)
viz.plot_greene_metric(min_num_topics=15, 
                       max_num_topics=50, 
                       tao=10, step=1, 
                       top_n_words=10)
viz.plot_arun_metric(min_num_topics=15, 
                     max_num_topics=50, 
                     iterations=10)
viz.plot_brunet_metric(min_num_topics=15, 
                       max_num_topics=50,
                       iterations=10)
"""
utils.save_topic_model(topic_model, 'output/NMF_15topics.tom')
topic_model = utils.load_topic_model('output/NMF_15topics.tom')


topic_model.infer_topics(num_topics=num_topics)
topic_model.print_topics(num_words=30)

# Clean the data directory
if os.path.exists('browser/static/data'):
    shutil.rmtree('browser/static/data')
os.makedirs('browser/static/data')

# Export topic cloud
utils.save_topic_cloud(topic_model, 'browser/static/data/topic_cloud.json')

# Export details about topics
for topic_id in range(topic_model.nb_topics):
    utils.save_word_distribution(topic_model.top_words(topic_id, 50),
                                 'browser/static/data/word_distribution' + str(topic_id) + '.tsv')
    utils.save_affiliation_repartition(topic_model.affiliation_repartition(topic_id),
                                       'browser/static/data/affiliation_repartition' + str(topic_id) + '.tsv')
    evolution = []
    for i in range(2012, 2016):
        evolution.append((i, topic_model.topic_frequency(topic_id, date=i)))
    utils.save_topic_evolution(evolution, 'browser/static/data/frequency' + str(topic_id) + '.tsv')

# Export details about documents
for doc_id in range(topic_model.corpus.size):
    utils.save_topic_distribution(topic_model.topic_distribution_for_document(doc_id),
                                  'browser/static/data/topic_distribution_d' + str(doc_id) + '.tsv')

# Export details about words
for word_id in range(len(topic_model.corpus.vocabulary)):
    utils.save_topic_distribution(topic_model.topic_distribution_for_word(word_id),
                                  'browser/static/data/topic_distribution_w' + str(word_id) + '.tsv')

# Associate documents with topics
topic_associations = topic_model.documents_per_topic()

# Export per-topic author network
#for topic_id in range(topic_model.nb_topics):
#    utils.save_json_object(corpus.collaboration_network(topic_associations[topic_id]),
#                           'browser/static/data/author_network' + str(topic_id) + '.json')


@app.route('/')
def index():
    return render_template('index.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size),
                           method=type(topic_model).__name__,
                           corpus_size=corpus.size,
                           vocabulary_size=len(corpus.vocabulary),
                           max_tf=max_tf,
                           min_tf=min_tf,
                           vectorization=vectorization,
                           num_topics=num_topics)


import mimerender

mimerender.register_mime('pdf', ('application/pdf',))
mimerender = mimerender.FlaskMimeRender(global_charset='UTF-8')

def render_pdf(html):
    from xhtml2pdf import pisa
    from cStringIO import StringIO
    pdf = StringIO()
    pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=export.pdf'
    pdf.close()
    return response




@app.route('/topic_cloud.html')
@mimerender(default='html', html=lambda html: html, pdf=render_pdf, override_input_key='format')

def topic_cloud():
    nmf = joblib.load('nmfModel.pkl')
    vectorizer = joblib.load('vectorizer.bin')

    text = "John The Logi Circle 2 arrived and set up perfectly. Thank you for the technical support. David > On Mar 29 2018 at 3:56 PM customercare@logitech.com wrote: > > > > > > <http://support.logitech.com/> > > Hi David > > > This is John and I am reaching out to inform you that your RMA has shipped! As I believe you should be good to go now I?m going to go ahead and close this case but if you have any issues or questions moving forward please reply to this email and your case will be reopened immediately. You may also receive a survey based on our interactions and I would appreciate it if you filled that out. > Thank you! > > Best regards > > John > Circle Crew > Circle 2 Support <http://www.logitech.com/circle2/support> > Circle Support <http://www.logitech.com/support/circle> > > > Security Made Simple. #CircleIt <> > > > >"
    x = nmf.transform(vectorizer.transform([text]))[0]
    print(x, x.sum())

    print("----------------------------------")



    # create a blank model
    lda = LDA()

    # load parameters from file
    with open ('outfile', 'rb') as fd:
        (features,lda.components_,lda.exp_dirichlet_component_,lda.doc_topic_prior_) = pickle.load(fd)

    # the dataset to predict on (first two samples were also in the training set so one can compare)
    data_samples = ["connect bluetooth connectivity","battery","camera"]
    # Vectorize the training set using the model features as vocabulary
    tf_vectorizer = TfidfVectorizer(vocabulary=features, ngram_range=(1, 1),
                                         max_df=max_tf,
                                         min_df=min_tf,
                                         max_features=3000,
                                         stop_words=stopwords.words("english"))
    tf = tf_vectorizer.fit_transform(data_samples)

    # transform method returns a matrix with one line per document, columns being topics weight
    predict = lda.transform(tf)
    print(predict)

    
    pdf = create_pdf(render_template('topic_cloud.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size)))
    #response = make_response(pdf)
    #response.headers['Content-Type'] = 'application/pdf'
    #response.heders['Content-Disposition'] = 'inline; filename=output.pdf'
    html = render_template('topic_cloud.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size))

    return { 'html': html }

    #return render_template('topic_cloud.html',
    #                       topic_ids=range(topic_model.nb_topics),
    #                       doc_ids=range(corpus.size))



@app.route('/vocabulary.html')
def vocabulary():

    word_list = []
    for i in range(len(corpus.vocabulary)):
        word_list.append((i, corpus.word_for_id(i)))
    splitted_vocabulary = []
    words_per_column = int(len(corpus.vocabulary)/5)
    for j in range(5):
        sub_vocabulary = []
        for l in range(j*words_per_column, (j+1)*words_per_column):
            sub_vocabulary.append(word_list[l])
        splitted_vocabulary.append(sub_vocabulary)
    return render_template('vocabulary.html',
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size),
                           splitted_vocabulary=splitted_vocabulary,
                           vocabulary_size=len(word_list))


@app.route('/topic/<tid>.html')
def topic_details(tid):
    ids = topic_associations[int(tid)]
    documents = []
    title_count = []
  

    for document_id in ids:
        documents.append((corpus.title(document_id),
                          ', '.join(corpus.author(document_id)),
                          corpus.date(document_id), document_id))
    import pandas as pd

    labels = ['document_id', 'description', 'date','doc']
    df = pd.DataFrame.from_records(documents, columns=labels)
    print(df.head())
    print(df.document_id.value_counts())
    df.document_id.value_counts().values.tolist()
    s = df.document_id.value_counts()
    for i, v in s.iteritems():
      title_count.append((i,v))

    return render_template('topic.html',
                           topic_id=tid,
                           frequency=round(topic_model.topic_frequency(int(tid))*100, 2),
                           documents=documents,
                           title_count=title_count,
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size))


@app.route('/document/<did>.html')
def document_details(did):
    vector = topic_model.corpus.vector_for_document(int(did))
    word_list = []
    for a_word_id in range(len(vector)):
        word_list.append((corpus.word_for_id(a_word_id), round(vector[a_word_id], 3), a_word_id))
    word_list.sort(key=lambda x: x[1])
    word_list.reverse()
    documents = []
    for another_doc in corpus.similar_documents(int(did), 5):
        documents.append((corpus.title(another_doc[0]).capitalize(),
                          ', '.join(corpus.author(another_doc[0])),
                          corpus.date(another_doc[0]), another_doc[0], round(another_doc[1], 3)))
    return render_template('document.html',
                           doc_id=did,
                           words=word_list[:21],
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size),
                           documents=documents,
                           authors=', '.join(corpus.author(int(did))),
                           year=corpus.date(int(did)),
                           short_content=corpus.title(int(did)))


@app.route('/word/<wid>.html')
def word_details(wid):
    documents = []
    for document_id in corpus.docs_for_word(int(wid)):
        documents.append((corpus.title(document_id),
                          ', '.join(corpus.author(document_id)),
                          corpus.date(document_id), document_id))
    return render_template('word.html',
                           word_id=wid,
                           word=topic_model.corpus.word_for_id(int(wid)),
                           topic_ids=range(topic_model.nb_topics),
                           doc_ids=range(corpus.size),
                           documents=documents)

@app.route('/predicts', methods=['POST'])
def predicts():
    clf = joblib.load('nmfModel.pkl')
    prediction = clf.predict("hi my mouse is having issue in connectivity")
    print(jsonify({'prediction': list(prediction)}))
    return jsonify({'prediction': list(prediction)})
    


if __name__ == '__main__':
    # Access the browser at http://localhost:2016/
    app.run(debug=True, host='0.0.0.0', port=8009)
