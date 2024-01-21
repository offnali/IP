from website import create_app

UPLOAD_FOLDER = 'uploads'

app = create_app()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(debug=True)