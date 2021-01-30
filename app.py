from salsa import app, HOST, PORT


@app.route('/')
def salsa():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
