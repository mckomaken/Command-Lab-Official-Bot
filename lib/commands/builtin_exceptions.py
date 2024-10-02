

from lib.commands.exceptions import DynamicCommandExceptionType, LiteralMessage, SimpleCommandExceptionType


FLOAT_TOO_SMALL = DynamicCommandExceptionType(lambda found, minimum: LiteralMessage(f"Float must not be less than {minimum}, found {found}"))
FLOAT_TOO_BIG = DynamicCommandExceptionType(lambda found, maximum: LiteralMessage(f"Float must not be more than {maximum}, found {found}"))

INTEGER_TOO_SMALL = DynamicCommandExceptionType(lambda found, minimum: LiteralMessage(f"Integer must not be less than {minimum}, found {found}"))
INTEGER_TOO_BIG = DynamicCommandExceptionType(lambda found, maximum: LiteralMessage(f"Integer must not be more than {maximum}, found {found}"))

LONG_TOO_SMALL = DynamicCommandExceptionType(lambda found, minimum: LiteralMessage(f"Long must not be less than {minimum}, found {found}"))
LONG_TOO_BIG = DynamicCommandExceptionType(lambda found, maximum: LiteralMessage(f"Long must not be more than {maximum}, found {found}"))

DOUBLE_TOO_SMALL = DynamicCommandExceptionType(lambda found, minimum: LiteralMessage(f"Double must not be less than {minimum}, found {found}"))
DOUBLE_TOO_BIG = DynamicCommandExceptionType(lambda found, maximum: LiteralMessage(f"Double must not be more than {maximum}, found {found}"))

LITERAL_INCORRECT = DynamicCommandExceptionType(lambda expected: LiteralMessage(f"Expected literal {expected}"))

READER_EXPECTED_START_OF_QUOTE = SimpleCommandExceptionType(LiteralMessage("Expected quote to start a string"))
READER_EXPECTED_END_OF_QUOTE = SimpleCommandExceptionType(LiteralMessage("Unclosed quoted string"))
READER_INVALID_ESCAPE = DynamicCommandExceptionType(lambda character: LiteralMessage(f"Invalid escape sequence '{character}' in quoted string"))
READER_EXPECTED_SYMBOL = DynamicCommandExceptionType(lambda symbol: LiteralMessage(f"Expected {symbol}"))

READER_INVALID_BOOL = DynamicCommandExceptionType(lambda value: LiteralMessage(f"Invalid bool, expected true or false but found '{value}'"))
READER_EXPECTED_BOOL = SimpleCommandExceptionType(LiteralMessage("Expected bool"))

READER_INVALID_INT = DynamicCommandExceptionType(lambda value: LiteralMessage(f"Invalid integer '{value}'"))
READER_EXPECTED_INT = SimpleCommandExceptionType(LiteralMessage("Expected integer"))

READER_INVALID_LONG = DynamicCommandExceptionType(lambda value: LiteralMessage(f"Invalid long '{value}'"))
READER_EXPECTED_LONG = SimpleCommandExceptionType(LiteralMessage("Expected long"))

READER_INVALID_DOUBLE = DynamicCommandExceptionType(lambda value: LiteralMessage(f"Invalid double '{value}'"))
READER_EXPECTED_DOUBLE = SimpleCommandExceptionType(LiteralMessage("Expected double"))

READER_INVALID_FLOAT = DynamicCommandExceptionType(lambda value: LiteralMessage(f"Invalid float '{value}'"))
READER_EXPECTED_FLOAT = SimpleCommandExceptionType(LiteralMessage("Expected float"))

DISPATCHER_UNKNOWN_COMMAND = SimpleCommandExceptionType(LiteralMessage("Unknown command"))
DISPATCHER_UNKNOWN_ARGUMENT = SimpleCommandExceptionType(LiteralMessage("Incorrect argument for command"))
DISPATCHER_EXPECTED_ARGUMENT_SEPARATOR = SimpleCommandExceptionType(
    LiteralMessage("Expected whitespace to end one argument, but found trailing data")
)
DISPATCHER_PARSE_EXPECTION = DynamicCommandExceptionType(lambda message: LiteralMessage(f"Could not parse command: {message}"))


class BuiltInExceptions:
    def double_too_low():
        return DOUBLE_TOO_SMALL

    def double_too_high():
        return DOUBLE_TOO_BIG

    def float_too_low():
        return FLOAT_TOO_SMALL

    def float_too_high():
        return FLOAT_TOO_BIG

    def integer_too_low():
        return INTEGER_TOO_SMALL

    def integer_too_high():
        return INTEGER_TOO_BIG

    def long_too_low():
        return LONG_TOO_SMALL

    def long_too_high():
        return LONG_TOO_BIG

    def literal_incorrect():
        return LITERAL_INCORRECT

    def reader_expected_start_of_quote():
        return READER_EXPECTED_START_OF_QUOTE

    def reader_expected_end_of_quote():
        return READER_EXPECTED_END_OF_QUOTE

    def reader_invalid_escape():
        return READER_INVALID_ESCAPE

    def reader_invalid_bool():
        return READER_INVALID_BOOL

    def reader_invalid_int():
        return READER_INVALID_INT

    def reader_expected_int():
        return READER_EXPECTED_INT

    def reader_invalid_long():
        return READER_INVALID_FLOAT

    def reader_expected_long():
        return READER_EXPECTED_LONG

    def reader_expected_double():
        return READER_EXPECTED_DOUBLE

    def reader_invalid_double():
        return READER_INVALID_DOUBLE

    def reader_invalid_float():
        return READER_INVALID_FLOAT

    def reader_expected_float():
        return READER_EXPECTED_FLOAT

    def reader_expected_symbol():
        return READER_EXPECTED_SYMBOL

    def dispatcher_unknown_command():
        return DISPATCHER_UNKNOWN_COMMAND

    def dispatcher_unknown_argument():
        return DISPATCHER_UNKNOWN_ARGUMENT

    def dispatcher_expected_argument_separator():
        return DISPATCHER_EXPECTED_ARGUMENT_SEPARATOR

    def dispatcher_parse_expection():
        return DISPATCHER_PARSE_EXPECTION

    def reader_expected_bool():
        return READER_EXPECTED_BOOL
