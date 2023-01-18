# Module imports
from flask import Flask, render_template, request, redirect, abort
from pyndb import PYNDatabase
from os import urandom


# Constants
PORT = 8383


# Object inits
config = PYNDatabase('config.json')
app = Flask(__name__)


# Flask routes
@app.route('/')
@app.route('/<path:path>')
def index(*args, sub="default", host="default", path=None):
    # path = args[0] if len(args) > 0 else "/"
    path = "/" + path if path else ""
    base = request.base_url.rsplit('/', maxsplit=1)[0].split('://', maxsplit=1)[1]
    base = base.rsplit('.', maxsplit=2)
    if len(base) >= 3:
        name = base[1]
        tld = base[2]
        domain_name = name + '.' + tld
        subdomain = base[0]
        try:
            location = config.get(domain_name, ignore_dots=True).get(subdomain).val
        except AttributeError:
            try:
                if config.get(domain_name, ignore_dots=True).has('*'):
                    location = config.get(domain_name, ignore_dots=True).get('*').val
                else:
                    abort(404)
            except AttributeError:
                abort(404)
        return redirect(location + path)
    else:
        name = base[0]
        tld = base[1]
        domain_name = name + '.' + tld
        try:
            location = config.get(domain_name, ignore_dots=True).get('@').val
        except AttributeError:
            try:
                if config.get(domain_name, ignore_dots=True).has('*'):
                    location = config.get(domain_name, ignore_dots=True).get('*').val
                else:
                    abort(404)
            except AttributeError:
                abort(404)
        return redirect(location + path)

@app.errorhandler(404)
def not_found(error):
    print(request.base_url)
    return render_template('doesnt_exist.html')

@app.route('/favicon.ico')
def favicon():
    abort(404)


# Run
if __name__ == '__main__':
    app.secret_key = urandom(15)
    app.run(host='0.0.0.0', port=PORT)
