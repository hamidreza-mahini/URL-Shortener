from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random
import secrets
from forms import HomeFrm

app = Flask(__name__)
app.secret_key = secrets.token_hex(12)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ulrs_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class URLs(db.Model):
    id_ = db.Column('id_', db.Integer, primary_key=True)
    long_url = db.Column('long_url', db.String())
    short_url = db.Column('short_url', db.String(5))

    def __init__(self, long_url, short_url) -> None:
        self.long_url = long_url
        self.short_url = short_url


def url_shortener(long_url):
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        temp = random.choices(letters, k=5)
        short_url = "".join(temp)
        db_url = URLs.query.filter_by(short_url=short_url).first()
        if not db_url:
            return short_url


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def ep_home():
    form = HomeFrm(request.form)
    if request.method == 'POST' and form.validate():
        req_url = request.form.get('long_url')
        db_url = URLs.query.filter_by(long_url=req_url).first()
        if db_url:
            flash('http://localhost:5000/' + db_url.short_url, category='success')
            return redirect(url_for('ep_home'))
        else:
            short_url = url_shortener(req_url)
            new_url = URLs(req_url, short_url)
            db.session.add(new_url)
            db.session.commit()
            flash('http://localhost:5000/' + new_url.short_url, category='info')
            return redirect(url_for('ep_home'))

    return render_template('home.html', form=form)


@app.route('/all', methods=['GET'])
def ep_all():
    records = URLs.query.all()
    return render_template('all.html', records=records)


@app.route('/<short_url>', methods=['GET'])
def ep_goto_url(short_url):
    db_url = URLs.query.filter_by(short_url=short_url).first()
    if db_url:
        return redirect(db_url.long_url)
    else:
        flash('There is not a valid url for {}'.format(short_url), category='danger')
        return redirect(url_for('ep_home'))


@app.route('/delete/<id>')
def ep_delete(id):
    db_url = URLs.query.filter_by(id_=id).first()
    if db_url:
        db.session.delete(db_url)
        db.session.commit()
        flash('The short_url for {} has been deleted successfully!'.format(db_url.long_url), category='info')
    else:
        flash('There is no record for id = {}!'.format(id), category='danger')
    return redirect(url_for('ep_all'))


@app.route('/about')
def ep_about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
