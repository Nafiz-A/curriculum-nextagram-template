from models.user import *
from models.following import *
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for

following_blueprint = Blueprint(
    'following', __name__, template_folder='templates'
)


@following_blueprint.route('/show')
def show():
    users = User.select()
    return render_template('following/view.html', current_user=current_user, users=users)


@following_blueprint.route('follow/<id>', methods=['POST'])
def follow(id):
    follow = Following(user_id=id, follower_id=current_user.id)
    follow.save()
    return redirect(url_for('following.show'))


@following_blueprint.route('accept/<id>', methods=['POST'])
def accept(id):
    accept = Following.get((Following.user_id == current_user.id) & (
        Following.follower_id == id))
    accept.approved = True
    accept.save()

    return redirect(url_for('following.show'))
