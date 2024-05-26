from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
from models import storage
from models.amenity import *
from models.city import *
from models.user import *
from models.place import *
from models.state import *
from models.review import *
