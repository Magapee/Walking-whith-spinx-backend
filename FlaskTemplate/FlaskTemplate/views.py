from FlaskTemplate import app
from flask import jsonify, request

@app.route('/', methods=['GET', 'POST'])
#@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    data = request.get_json()
    #app.logger.debug("Вывод: " + str(request.args.get('fio')))
    return jsonify(data)

