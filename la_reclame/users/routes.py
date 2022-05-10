from flask import render_template, session
from la_reclame.users import users


@users.route('/profile')
def profile():
    return render_template('profile.html', user=session['user'])
