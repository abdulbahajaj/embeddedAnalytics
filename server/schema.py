import graphene
from user.schema import Query as user_query, Mutation as user_mutation

class Query(
	user_query,
	graphene.ObjectType):
	node = graphene.relay.Node.Field()

class Mutation(
	user_mutation,
	graphene.ObjectType
	): pass

schema = graphene.Schema(query=Query,mutation=Mutation)
