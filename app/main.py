from flask import Flask, request, redirect, render_template, session, url_for
import redis

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Redis 설정
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/')
def index():
    if 'user' in session:
        user = session['user']
        user_score = user + '_score'
        current_score = redis_client.get(user_score) or 0
        return render_template('index.html', user=session['user'], score=int(current_score))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['userId']
        redis_client.set(session['user'], request.form['password'])
        return redirect('/')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/increase_score', methods=['POST'])
def increase_score():
    if 'user' in session:
        user = session['user']
        user_score = user + '_score'
        current_score = redis_client.get(user_score) or 0
        new_score = int(current_score) + 1
        redis_client.set(user_score, new_score)
        return {'score': new_score}
    return redirect(url_for('login'))
