from flask import redirect, url_for


def add_routes(app):
    @app.route("/portfolio/", methods=["GET"])
    def portfolio():
        return redirect(url_for('hello_world'))
    @app.route("/about/", methods=["GET"])
    def about():
        return redirect(url_for('hello_world'))
    @app.route("/contact/", methods=["GET"])
    def contact():
        return redirect(url_for('hello_world'))
    
    return app