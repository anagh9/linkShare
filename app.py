# app.py
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

DATABASE = 'links.db'

app = Flask(__name__)
app.config['DATABASE'] = DATABASE

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database from the schema file."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    """Main page, displays all the links."""
    db = get_db()
    links = db.execute('SELECT * FROM links ORDER BY id DESC').fetchall()
    return render_template('index.html', links=links)

@app.route('/api/delete/<int:link_id>', methods=['POST'])
def delete_link(link_id):
    """API endpoint to delete a link by its ID."""
    db = get_db()
    db.execute('DELETE FROM links WHERE id = ?', (link_id,))
    db.commit()
    return '', 204

@app.route('/add', methods=('GET', 'POST'))
def add():
    """Page to add a new link."""
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']

        if name and url: # Basic validation
            db = get_db()
            db.execute('INSERT INTO links (name, url) VALUES (?, ?)', (name, url))
            db.commit()
            return redirect(url_for('index'))
            
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
