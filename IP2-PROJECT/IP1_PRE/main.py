from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        port=443, 
        debug=True,
        ssl_context=('website/sslkeys/cert.pem', 'website/sslkeys/key.pem')
    )
