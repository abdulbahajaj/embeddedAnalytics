import graphene
from . import actions

class CompanyType(graphene.ObjectType):
	class Meta:
		interfaces = (graphene.relay.Node, )
	created = graphene.Int()
	public_key = graphene.String()


class UserType(graphene.ObjectType):
	class Meta:
		interfaces = (graphene.relay.Node, )
	logged_in = graphene.Boolean()
	email = graphene.String()
	created = graphene.Int()
	company	= graphene.Field(CompanyType)

class Query(graphene.ObjectType):
	user = graphene.Field(UserType)
	def resolve_user(self, info, **kwargs):
		user = info.context.get("user",None)
		print(user)
		if user is None:
			return UserType(logged_in=False)
		return UserType(
			logged_in=True,
			created=user.created,
			email=user.email,
			company=CompanyType(
				created=user.company.created,
				public_key = user.company.public_key,
			)
		)

class CreateUser(graphene.Mutation):
	class Arguments:
		email = graphene.String()
		password = graphene.String()

	Output = UserType
	def mutate(self, info, **kwargs):
		user = actions.register(email=kwargs.get('email'), password=kwargs.get('password'))
		return UserType(
			logged_in=True,
			created=user.created,
			email=user.email,
			company=CompanyType(
				created=user.company.created,
				public_key = user.company.public_key,
			)
		)


class LoginUser(graphene.Mutation):
	class Arguments:
		email = graphene.String()
		password = graphene.String()
	Output = UserType
	def mutate(self, info, **kwargs):
		email=kwargs.get('email')
		password=kwargs.get('password').encode('utf-8')
		actions.logout()
		user = actions.login(email=email, password=password)
		return UserType(
			logged_in=True,
			created=user.created,
			email=user.email,
			company=CompanyType(
				created=user.company.created,
				public_key = user.company.public_key,
			)
		)

class Mutation(graphene.ObjectType):
	createUser = CreateUser.Field()
	loginUser = LoginUser.Field()



















