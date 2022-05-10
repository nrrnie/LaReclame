from la_reclame.items import items
from la_reclame.models import Users


@items.app_template_global()
def get_user_by_id(user_id: int):
    return Users.query.get(user_id)
