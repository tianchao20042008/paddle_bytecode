# Do not edit directly. This file is generated by tools/generate_lexer_token_class.py
class BytecodeLexerToken:

    def parse_token(t):
        return t


    t_LABEL = 'LABEL'

    def t_POP_TOP(self, t):
        "POP_TOP"
        return self.parse_token(t)

    def t_ROT_TWO(self, t):
        "ROT_TWO"
        return self.parse_token(t)

    def t_ROT_THREE(self, t):
        "ROT_THREE"
        return self.parse_token(t)

    def t_DUP_TOP(self, t):
        "DUP_TOP"
        return self.parse_token(t)

    def t_DUP_TOP_TWO(self, t):
        "DUP_TOP_TWO"
        return self.parse_token(t)

    def t_ROT_FOUR(self, t):
        "ROT_FOUR"
        return self.parse_token(t)

    def t_NOP(self, t):
        "NOP"
        return self.parse_token(t)

    def t_UNARY_POSITIVE(self, t):
        "UNARY_POSITIVE"
        return self.parse_token(t)

    def t_UNARY_NEGATIVE(self, t):
        "UNARY_NEGATIVE"
        return self.parse_token(t)

    def t_UNARY_NOT(self, t):
        "UNARY_NOT"
        return self.parse_token(t)

    def t_UNARY_INVERT(self, t):
        "UNARY_INVERT"
        return self.parse_token(t)

    def t_BINARY_MATRIX_MULTIPLY(self, t):
        "BINARY_MATRIX_MULTIPLY"
        return self.parse_token(t)

    def t_INPLACE_MATRIX_MULTIPLY(self, t):
        "INPLACE_MATRIX_MULTIPLY"
        return self.parse_token(t)

    def t_BINARY_POWER(self, t):
        "BINARY_POWER"
        return self.parse_token(t)

    def t_BINARY_MULTIPLY(self, t):
        "BINARY_MULTIPLY"
        return self.parse_token(t)

    def t_BINARY_MODULO(self, t):
        "BINARY_MODULO"
        return self.parse_token(t)

    def t_BINARY_ADD(self, t):
        "BINARY_ADD"
        return self.parse_token(t)

    def t_BINARY_SUBTRACT(self, t):
        "BINARY_SUBTRACT"
        return self.parse_token(t)

    def t_BINARY_SUBSCR(self, t):
        "BINARY_SUBSCR"
        return self.parse_token(t)

    def t_BINARY_FLOOR_DIVIDE(self, t):
        "BINARY_FLOOR_DIVIDE"
        return self.parse_token(t)

    def t_BINARY_TRUE_DIVIDE(self, t):
        "BINARY_TRUE_DIVIDE"
        return self.parse_token(t)

    def t_INPLACE_FLOOR_DIVIDE(self, t):
        "INPLACE_FLOOR_DIVIDE"
        return self.parse_token(t)

    def t_INPLACE_TRUE_DIVIDE(self, t):
        "INPLACE_TRUE_DIVIDE"
        return self.parse_token(t)

    def t_GET_AITER(self, t):
        "GET_AITER"
        return self.parse_token(t)

    def t_GET_ANEXT(self, t):
        "GET_ANEXT"
        return self.parse_token(t)

    def t_BEFORE_ASYNC_WITH(self, t):
        "BEFORE_ASYNC_WITH"
        return self.parse_token(t)

    def t_BEGIN_FINALLY(self, t):
        "BEGIN_FINALLY"
        return self.parse_token(t)

    def t_END_ASYNC_FOR(self, t):
        "END_ASYNC_FOR"
        return self.parse_token(t)

    def t_INPLACE_ADD(self, t):
        "INPLACE_ADD"
        return self.parse_token(t)

    def t_INPLACE_SUBTRACT(self, t):
        "INPLACE_SUBTRACT"
        return self.parse_token(t)

    def t_INPLACE_MULTIPLY(self, t):
        "INPLACE_MULTIPLY"
        return self.parse_token(t)

    def t_INPLACE_MODULO(self, t):
        "INPLACE_MODULO"
        return self.parse_token(t)

    def t_STORE_SUBSCR(self, t):
        "STORE_SUBSCR"
        return self.parse_token(t)

    def t_DELETE_SUBSCR(self, t):
        "DELETE_SUBSCR"
        return self.parse_token(t)

    def t_BINARY_LSHIFT(self, t):
        "BINARY_LSHIFT"
        return self.parse_token(t)

    def t_BINARY_RSHIFT(self, t):
        "BINARY_RSHIFT"
        return self.parse_token(t)

    def t_BINARY_AND(self, t):
        "BINARY_AND"
        return self.parse_token(t)

    def t_BINARY_XOR(self, t):
        "BINARY_XOR"
        return self.parse_token(t)

    def t_BINARY_OR(self, t):
        "BINARY_OR"
        return self.parse_token(t)

    def t_INPLACE_POWER(self, t):
        "INPLACE_POWER"
        return self.parse_token(t)

    def t_GET_ITER(self, t):
        "GET_ITER"
        return self.parse_token(t)

    def t_GET_YIELD_FROM_ITER(self, t):
        "GET_YIELD_FROM_ITER"
        return self.parse_token(t)

    def t_PRINT_EXPR(self, t):
        "PRINT_EXPR"
        return self.parse_token(t)

    def t_LOAD_BUILD_CLASS(self, t):
        "LOAD_BUILD_CLASS"
        return self.parse_token(t)

    def t_YIELD_FROM(self, t):
        "YIELD_FROM"
        return self.parse_token(t)

    def t_GET_AWAITABLE(self, t):
        "GET_AWAITABLE"
        return self.parse_token(t)

    def t_INPLACE_LSHIFT(self, t):
        "INPLACE_LSHIFT"
        return self.parse_token(t)

    def t_INPLACE_RSHIFT(self, t):
        "INPLACE_RSHIFT"
        return self.parse_token(t)

    def t_INPLACE_AND(self, t):
        "INPLACE_AND"
        return self.parse_token(t)

    def t_INPLACE_XOR(self, t):
        "INPLACE_XOR"
        return self.parse_token(t)

    def t_INPLACE_OR(self, t):
        "INPLACE_OR"
        return self.parse_token(t)

    def t_WITH_CLEANUP_START(self, t):
        "WITH_CLEANUP_START"
        return self.parse_token(t)

    def t_WITH_CLEANUP_FINISH(self, t):
        "WITH_CLEANUP_FINISH"
        return self.parse_token(t)

    def t_RETURN_VALUE(self, t):
        "RETURN_VALUE"
        return self.parse_token(t)

    def t_IMPORT_STAR(self, t):
        "IMPORT_STAR"
        return self.parse_token(t)

    def t_SETUP_ANNOTATIONS(self, t):
        "SETUP_ANNOTATIONS"
        return self.parse_token(t)

    def t_YIELD_VALUE(self, t):
        "YIELD_VALUE"
        return self.parse_token(t)

    def t_POP_BLOCK(self, t):
        "POP_BLOCK"
        return self.parse_token(t)

    def t_END_FINALLY(self, t):
        "END_FINALLY"
        return self.parse_token(t)

    def t_POP_EXCEPT(self, t):
        "POP_EXCEPT"
        return self.parse_token(t)

    def t_STORE_NAME(self, t):
        "STORE_NAME"
        return self.parse_token(t)

    def t_DELETE_NAME(self, t):
        "DELETE_NAME"
        return self.parse_token(t)

    def t_UNPACK_SEQUENCE(self, t):
        "UNPACK_SEQUENCE"
        return self.parse_token(t)

    def t_FOR_ITER(self, t):
        "FOR_ITER"
        return self.parse_token(t)

    def t_UNPACK_EX(self, t):
        "UNPACK_EX"
        return self.parse_token(t)

    def t_STORE_ATTR(self, t):
        "STORE_ATTR"
        return self.parse_token(t)

    def t_DELETE_ATTR(self, t):
        "DELETE_ATTR"
        return self.parse_token(t)

    def t_STORE_GLOBAL(self, t):
        "STORE_GLOBAL"
        return self.parse_token(t)

    def t_DELETE_GLOBAL(self, t):
        "DELETE_GLOBAL"
        return self.parse_token(t)

    def t_LOAD_CONST(self, t):
        "LOAD_CONST"
        return self.parse_token(t)

    def t_LOAD_NAME(self, t):
        "LOAD_NAME"
        return self.parse_token(t)

    def t_BUILD_TUPLE(self, t):
        "BUILD_TUPLE"
        return self.parse_token(t)

    def t_BUILD_LIST(self, t):
        "BUILD_LIST"
        return self.parse_token(t)

    def t_BUILD_SET(self, t):
        "BUILD_SET"
        return self.parse_token(t)

    def t_BUILD_MAP(self, t):
        "BUILD_MAP"
        return self.parse_token(t)

    def t_LOAD_ATTR(self, t):
        "LOAD_ATTR"
        return self.parse_token(t)

    def t_COMPARE_OP(self, t):
        "COMPARE_OP"
        return self.parse_token(t)

    def t_IMPORT_NAME(self, t):
        "IMPORT_NAME"
        return self.parse_token(t)

    def t_IMPORT_FROM(self, t):
        "IMPORT_FROM"
        return self.parse_token(t)

    def t_JUMP_FORWARD(self, t):
        "JUMP_FORWARD"
        return self.parse_token(t)

    def t_JUMP_IF_FALSE_OR_POP(self, t):
        "JUMP_IF_FALSE_OR_POP"
        return self.parse_token(t)

    def t_JUMP_IF_TRUE_OR_POP(self, t):
        "JUMP_IF_TRUE_OR_POP"
        return self.parse_token(t)

    def t_JUMP_ABSOLUTE(self, t):
        "JUMP_ABSOLUTE"
        return self.parse_token(t)

    def t_POP_JUMP_IF_FALSE(self, t):
        "POP_JUMP_IF_FALSE"
        return self.parse_token(t)

    def t_POP_JUMP_IF_TRUE(self, t):
        "POP_JUMP_IF_TRUE"
        return self.parse_token(t)

    def t_LOAD_GLOBAL(self, t):
        "LOAD_GLOBAL"
        return self.parse_token(t)

    def t_SETUP_FINALLY(self, t):
        "SETUP_FINALLY"
        return self.parse_token(t)

    def t_LOAD_FAST(self, t):
        "LOAD_FAST"
        return self.parse_token(t)

    def t_STORE_FAST(self, t):
        "STORE_FAST"
        return self.parse_token(t)

    def t_DELETE_FAST(self, t):
        "DELETE_FAST"
        return self.parse_token(t)

    def t_RAISE_VARARGS(self, t):
        "RAISE_VARARGS"
        return self.parse_token(t)

    def t_CALL_FUNCTION(self, t):
        "CALL_FUNCTION"
        return self.parse_token(t)

    def t_MAKE_FUNCTION(self, t):
        "MAKE_FUNCTION"
        return self.parse_token(t)

    def t_BUILD_SLICE(self, t):
        "BUILD_SLICE"
        return self.parse_token(t)

    def t_LOAD_CLOSURE(self, t):
        "LOAD_CLOSURE"
        return self.parse_token(t)

    def t_LOAD_DEREF(self, t):
        "LOAD_DEREF"
        return self.parse_token(t)

    def t_STORE_DEREF(self, t):
        "STORE_DEREF"
        return self.parse_token(t)

    def t_DELETE_DEREF(self, t):
        "DELETE_DEREF"
        return self.parse_token(t)

    def t_CALL_FUNCTION_KW(self, t):
        "CALL_FUNCTION_KW"
        return self.parse_token(t)

    def t_CALL_FUNCTION_EX(self, t):
        "CALL_FUNCTION_EX"
        return self.parse_token(t)

    def t_SETUP_WITH(self, t):
        "SETUP_WITH"
        return self.parse_token(t)

    def t_LIST_APPEND(self, t):
        "LIST_APPEND"
        return self.parse_token(t)

    def t_SET_ADD(self, t):
        "SET_ADD"
        return self.parse_token(t)

    def t_MAP_ADD(self, t):
        "MAP_ADD"
        return self.parse_token(t)

    def t_LOAD_CLASSDEREF(self, t):
        "LOAD_CLASSDEREF"
        return self.parse_token(t)

    def t_EXTENDED_ARG(self, t):
        "EXTENDED_ARG"
        return self.parse_token(t)

    def t_BUILD_LIST_UNPACK(self, t):
        "BUILD_LIST_UNPACK"
        return self.parse_token(t)

    def t_BUILD_MAP_UNPACK(self, t):
        "BUILD_MAP_UNPACK"
        return self.parse_token(t)

    def t_BUILD_MAP_UNPACK_WITH_CALL(self, t):
        "BUILD_MAP_UNPACK_WITH_CALL"
        return self.parse_token(t)

    def t_BUILD_TUPLE_UNPACK(self, t):
        "BUILD_TUPLE_UNPACK"
        return self.parse_token(t)

    def t_BUILD_SET_UNPACK(self, t):
        "BUILD_SET_UNPACK"
        return self.parse_token(t)

    def t_SETUP_ASYNC_WITH(self, t):
        "SETUP_ASYNC_WITH"
        return self.parse_token(t)

    def t_FORMAT_VALUE(self, t):
        "FORMAT_VALUE"
        return self.parse_token(t)

    def t_BUILD_CONST_KEY_MAP(self, t):
        "BUILD_CONST_KEY_MAP"
        return self.parse_token(t)

    def t_BUILD_STRING(self, t):
        "BUILD_STRING"
        return self.parse_token(t)

    def t_BUILD_TUPLE_UNPACK_WITH_CALL(self, t):
        "BUILD_TUPLE_UNPACK_WITH_CALL"
        return self.parse_token(t)

    def t_LOAD_METHOD(self, t):
        "LOAD_METHOD"
        return self.parse_token(t)

    def t_CALL_METHOD(self, t):
        "CALL_METHOD"
        return self.parse_token(t)

    def t_CALL_FINALLY(self, t):
        "CALL_FINALLY"
        return self.parse_token(t)

    def t_POP_FINALLY(self, t):
        "POP_FINALLY"
        return self.parse_token(t)

    def t_ARG0(self, t):
        "ARG0"
        return t

    def t_ARG1(self, t):
        "ARG1"
        return t

    def t_ARG2(self, t):
        "ARG2"
        return t

    def t_ARG3(self, t):
        "ARG3"
        return t

    def t_ARG4(self, t):
        "ARG4"
        return t

    def t_ARG5(self, t):
        "ARG5"
        return t

    def t_ARG6(self, t):
        "ARG6"
        return t

    def t_ARG7(self, t):
        "ARG7"
        return t

    def t_ARG8(self, t):
        "ARG8"
        return t

    def t_ARG9(self, t):
        "ARG9"
        return t

    def t_ARG10(self, t):
        "ARG10"
        return t

    def t_ARG11(self, t):
        "ARG11"
        return t

    def t_ARG12(self, t):
        "ARG12"
        return t

    def t_ARG13(self, t):
        "ARG13"
        return t

    def t_ARG14(self, t):
        "ARG14"
        return t

    def t_ARG15(self, t):
        "ARG15"
        return t

    def t_ARG16(self, t):
        "ARG16"
        return t

    def t_ARG17(self, t):
        "ARG17"
        return t

    def t_ARG18(self, t):
        "ARG18"
        return t

    def t_ARG19(self, t):
        "ARG19"
        return t

    def t_ARG20(self, t):
        "ARG20"
        return t

    def t_ARG21(self, t):
        "ARG21"
        return t

    def t_ARG22(self, t):
        "ARG22"
        return t

    def t_ARG23(self, t):
        "ARG23"
        return t

    def t_ARG24(self, t):
        "ARG24"
        return t

    def t_ARG25(self, t):
        "ARG25"
        return t

    def t_ARG26(self, t):
        "ARG26"
        return t

    def t_ARG27(self, t):
        "ARG27"
        return t

    def t_ARG28(self, t):
        "ARG28"
        return t

    def t_ARG29(self, t):
        "ARG29"
        return t

    def t_ARG30(self, t):
        "ARG30"
        return t

    def t_ARG31(self, t):
        "ARG31"
        return t

    def t_ARG32(self, t):
        "ARG32"
        return t

    def t_ARG33(self, t):
        "ARG33"
        return t

    def t_ARG34(self, t):
        "ARG34"
        return t

    def t_ARG35(self, t):
        "ARG35"
        return t

    def t_ARG36(self, t):
        "ARG36"
        return t

    def t_ARG37(self, t):
        "ARG37"
        return t

    def t_ARG38(self, t):
        "ARG38"
        return t

    def t_ARG39(self, t):
        "ARG39"
        return t

    def t_ARG40(self, t):
        "ARG40"
        return t

    def t_ARG41(self, t):
        "ARG41"
        return t

    def t_ARG42(self, t):
        "ARG42"
        return t

    def t_ARG43(self, t):
        "ARG43"
        return t

    def t_ARG44(self, t):
        "ARG44"
        return t

    def t_ARG45(self, t):
        "ARG45"
        return t

    def t_ARG46(self, t):
        "ARG46"
        return t

    def t_ARG47(self, t):
        "ARG47"
        return t

    def t_ARG48(self, t):
        "ARG48"
        return t

    def t_ARG49(self, t):
        "ARG49"
        return t

    def t_ARG50(self, t):
        "ARG50"
        return t

    def t_ARG51(self, t):
        "ARG51"
        return t

    def t_ARG52(self, t):
        "ARG52"
        return t

    def t_ARG53(self, t):
        "ARG53"
        return t

    def t_ARG54(self, t):
        "ARG54"
        return t

    def t_ARG55(self, t):
        "ARG55"
        return t

    def t_ARG56(self, t):
        "ARG56"
        return t

    def t_ARG57(self, t):
        "ARG57"
        return t

    def t_ARG58(self, t):
        "ARG58"
        return t

    def t_ARG59(self, t):
        "ARG59"
        return t

    def t_ARG60(self, t):
        "ARG60"
        return t

    def t_ARG61(self, t):
        "ARG61"
        return t

    def t_ARG62(self, t):
        "ARG62"
        return t

    def t_ARG63(self, t):
        "ARG63"
        return t


    tokens = (
        "LABEL",
        "POP_TOP",
        "ROT_TWO",
        "ROT_THREE",
        "DUP_TOP",
        "DUP_TOP_TWO",
        "ROT_FOUR",
        "NOP",
        "UNARY_POSITIVE",
        "UNARY_NEGATIVE",
        "UNARY_NOT",
        "UNARY_INVERT",
        "BINARY_MATRIX_MULTIPLY",
        "INPLACE_MATRIX_MULTIPLY",
        "BINARY_POWER",
        "BINARY_MULTIPLY",
        "BINARY_MODULO",
        "BINARY_ADD",
        "BINARY_SUBTRACT",
        "BINARY_SUBSCR",
        "BINARY_FLOOR_DIVIDE",
        "BINARY_TRUE_DIVIDE",
        "INPLACE_FLOOR_DIVIDE",
        "INPLACE_TRUE_DIVIDE",
        "GET_AITER",
        "GET_ANEXT",
        "BEFORE_ASYNC_WITH",
        "BEGIN_FINALLY",
        "END_ASYNC_FOR",
        "INPLACE_ADD",
        "INPLACE_SUBTRACT",
        "INPLACE_MULTIPLY",
        "INPLACE_MODULO",
        "STORE_SUBSCR",
        "DELETE_SUBSCR",
        "BINARY_LSHIFT",
        "BINARY_RSHIFT",
        "BINARY_AND",
        "BINARY_XOR",
        "BINARY_OR",
        "INPLACE_POWER",
        "GET_ITER",
        "GET_YIELD_FROM_ITER",
        "PRINT_EXPR",
        "LOAD_BUILD_CLASS",
        "YIELD_FROM",
        "GET_AWAITABLE",
        "INPLACE_LSHIFT",
        "INPLACE_RSHIFT",
        "INPLACE_AND",
        "INPLACE_XOR",
        "INPLACE_OR",
        "WITH_CLEANUP_START",
        "WITH_CLEANUP_FINISH",
        "RETURN_VALUE",
        "IMPORT_STAR",
        "SETUP_ANNOTATIONS",
        "YIELD_VALUE",
        "POP_BLOCK",
        "END_FINALLY",
        "POP_EXCEPT",
        "STORE_NAME",
        "DELETE_NAME",
        "UNPACK_SEQUENCE",
        "FOR_ITER",
        "UNPACK_EX",
        "STORE_ATTR",
        "DELETE_ATTR",
        "STORE_GLOBAL",
        "DELETE_GLOBAL",
        "LOAD_CONST",
        "LOAD_NAME",
        "BUILD_TUPLE",
        "BUILD_LIST",
        "BUILD_SET",
        "BUILD_MAP",
        "LOAD_ATTR",
        "COMPARE_OP",
        "IMPORT_NAME",
        "IMPORT_FROM",
        "JUMP_FORWARD",
        "JUMP_IF_FALSE_OR_POP",
        "JUMP_IF_TRUE_OR_POP",
        "JUMP_ABSOLUTE",
        "POP_JUMP_IF_FALSE",
        "POP_JUMP_IF_TRUE",
        "LOAD_GLOBAL",
        "SETUP_FINALLY",
        "LOAD_FAST",
        "STORE_FAST",
        "DELETE_FAST",
        "RAISE_VARARGS",
        "CALL_FUNCTION",
        "MAKE_FUNCTION",
        "BUILD_SLICE",
        "LOAD_CLOSURE",
        "LOAD_DEREF",
        "STORE_DEREF",
        "DELETE_DEREF",
        "CALL_FUNCTION_KW",
        "CALL_FUNCTION_EX",
        "SETUP_WITH",
        "LIST_APPEND",
        "SET_ADD",
        "MAP_ADD",
        "LOAD_CLASSDEREF",
        "EXTENDED_ARG",
        "BUILD_LIST_UNPACK",
        "BUILD_MAP_UNPACK",
        "BUILD_MAP_UNPACK_WITH_CALL",
        "BUILD_TUPLE_UNPACK",
        "BUILD_SET_UNPACK",
        "SETUP_ASYNC_WITH",
        "FORMAT_VALUE",
        "BUILD_CONST_KEY_MAP",
        "BUILD_STRING",
        "BUILD_TUPLE_UNPACK_WITH_CALL",
        "LOAD_METHOD",
        "CALL_METHOD",
        "CALL_FINALLY",
        "POP_FINALLY",
        "ARG0",
        "ARG1",
        "ARG2",
        "ARG3",
        "ARG4",
        "ARG5",
        "ARG6",
        "ARG7",
        "ARG8",
        "ARG9",
        "ARG10",
        "ARG11",
        "ARG12",
        "ARG13",
        "ARG14",
        "ARG15",
        "ARG16",
        "ARG17",
        "ARG18",
        "ARG19",
        "ARG20",
        "ARG21",
        "ARG22",
        "ARG23",
        "ARG24",
        "ARG25",
        "ARG26",
        "ARG27",
        "ARG28",
        "ARG29",
        "ARG30",
        "ARG31",
        "ARG32",
        "ARG33",
        "ARG34",
        "ARG35",
        "ARG36",
        "ARG37",
        "ARG38",
        "ARG39",
        "ARG40",
        "ARG41",
        "ARG42",
        "ARG43",
        "ARG44",
        "ARG45",
        "ARG46",
        "ARG47",
        "ARG48",
        "ARG49",
        "ARG50",
        "ARG51",
        "ARG52",
        "ARG53",
        "ARG54",
        "ARG55",
        "ARG56",
        "ARG57",
        "ARG58",
        "ARG59",
        "ARG60",
        "ARG61",
        "ARG62",
        "ARG63"
    )
