from models.user import *
from models.following import *
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for

following_blueprint = Blueprint(
    'following', __name__, template_folder='templates'
)


@following_blueprint.route('/show')
def show():
    return '''
        <form action="follow" method=" POST"">
        <button type=" submit" class="btn btn-primary">follow</button>
        </form>
        <h6>current_user</h6>
        <form action="accept">
        <button type="submit" class="btn btn-primary">accept</button>
        </form>
        '''
    # return render_template('following/show.html', current_user=current_user)


@following_blueprint.route('follow/<user_id>', methods=['POST'])
def follow(user_id):
    follow = Following(user_id=user_id, follower_id=current_user.id)
    follow.save()
    return redirect(url_for('following.show', id=user_id))


@following_blueprint.route('accept/<user_id>', methods=['POST'])
def accept(user_id):
    # follow = Following.get((Following.user_id == current_user.id) & (
    #     Following.follower_id == user.id))
    # follow.approved = True
    # follow.save()

    return redirect(url_for('following.show', id=user_id))
