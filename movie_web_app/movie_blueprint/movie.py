from flask import Blueprint, render_template, url_for, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
import movie_web_app.adapters.repository as repo
from movie_web_app.authentication.authentication import login_required
from flask import request

movie_blueprint = Blueprint(
    'movie_bp', __name__
)


class SearchForm(FlaskForm):
    movie_title = StringField('Movie title')
    director_name = StringField('Director name')
    actor_name = StringField('Actor name')
    genre_name = StringField('Genre name')
    year = IntegerField('Year')
    rating = IntegerField('Rating')
    review_text = StringField('Review text')
    submit = SubmitField('Find')


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter, \
            a lower case letter and a digit'
            self.message = message

        def __call__(self, form, field):
            schema = PasswordValidator()
            schema \
                .min(8) \
                .has().uppercase() \
                .has().lowercase() \
                .has().digits()
            if not schema.validate(field.data):
                raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


@movie_blueprint.route('/')
def home():
    return render_template(
        'home.html'
    )


@movie_blueprint.route('/list/number=<number>')
def list_movies(number):
    list = []
    for i in range(0, 100):
        try:
            list.append(repo.repo_instance.dataset_of_movies[i+100*int(number)])
        except IndexError:
            pass
    return render_template(
        'list_browse_movies.html',
        movies=list,
        current_number=int(number)
    )


@movie_blueprint.route('/find_movie_title', methods=['GET', 'POST'])
def find_movie_title():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_movie_title(form.movie_title.data)
        return render_template(
            'list_movies.html',
            movies=movie
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.find_movie_title'),
            form=form,
            search_type='movie_title'
        )


@movie_blueprint.route('/find_movie_director', methods=['GET', 'POST'])
def find_movie_director():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_director_name(form.director_name.data)
        return render_template(
            'list_movies.html',
            movies=movie
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.find_movie_director'),
            form=form,
            search_type='director_name'
        )


@movie_blueprint.route('/find_movie_actor', methods=['GET', 'POST'])
def find_movie_actor():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_actor_name(form.actor_name.data)
        return render_template(
            'list_movies.html',
            movies=movie
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.find_movie_actor'),
            form=form,
            search_type='actor_name'
        )


@movie_blueprint.route('/find_movie_genre', methods=['GET', 'POST'])
def find_movie_genre():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_genre_name(form.genre_name.data)
        return render_template(
            'list_movies.html',
            movies=movie
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.find_movie_genre'),
            form=form,
            search_type='genre_name'
        )


@movie_blueprint.route('/watch_list', methods=['GET'])
@login_required
def watch_list():
    return render_template(
        'list_watchlist.html',
        time=repo.repo_instance.get_user(session['username']).time_spent_watching_movies_minutes,
        movies=repo.repo_instance.get_user(session['username']).get_watch_list()
    )


@movie_blueprint.route('/add_watch_list', methods=['GET', 'Post'])
@login_required
def add_watch_list():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_exact_movie(form.movie_title.data, form.year.data)
        if movie is not None:
            repo.repo_instance.get_user(session['username']).get_watch_list().add_movie(movie)
        return render_template(
            'list_watchlist.html',
            time=repo.repo_instance.get_user(session['username']).time_spent_watching_movies_minutes,
            movies=repo.repo_instance.get_user(session['username']).get_watch_list()
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.add_watch_list'),
            form=form,
            search_type='movie_title_year'
        )


@movie_blueprint.route('/watchlist_remove/title=<title>&year=<year>', methods=['GET'])
@login_required
def watchlist_remove(title, year):
    movie = repo.repo_instance.get_exact_movie(str(title), int(year))
    repo.repo_instance.get_user(session['username']).add_runtime(movie.runtime_minutes)
    repo.repo_instance.get_user(session['username']).get_watch_list().remove_movie(movie)
    return render_template(
        'list_watchlist.html',
        time=repo.repo_instance.get_user(session['username']).time_spent_watching_movies_minutes,
        movies=repo.repo_instance.get_user(session['username']).get_watch_list()
    )


@movie_blueprint.route('/list_reviews', methods=['GET'])
def list_reviews():
    return render_template(
        'list_reviews.html',
        reviews=repo.repo_instance.get_reviews()
    )


@movie_blueprint.route('/add_reviews', methods=['GET', 'POST'])
@login_required
def add_reviews():
    form = SearchForm()
    if form.validate_on_submit():
        movie = repo.repo_instance.get_exact_movie(form.movie_title.data, form.year.data)
        if movie is not None:
            repo.repo_instance.add_review(form.movie_title.data, form.review_text.data, form.rating.data, session['username'])
        return render_template(
            'list_reviews.html',
            reviews=repo.repo_instance.get_reviews()
        )
    else:
        return render_template(
            'find_movie.html',
            handler_url=url_for('movie_bp.add_reviews'),
            form=form,
            search_type='add_review'
        )


@movie_blueprint.route('/list_one_movie/title=<title>&year=<year>', methods=['GET', 'POST'])
def list_one_movie(title, year):
    return render_template(
        'list_one_movie.html',
        movie=repo.repo_instance.get_exact_movie(str(title), int(year))
    )
