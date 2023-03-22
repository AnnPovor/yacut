import random
from http import HTTPStatus
from string import ascii_letters, digits

from flask import flash, redirect, render_template, url_for

from yacut.forms import URLMapForm
from yacut.models import URLMap

from . import app, db


def get_unique_short_id():
    while True:
        letters_digits = ascii_letters + digits
        uniq_url = ''.join(random.choices(letters_digits, k=6))
        if not URLMap.query.filter_by(short=uniq_url).first():
            return uniq_url


def check_unique_short_url(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('main.html', form=form)

    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()

    if check_unique_short_url(custom_id) is not None:
        flash(f'Имя {custom_id} уже занято!', 'rejected1')
        return render_template('main.html', form=form)

    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    flash(
        url_for('forwarding', short=custom_id, _external=True), 'complete_link')
    return render_template('main.html', url_map=url_map, form=form)


@app.route('/<string:short>')
def forwarding(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original, code=HTTPStatus.FOUND)
