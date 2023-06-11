from flask import Flask, redirect, url_for, request, session
from flask.templating import render_template
import queries

query = queries.Queries()

app = Flask(__name__)
app.secret_key = 'imdb'


# This is an absolutely terrible way to handle the data as it means genre must always
# need to be the second element in a given result list, however i could not find a better
# way because of needing to use the time for other critical implementations.
def getGenres(lst):
    for x in range(len(lst)):
        g = list(lst[x])
        gval = ''
        gs = g[1]
        while 1:
            start = gs.find(': ""')+4
            stop = gs.find('""}')
            if stop==-1:
                break
            gval += gs[start:stop] + ', '
            gs = gs[stop+4:]
        g[1] = gval[:-2]
        lst[x] = tuple(g)
    return lst

def getGenresingle(gen):
    g = list(gen)
    gval = ''
    gs = g[2]
    while 1:
        start = gs.find(': ""')+4
        stop = gs.find('""}')
        if stop==-1:
            break
        gval += gs[start:stop] + ', '
        gs = gs[stop+4:]
    g[2] = gval[:-2]
    gen = tuple(g)
    return gen




@app.route('/', methods=['GET','POST'])
@app.route("/home", methods=['GET', 'POST']) 
def homepage():
    lst = query.newestMovies()
    lst = getGenres(lst)
    if 'ID' in session:
        id = session['ID']
        lst2 = query.getFavList(id)
        lst3 = query.ratedMovies(id)
        if request.method == 'POST':
            m_id = request.form.get('newmovie')
            fs = request.form.get('favesearch')
            rs = request.form.get('ratesearch')
            if m_id != None:
                session['M'] = m_id
                return redirect(url_for('moviedisplay'))
            if fs != None:
                search = '%' + fs + '%'
                lst2 = query.NsearchFav(search)
            else:
                lst2 = query.getFavList(id)
            if rs != None:
                search = '%' + rs + '%'
                lst3 = query.NsearchRate(search)
                print(lst3)
            else:
                lst3 = query.ratedMovies(id)
        return render_template("home.html", id=id, newm=lst, favm=lst2, ratedm=lst3)
    else:
        if request.method == 'POST':
            m_id = request.form.get('newmovie')
            session['M'] = m_id
            return redirect(url_for('moviedisplay'))
        return render_template("home.html", newm=lst)




@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('nm')
        pword = request.form.get('pw')

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
  return redirect(url_for('homepage'))



@app.route('/profile', methods=['GET','POST'])
def profile():
    id = session['ID']
    if request.method == 'POST':
        inp = request.form.get('del')
        lst = query.lookupUser(id, inp)
        print(id)
        print(inp)
        if lst == []:
            return render_template('profile.html', a=1, id=id)
        else:
            session.pop('ID', None)
            query.deleteUser(id, inp)
            return redirect(url_for('homepage'))
    return render_template('profile.html', id=id)


@app.route('/search', methods=['GET','POST'])
def search():
    if 'ID' in session:
        id = session['ID']
        if request.method == 'POST':
            movSelect = request.form.get('goMovie')
            fav = request.form.get('AddFavorite')
            if fav != None:
                query.insertFavorite(id, fav)
            if movSelect != None:
                session['M'] = movSelect
                return redirect(url_for('moviedisplay'))
            ts = request.form.get('Titlesearch')
            rs = request.form.getlist('rating')
            gs = request.form.getlist('genre')
            if ts != None:
                if len(ts) == 0:
                    ts = ''
                else:
                    ts = '%'+ts+'%'
                if len(rs) == 0:
                    rs = [8]
                if len(gs) == 0:
                    gs = '2'
                else:
                    ngs = '%'
                    for x in range(len(gs)):
                        ngs += gs[x]+'%'
                    gs = ngs
                lst = query.searchMovies(ts, rs, gs)
                lst = getGenres(lst)
                return render_template('search.html', lst=lst, id=id)
            return render_template('search.html', id=id)
        else:
            return render_template('search.html', id=id)
    else:
        if request.method == 'POST':
            movSelect = request.form.get('goMovie')
            if movSelect != None:
                session['M'] = movSelect
                return redirect(url_for('moviedisplay'))
        ts = request.form.get('Titlesearch')
        rs = request.form.getlist('rating')
        gs = request.form.getlist('genre')
        if ts != None:
            if len(ts) == 0:
                ts = ''
            else:
                ts = '%'+ts+'%'
            if len(rs) == 0:
                rs = [8]
            if len(gs) == 0:
                gs = '2'
            else:
                ngs = '%'
                for x in range(len(gs)):
                    ngs += gs[x]+'%'
                gs = ngs
            lst = query.searchMovies(ts, rs, gs)
            lst = getGenres(lst)
            return render_template('search.html', lst=lst)


@app.route('/moviedisplay', methods=['GET','POST'])
def moviedisplay():
    if 'M' in session:
        movie = query.lookupMovie(session['M'])
        movie = getGenresingle(movie)
        avgrating = query.getAvgRating(movie[0])
        ratings = query.getMovieRatings(movie[0])
        if 'ID' in session:
            id = session['ID']
            if request.method == 'POST':
                rate = request.form.get('rate')
                add = request.form.get('addF')
                rem = request.form.get('remF')
                if rate != None:
                    query.insertRating(rate, movie[0], id)
                if add != None:
                    query.insertFavorite(id, movie[0])
                if rem != None:
                    query.deleteFavorite(id, movie[0])
            isfavorite = query.checkFavorite(id, movie[0])
            avgrating = query.getAvgRating(movie[0])
            ratings = query.getMovieRatings(movie[0])
            if isfavorite != None:
                return render_template('moviedisplay.html', movie=movie, avgR=avgrating[0], R=ratings, id=id, F=isfavorite)
            else:
                return render_template('moviedisplay.html', movie=movie, avgR=avgrating[0], R=ratings, id=id)
        return render_template('moviedisplay.html', movie=movie, avgR=avgrating[0], R=ratings)
    else:
        #Should never happen
        return render_template('moviedisplay.html')




app.run(debug=True)

