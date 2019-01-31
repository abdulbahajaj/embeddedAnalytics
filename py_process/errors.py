

def createError(name,defaultDescription):
	def wrapper(description=None,context={}):
		class ExceptionTemplate(Exception):
			name = None
			description = None
			context = None
			def __init__(self, description):
				super().__init__(description)
				self.name = name
				self.description = description
				self.context = context
		if description is None: description = defaultDescription
		ExceptionTemplate.__name__ = name
		return ExceptionTemplate(description)
	return wrapper

WrongOperationType = createError(
	name="WrongOperationType",
	defaultDescription="The given operation type doesn't exist"
)

NoArgsGiven = createError(
	name="NoArgsGiven",
	defaultDescription="No arguments were given for the operation"
)

MissingOperationType = createError(
	name="MissingOperationType",
	defaultDescription="No operation type was provided"
)

NoInputGiven = createError(
	name="NoInputGiven",
	defaultDescription="No input was provided to the given operation. You probably forget to add a collection parameter"
)
