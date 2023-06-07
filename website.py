from flask import Flask, redirect, url_for, request, session
from flask.templating import render_template
import queries

query = queries.Queries()

app = Flask(__name__)
app.secret_key = 'imdb'

@app.route('/', methods=['GET','POST'])
@app.route("/home", methods=['GET', 'POST'])
def homepage():
    if 'ID' in session:
        id = session['ID']
        return render_template("home.html", id=id)
    else:
        return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('nm')
        pword = request.form.get('pw')

        if (request.form.get('logon') == 'Sign up' and uname != None and pword != None):
            match query.addUser(uname, pword):
                case 0:
                    print('Username already taken')
                    return render_template("login.html")
                case 1:
                    print('New user added')
                    return redirect(url_for('homepage'))
        elif (request.form.get('login') == 'Sign in' and uname != None and pword != None):
            print('A user wants to log in')
            lst = query.lookupUser(uname, pword)
            match len(lst):
                case 0:
                    print('Could not find, username or password incorrect')
                    return render_template('login.html')
                case 1:
                    session['ID'] = uname
                    return redirect(url_for('homepage'))
        else:
            print('Username or password not given')
            return render_template("login.html")
    else:    
        return render_template("login.html")


@app.route('/logout')
def logout():
  session.pop('ID',None)
  return render_template('home.html')



app.run(debug=True)
# query.ResetDB()
