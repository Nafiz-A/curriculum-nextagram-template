from models.user import *

following_blueprint = Blueprint(
    'following', __name__, template_folder='templates'
)


@following_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('following/new.html')
