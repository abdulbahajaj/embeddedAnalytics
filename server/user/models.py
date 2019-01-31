import mongoengine

mongoengine.connect("embeddedAnalytics")

class Company(mongoengine.Document):
	public_key = mongoengine.StringField()

	private_key_hash = mongoengine.BinaryField()
	# private_key_hash_salt = mongoengine.BinaryField(required=True)
	private_key_encrypted = mongoengine.BinaryField()

	created = mongoengine.IntField()

class User(mongoengine.Document):
	company_key_encrypted = mongoengine.BinaryField(required=True)
	password_hash = mongoengine.BinaryField(required=True)
	email = mongoengine.StringField(required=True)
	created = mongoengine.IntField()
	company = mongoengine.ReferenceField(Company)


