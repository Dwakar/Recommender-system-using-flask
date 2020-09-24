import flask
from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = flask.Flask(__name__, template_folder='templates')
class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Anish', password='anish'))
users.append(User(id=2, username='Manish', password='manish'))
app = Flask(__name__)
app.secret_key = '#!@#'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


df2 = pd.read_csv('./model/content.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['brand'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['title'].iloc[movie_indices]
    dat = df2['categories'].iloc[movie_indices]
    return_df = pd.DataFrame(columns=['Title','categories'])
    return_df['Title'] = tit
    return_df['categories'] = dat
    return return_df

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('profile.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            result_final = get_recommendations(m_name)
            names = []
            cat = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                cat.append(result_final.iloc[i][1])

            return flask.render_template('positive.html',movie_names=names,movie_cat=cat,search_name=m_name)
@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return render_template('protected.html')
   
if __name__ == '__main__':
    app.run()