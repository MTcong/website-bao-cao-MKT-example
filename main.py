from website import create_app

app = create_app()

if __name__ == '__main__':
    # context = ('/etc/letsencrypt/live/gumilacmkt.website/fullchain.pem', '/etc/letsencrypt/live/gumilacmkt.website/privkey.pem')
    # app.run(host='0.0.0.0', port=443, ssl_context=context)
    app.run(debug=True)