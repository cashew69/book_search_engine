from flask import Flask, render_template, jsonify, request, make_response, send_from_directory

from listoftitles import data
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

import sqlite3

DATABASE = '/media/cashew/ac0c66a0-9267-41b6-a5a0-ddd0d5fca487/PROJECTS/Serious/indexofbooks/code/db'

def get_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.error as e:
        print(e)
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')
    #return jsonify('x')


@app.route('/search', methods=["GET","POST"])
def string():
    if request.method == 'POST':
        tit = request.get_json()['searchTerm']
        temp = []
        for word in enumerate(data):
            if tit.lower() in str(word[1]).lower():
                temp.append(word)
        print(tit)
        return make_response(jsonify(temp), 200)
    else:
        return None

books = {
    0: "book 1",
    2: "book 2",
    3: "book 3",
}
@app.route('/book_id=<book_id>')
def get_book(book_id):
    db = get_db().cursor()
    book_id=str(book_id)
    maininfo = db.execute('SELECT field1, title, author, description, language, publisher, publishDate, coverImg FROM split_dataset WHERE field1 ='+book_id)
    
    for row in maininfo:
        bookinfo = {
            'index' : str(row[0]),
            'title' : str(row[1]),
            'author' : str(row[2]),
            'description' : str(row[3]),
            'language' : str(row[4]),
            'publisher' : str(row[5]),
            'publishdate' : str(row[6]),
            'coverimg' : str(row[7]),
        }

    similarinfo = db.execute('SELECT * FROM data2 WHERE field1 ='+book_id)
    similarinfo = similarinfo.fetchall()
    similarinfo = list(similarinfo[0])
    similarinfo = similarinfo[0:6]
    #print(similarinfo)
    
    for bidx in range(1, 6):

        sim = db.execute('SELECT title, coverImg FROM split_dataset WHERE field1='+str(similarinfo[bidx]))
        sim = sim.fetchall()
        sim = list(sim[0])
        bookinfo['similar_book'+str(bidx)] = {
            'simid': str(similarinfo[bidx]),
            'title': str(sim[0]), 
            'coverimg' : str(sim[1]),
                }
    return render_template('book_info.html', bookinfo=bookinfo)

