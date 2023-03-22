from re import match
from urllib import request

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id

CHECK_OUT = r'^[a-z]+://[^\/\?:]+(:[0-9]+)?(\/.*?)?(\?.*)?$'
REGULAR_EXPRESSION = '^[a-zA-Z0-9_]*$'
LEN = 16


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if not match(CHECK_OUT, data['url']):
        raise InvalidAPIUsage('Url не подходит.')

    custom_id = data.get('custom_id')

    if 'custom_id' not in data or custom_id is None:
        data['custom_id'] = get_unique_short_id()

    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

        if not match(REGULAR_EXPRESSION, custom_id) or len(custom_id) > LEN:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
