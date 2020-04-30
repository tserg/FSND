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

    """
      Constraint based on the assumption that there will not be two venues
      with the same name and address
    """

    __table_args__ = (db.UniqueConstraint('name', 'city', 'state', 'address'), )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    
    def _create_individual_venue_dict(self):

      """
        Helper function for venues()
      """
      temp_dict = {
        'id': self.id,
        'name': self.name,

      }

      return temp_dict

    def _create_individual_venue_dict_2(self):
      """ 
        Helper function for show_venue() and edit_venue()
      """

      temp_dict ={
        'id': self.id,
        'name': self.name,
        'genres': self.genres,
        'address': self.address,
        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description,
        'image_link': self.image_link
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

    """
      Constraint based on the assumption that there will not be two venues
      with the same name, city and genres
    """

    __table_args__ = (db.UniqueConstraint('name', 'city', 'state', 'genres'), )

    def _create_individual_artist_dict(self):

      """
        Helper function for artists()
      """
      temp_dict = {
        'id': self.id,
        'name': self.name
      }

      return temp_dict

    def _create_individual_artist_dict_2(self):

      """
        Helper function for create_artist() and edit_artist()

      """

      temp_dict = {
        'id': self.id,
        'name': self.name,
        'genres': self.genres,

        'city': self.city,
        'state': self.state,
        'phone': self.phone,
        'website': self.website,
        'facebook_link': self.facebook_link,
        'seeking_venue': self.seeking_venue,
        'seeking_description': self.seeking_description,
        'image_link': self.image_link,


      }

      return temp_dict


class Show(db.Model):
  __tablename__ = 'Shows' 

  venue_id =  db.Column(db.Integer, db.ForeignKey('Venues.id'), primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artists.id'), primary_key=True)
  start_time = db.Column(db.DateTime(), primary_key=True)

  """
    Constraint on the assumption that an artist cannot be at more than one venue at one time but
    a single venue may have multiple stages.

  """

  __table_args__ = (db.UniqueConstraint('artist_id', 'start_time', name='same_artist_start_time'), )

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

  latest_venue = Venue.query.order_by(Venue.id.desc()).limit(1).all()

  data = latest_venue[0]._create_individual_venue_dict_2()

  return render_template('pages/home.html', venue=data)


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
      current_venue = venue._create_individual_venue_dict()
      upcoming_shows = Show.query.filter_by(venue_id = venue.id).filter(Show.start_time >= datetime.datetime.now()).all()
      current_venue['num_upcoming_shows'] = len(upcoming_shows)
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
  
  query = request.form.get('search_term')

  print(query)

  '''
    https://knowledge.udacity.com/questions/83562
  '''

  results = Venue.query.filter(Venue.name.ilike('%{}%'.format(query))).all()

  venue_list = []

  for result in results:

    temp_dict = {}
    temp_dict['id'] = result.id
    temp_dict['name'] = result.name
    temp_dict['num_upcoming_shows'] = Show.query.filter_by(venue_id = result.id).filter(Show.start_time >= datetime.datetime.now()).all()

    venue_list.append(temp_dict)

  response = {
    'count': len(results),
    'data': venue_list
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

  data = current_venue._create_individual_venue_dict_2()
   
  data['past_shows'] = past_shows_data
  data['upcoming_shows'] = upcoming_shows_data
  data['past_shows_count'] =  len(past_shows_data)
  data['upcoming_shows_count'] = len(upcoming_shows_data)

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


  # redirect is used instead of render_template due to the need 
  # to send data using index()

  return redirect(url_for('index'))

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  try:
    current_venue = Venue.query.get(venue_id)
    db.session.delete(current_venue)
    db.session.commit()

    flash('Venue ' + str(venue_id) + ' was deleted!')

  except:

    db.session.rollback()

    flash('Venue ' + str(venue_id) + ' could not be deleted!')

  finally:

    db.session.close()


  return redirect(url_for('index'))

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

  query = request.form.get('search_term')

  print(query)

  '''
    https://knowledge.udacity.com/questions/83562
  '''

  results = Artist.query.filter(Artist.name.ilike('%{}%'.format(query))).all()

  artist_list = []

  for result in results:

    temp_dict = {}
    temp_dict['id'] = result.id
    temp_dict['name'] = result.name
    temp_dict['num_upcoming_shows'] = Show.query.filter_by(artist_id = result.id).filter(Show.start_time >= datetime.datetime.now()).all()

    artist_list.append(temp_dict)

  response = {
    'count': len(results),
    'data': artist_list
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

  data = current_artist._create_individual_artist_dict_2()

  data['past_shows'] = past_shows_data
  data['upcoming_shows'] =  upcoming_shows_data
  data['past_shows_count'] = len(past_shows_data)
  data['upcoming_shows_count'] = len(upcoming_shows_data)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)
  artist_data = artist._create_individual_artist_dict_2()

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.website.data = artist.website
  form.image_link.data = artist.image_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form)
  current_artist = Artist.query.get(artist_id)
  try:

# on successful db insert, flash success
    if form.validate():

      if form.seeking_venue.data is False:
        seeking_description = ''
      else:
        seeking_description = form.seeking_description.data

      current_artist.name = form.name.data
      current_artist.city = form.city.data
      current_artist.state = form.state.data
      current_artist.phone = form.phone.data
      current_artist.genres = form.genres.data
      current_artist.facebook_link = form.facebook_link.data
      current_artist.website = form.website.data
      current_artist.image_link = form.image_link.data
      current_artist.seeking_venue = form.seeking_venue.data
      current_artist.seeking_description = seeking_description

      db.session.commit()

      flash('Information for Artist ' + request.form['name'] + ' was successfully edited!')

  except:
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('Information for Artist ' + request.form['name'] + ' could not be edited!')

  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.get(venue_id)

  venue_data = venue._create_individual_venue_dict_2()

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.website.data = venue.website
  form.image_link.data = venue.image_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  current_venue = Venue.query.get(venue_id)
  try:

# on successful db insert, flash success
    if form.validate():

      if form.seeking_talent.data is False:
        seeking_description = ''
      else:
        seeking_description = form.seeking_description.data

      current_venue.name = form.name.data
      current_venue.city = form.city.data
      current_venue.state = form.state.data
      current_venue.address = form.address.data
      current_venue.phone = form.phone.data
      current_venue.genres = form.genres.data
      current_venue.facebook_link = form.facebook_link.data
      current_venue.website = form.website.data
      current_venue.image_link = form.image_link.data
      current_venue.seeking_talent = form.seeking_talent.data
      current_venue.seeking_description = seeking_description

      db.session.commit()

      flash('Information for Venue ' + request.form['name'] + ' was successfully edited!')

  except:
# TODO: on unsuccessful db insert, flash an error instead.
# e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('Information for Venue ' + request.form['name'] + ' could not be edited!')

  finally:
    db.session.close()

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

      if form.seeking_venue.data is False:
        seeking_description = ''
      else:
        seeking_description = form.seeking_description.data

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

  # redirect is used instead of render_template due to the need 
  # to send data using index()

  return redirect(url_for('index'))


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


  return redirect(url_for('index'))



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