from la_reclame.items import items
from la_reclame.models import Users


@items.app_template_global()
def get_user_by_id(user_id: int):
    return Users.query.get(user_id)


@items.app_template_global()
def cut_description(description: str, chars: int):
    return description[:chars] + '...' if len(description) > chars else description[:chars]
