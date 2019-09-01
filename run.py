from image_library import create_app, db_setup


app = create_app()
app.app_context().push()

if __name__ == '__main__':
    # db_setup.init_db()
    app.run(debug=True)
