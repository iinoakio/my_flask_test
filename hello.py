from flask import Flask
from flask import request
from flask import current_app
from flask import redirect
from flask import session
from flask import render_template
from flask import url_for
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email

class NameForm(FlaskForm):
    name = StringField("What is your name ?", validators=[DataRequired()])
    email = EmailField("Please enter the email", validators=[DataRequired(), Email()])
    submit = SubmitField("送信")

app = Flask(__name__)
app.config['SECRET_KEY'] = "Canon-012"

@app.route("/", methods=["GET", "POST"])
def test_index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name and old_name != form.name.data:
            flash("名前を変えましたね！")
        session['name'] = form.name.data
        return redirect(url_for("test_index"))
    return render_template("index.html", form = form, name = session.get("name"))


    # user_agent = request.headers.get("User-Agent")
    # return f"<h1> Current App is '{current_app.name}' ---- Your browser is '{user_agent}' Hello World in Flask test program </h1>"

@app.route("/jinja_globals")
def jinja_globals():
    return "<pre>" + "\n".join(sorted(app.jinja_env.globals.keys())) + "</pre>"

@app.route("/user/<name>")
def test_user(name):
    return render_template("user.html", user = name)
    # return f"<h1> Welcome, {name} in Flask test program </h1>"

from markupsafe import escape
@app.route("/map")
@app.route("/show_map", endpoint="show_map")
def test_map():
    return f"<pre>{escape(app.url_map)}</pre>"

@app.route("/rule", endpoint="show_rule")
def test_rule():
    lines = []
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        endpoint = rule.endpoint
        view_func = app.view_functions.get(endpoint)
        view_name = getattr(view_func, "__name__", str(view_func))

        lines.append(
            f"'{rule.rule}',\n"
            f"endpoint='{endpoint}',\n"
            f"view_func={view_name}\n"
        )

    text = "\n".join(lines)
    return f"<pre>{escape(text)}</pre>"


@app.route("/error")
def test_error():
    return f"<h1> Bad request</h1>", 400

@app.route("/redirect")
def test_redirect():
    return redirect("https://www.nikkei.com")



if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
