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
        print(uname)
        print(pword)

        if (request.form.get('logon') == 'Sign up' and uname != "" and pword != ""):
            match query.addUser(uname, pword):
                case 0:
                    return render_template("login.html", a=1)
                case 1:
                    session['ID'] = uname
                    return redirect(url_for('homepage'))
        elif (request.form.get('login') == 'Sign in' and uname != "" and pword != ""):
            lst = query.lookupUser(uname, pword)
            match len(lst):
                case 0:
                    return render_template('login.html', b=1)
                case 1:
                    session['ID'] = uname
                    return redirect(url_for('homepage'))
        else:
            return render_template("login.html", c=1)
    else:    
        return render_template("login.html")


@app.route('/logout')
def logout():
  session.pop('ID',None)
  return render_template('home.html')



# app.run(debug=True)
query.ResetDB()
