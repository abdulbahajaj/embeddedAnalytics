import graphene
from . import actions
import messages

class CompanyType(graphene.ObjectType):
	class Meta:
		interfaces = (graphene.relay.Node, )
	created = graphene.Int()
	public_key = graphene.String()

class UserType(graphene.ObjectType):
	class Meta:
		interfaces = (graphene.relay.Node, )
	email = graphene.String()
	created = graphene.Int()
	company	= graphene.Field(CompanyType)
	error = graphene.String()

class GenericResponseType(graphene.ObjectType):
	response = graphene.String()
	message = graphene.String()
	code = graphene.String()

class Query(graphene.ObjectType):
	user = graphene.Field(UserType)
	def resolve_user(self, info, **kwargs):
		try:
			user = info.context.get("user",None)
			if user is None:
				raise messages.user_not_logged_in()
			return UserType(
				created=user.created,
				email=user.email,
				company=CompanyType(
					created=user.company.created,
					public_key = user.company.public_key,
				)
			)
		except Exception as err:
			response, http_status = messages.jsonify_message(message=err)
			return UserType(error=response)

class CreateUser(graphene.Mutation):
	class Arguments:
		email = graphene.String()
		password = graphene.String()
	Output = UserType
	def mutate(self, info, **kwargs):
		try:
			user = actions.register(email=kwargs.get('email'), password=kwargs.get('password'))

			return UserType(
				created=user.created,
				email=user.email,
				company=CompanyType(
					created=user.company.created,
					public_key = user.company.public_key,
				)
			)
		except Exception as err:
			print(err)
			response, http_status = messages.jsonify_message(message=err)
			return UserType(error = response)

class LoginUser(graphene.Mutation):
	class Arguments:
		email = graphene.String()
		password = graphene.String()
	Output = UserType
	def mutate(self, info, **kwargs):
		try:
			email=kwargs.get('email')
			password=kwargs.get('password')
			user = actions.login(email=email, password=password)
			return UserType(
				created=user.created,
				email=user.email,
				company=CompanyType(
					created=user.company.created,
					public_key = user.company.public_key,
				)
			)
		except Exception as err:
			error, http_status = messages.jsonify_message(message=err)
			return UserType(error=error)




class LogoutUser(graphene.Mutation):
	class Arguments: pass
	Output = GenericResponseType
	def mutate(self, info, **kwargs):
		print("I am logging out user")
		try:

			err = actions.logout()
			print("err: ", err)
			raise err
		except Exception as err:
			response, http_status = messages.jsonify_message(
				message=err, 
				dictify=True)

			return GenericResponseType(
				response=response,
				message = response.get("message"),
				code = response.get('code'),
			)


class Mutation(graphene.ObjectType):
	createUser = CreateUser.Field()
	loginUser = LoginUser.Field()
	logoutUser = LogoutUser.Field()



















