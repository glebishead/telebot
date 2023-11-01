from .send_all import *
from .add_product import *


def is_admin(userid):
	# todo: admin_list
	return userid == ADMIN_ID
