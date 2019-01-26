

class CustomNode(graphene.Node):
	class Meta:
		name = 'Node'

	@staticmethod
	def to_global_id(type, id):
		return '{}_{}'.format(type, id)

	# @staticmethod
	# def get_node_from_global_id(info, global_id, only_type=None):
	# 	type, id = global_id.split('_')
	# 	if only_type:
	# 	assert type == only_type._meta.name, 'Received not compatible node.'
	# 	if type == 'User':
	# 	return get_user(id)
	# 	elif type == 'Photo':
	# 	return get_photo(id)
