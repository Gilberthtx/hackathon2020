from flask import Flask, render_template, redirect, g, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from flask_bcrypt import check_password_hash
import forms
import functions
import models
import airports.airportScraper

app = Flask(__name__)
app.secret_key = 'asdjkansd1n3m1kldmaskdmasdlkas'


'''LOGIN'''

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    # connect to the database before each request
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    # close the database connection after each request
    g.db.close()
    return response


'''REGISTER PAGE'''


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('account'))
    return render_template('register.html', form=form)


'''LOGIN PAGE'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in!", "success")
                return redirect(url_for('account'))
            else:
                flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)


'''MAIN PAGE / SEARCH PAGE'''


@app.route('/', methods=['GET', 'POST'])
def search():
    # form
    form = forms.FlightSearchForm()

    # validate form
    if form.validate_on_submit():
        date_selected = form.form_date.data.replace('/', '')
        from_selected = form.form_origin.data
        to_selected = form.form_destination.data
        return redirect(url_for(
            'flights',
            date=date_selected,
            origin=from_selected,
            destination=to_selected
        ))

    # render template with variables needed in html
    return render_template(
        'search.html',
        form=form,
        flight_symbols=airports.airportScraper.symbol_list,
        airports=airports.airportScraper.airport_list,
        length=airports.airportScraper.num_of_airports

    )


'''FLIGHTS PAGE'''


@app.route('/<date>/<origin>/<destination>', methods=['GET', 'POST'])
def flights(date, origin, destination):
    temp = str(date[0:2]) + '-' + str(date[2:4]) + '-' + str(date[4:8])
    # fix date
    date = str(date[4:8]) + '-' + str(date[0:2]) + '-' + str(date[2:4])
    # get data
    flight_data = functions.flights_search(date, origin, destination)

    # render template with variables needed in html
    return render_template(
        'flights.html',
        flight_data=flight_data,
        date=temp
    )


'''ADD FLIGHT'''


@app.route('/<flight>/<date>/<origin>/<destination>/<arrival>/<departure>', methods=['GET', 'POST'])
@login_required
def add_flight(flight, date, origin, destination, arrival, departure):
    # add flight to account
    models.Flight.create(
        user=g.user.id,
        origin=origin,
        destination=destination,
        date=date,
        arrival_time=arrival,
        departure_time=departure,
        flight_number=flight
    )
    return redirect(url_for('account'))


'''REMOVE FLIGHT'''


@app.route('/remove/<flight>', methods=['GET', 'POST'])
@login_required
def remove_flight(flight):
    # find symbol in users watchlist but expect it not to be found
    try:
        models.Flight.get(
            flight_number=flight
        ).delete_instance()
    except models.IntegrityError:
        pass
    return redirect(url_for('account'))


'''FOOD ORDERING'''


@app.route('/food')
@login_required
def store():
    # render template with variables needed in html
    return render_template(
        'store.html'
    )


''' ACCOUNT PAGE'''


@app.route('/account')
@login_required
def account():
    # get all stocks in watchlist
    stream = current_user.get_flights()

    # render template with variables needed in html
    return render_template(
        'account.html',
        stream=stream,
        name=g.user.name
    )


'''RUN PROGRAM'''


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            name='Evelio',
            email='eveliososa123@gmail.com',
            password='password'
        )
    except ValueError:
        pass
    app.run(debug=True)  # debug is set because of testing phase
