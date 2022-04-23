import json
import os

from flask import request, jsonify, current_app, render_template

from transcript.app.views import app
from transcript.utils import write_config_json, read_config_json


@app.route('/settings', methods=['GET', 'POST', 'PUT'])
def settings():
    if request.method == 'GET' and request.args.get('params'):
        return jsonify(read_config_json(current_app.config['SETTING_PATH']))
    if request.method == 'PUT':
        try:
            inst = request.json
            if not inst:
                return jsonify(status=0), 400
            return jsonify(
                write_config_json(current_app.config['SETTING_PATH'], json.dumps(inst)))
        except Exception as e:
            return jsonify(status=0), 500
    return render_template('app/settings.html', title='Settings')
