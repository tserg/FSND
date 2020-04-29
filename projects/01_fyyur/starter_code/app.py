#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, CsrfProtect
from forms import *
from flask_migrate import Migrate
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

csrf = CsrfProtect()

csrf.init_app(app)

db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    def _create_individual_venue_dict(self):

      """
        Helper function for venues()
      """
      temp_dict = {
        'id': self.id,
        'name': self.name,
        'num_upcoming_shows': 0

      }

      return temp_dict

class Artist(db.Model):
    __tablename__ = 'Artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    shows = db.relationship('Show', backref='artist', lazy=True)

    def _create_individual_artist_dict(self):

      """
        Helper function for artists()
      """
      temp_dict = {
        'id': self.id,
        'name': self.name
      }

      return temp_dict


class Show(db.Model):
  __tablename__ = 'Shows' 

  venue_id =  db.Column(db.Integer, db.ForeignKey('Venues.id'), primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artists.id'), primary_key=True)
  start_time = db.Column(db.DateTime(), primary_key=True)

  def _create_individual_show_dict(self):
    """
      Helper function for shows()
    """

    temp_dict = {
      'venue_id': self.venue_id,
      'venue_name': self.venue.name,
      'artist_id': self.artist_id,
      'artist_name': self.artist.name,
      'artist_image_link': self.artist.image_link,
      'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S")
    }


    return temp_dict

  def _create_individual_show_dict_2(self):

    """
      Helper function for show_venue()

    """

    temp_dict = {
      'artist_id': self.artist_id,
      'artist_name': self.artist.name,
      'artist_image_link': self.artist.image_link,
      'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S")
      
    
    }

    return temp_dict

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data = []

  areas = Venue.query.distinct('city', 'state').all()

  for area in areas: 

    venues = Venue.query.filter(Venue.city == area.city,
      Venue.state == area.state).all()

    venue_dict = []

    for venue in venues:
      venue_dict.append(venue._create_individual_venue_dict())

    temp = {
      'city': area.city,
      'state': area.state,
      'venues': venue_dict
    }

    data.append(temp)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  current_venue = Venue.query.get(venue_id)

  past_shows = Show.query.filter_by(venue_id = venue_id).filter(Show.start_time < datetime.datetime.now()).all()
  upcoming_shows = Show.query.filter_by(venue_id = venue_id).filter(Show.start_time >= datetime.datetime.now()).all()

  past_shows_data = []
  upcoming_shows_data = []

  for show in past_shows:

    past_shows_data.append(show._create_individual_show_dict_2())

  for show in upcoming_shows:
    upcoming_shows_data.append(show._create_individual_show_dict_2())

  data = {
    'id': current_venue.id,
    'name': current_venue.name,
    'genres': current_venue.genres,
    'address': current_venue.address,
    'city': current_venue.city,
    'state': current_venue.state,
    'phone': current_venue.phone,
    'website': current_venue.website,
    'facebook_link': current_venue.facebook_link,
    'seeking_talent': current_venue.seeking_talent,
    'seeking_description': current_venue.seeking_description,
    'image_link': current_venue.image_link,
    'past_shows':past_shows_data,
    'upcoming_shows': upcoming_shows_data,
    'past_shows_count': len(past_shows_data),
    'upcoming_shows_count': len(upcoming_shows_data)

  }


  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)

  try:

# on successful db insert, flash success
    if form.validate():

      if form.seeking_talent.data is False:
        seeking_description = ''
      else:
        seeking_description = form.seeking_description

      new_venue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data,
        website = form.website.data,
        image_link = form.image_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = seeking_description
        )

      db.session.add(new_venue)

      db.session.commit()

      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    db.session.rollback()

    flash('Venue ' + request.form['name'] + ' could not be listed!')

  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database


  data = []

  all_artists = Artist.query.all()

  for artist in all_artists: 

    data.append(artist._create_individual_artist_dict())

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given venue_id
  # TODO: replace with real artist data from the artist table, using artist_id


  current_artist = Artist.query.get(artist_id)

  past_shows = Show.query.filter_by(artist_id = artist_id).filter(Show.start_time < datetime.datetime.now()).all()
  upcoming_shows = Show.query.filter_by(artist_id = artist_id).filter(Show.start_time >= datetime.datetime.now()).all()

  past_shows_data = []
  upcoming_shows_data = []

  for show in past_shows:

    past_shows_data.append(show._create_individual_show_dict_2())

  for show in upcoming_shows:
    upcoming_shows_data.append(show._create_individual_show_dict_2())

  data = {
    'id': current_artist.id,
    'name': current_artist.name,
    'genres': current_artist.genres,

    'city': current_artist.city,
    'state': current_artist.state,
    'phone': current_artist.phone,
    'website': current_artist.website,
    'facebook_link': current_artist.facebook_link,
    'seeking_venue': current_artist.seeking_venue,
    'seeking_description': current_artist.seeking_description,
    'image_link': current_artist.image_link,
    'past_shows':past_shows_data,
    'upcoming_shows': upcoming_shows_data,
    'past_shows_count': len(past_shows_data),
    'upcoming_shows_count': len(upcoming_shows_data)

  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)

  try:

# on successful db insert, flash success
    if form.validate():
      print(form.name.data)


      if form.seeking_venue.data is False:
        seeking_description = ''
      else:
        seeking_description = form.seeking_description

      new_artist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data,
        website = form.website.data,
        image_link = form.image_link.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = seeking_description
        )

      db.session.add(new_artist)
      db.session.commit()

      flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()

    flash('Artist ' + request.form['name'] + ' could not be listed!')

  finally:
    db.session.close()


  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []

  all_shows = Show.query.all()

  for show in all_shows: 

    data.append(show._create_individual_show_dict())

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form)

  try:

    if form.validate():

      # on successful db insert, flash success

      new_show = Show(
        venue_id = form.venue_id.data,
        artist_id = form.artist_id.data,
        start_time = form.start_time.data
      )

      db.session.add(new_show)

      db.session.commit()
      flash('Show was successfully listed!')

  except:
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()

    flash('Show could not be listed!')

  finally:
    db.session.close()


  return render_template('pages/home.html')



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''