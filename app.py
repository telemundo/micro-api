'''
@author: Rodolfo Puig <Rodolfo.Puig@nbcuni.com>
@copyright: Telemundo Digital Media
@organization: NBCUniversal
'''

from flask import Flask, request, abort, url_for, render_template, make_response
from os import path, unlink
from datetime import date
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['srt'])
UPLOAD_FOLDER      = '/tmp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

runtime = Flask(__name__)
runtime.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@runtime.route('/')
def index():
    return 'Hi!'

@runtime.route('/ttml')
def ttml_index():
    return render_template('ttml/form.html', url=url_for('ttml_parse'))

@runtime.route('/ttml/parse', methods=['POST'])
def ttml_parse():
    upload = request.files['file']
    try:
        language = request.form['lang']
    except KeyError:
        language = 'es'
    ''' validate upload '''
    if file and allowed_file(upload.filename):
        filename = secure_filename(upload.filename)
        filepath = path.join(runtime.config['UPLOAD_FOLDER'], filename)
        upload.save(filepath)
        ''' process captions '''
        captions = []
        ''' create response '''
        response = make_response(render_template('ttml/result.xml', language=language, year=date.today().year, captions=captions))
        response.mimetype = 'text/xml'
        unlink(filepath)

        return response
    else:
        abort(403)