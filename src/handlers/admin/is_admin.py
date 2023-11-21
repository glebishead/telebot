from src import ADMIN_ID
from data.methods import select_from_users


async def is_admin(userid):
	users = [*await select_from_users()]
	if userid in [*map(lambda x: x[1], [*filter(lambda x: x[-1] == 1, users)])] or userid == ADMIN_ID:
		return True
	return False
