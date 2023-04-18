class BytecodeYaccExpressionList:

    def p_expression_list_1(self, p):
        'expression_list_1 : expression'
        p[0] = [p[1]]

    def p_expression_list_2(self, p):
        'expression_list_2 : expression_list_1 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_3(self, p):
        'expression_list_3 : expression_list_2 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_4(self, p):
        'expression_list_4 : expression_list_3 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_5(self, p):
        'expression_list_5 : expression_list_4 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_6(self, p):
        'expression_list_6 : expression_list_5 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_7(self, p):
        'expression_list_7 : expression_list_6 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_8(self, p):
        'expression_list_8 : expression_list_7 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_9(self, p):
        'expression_list_9 : expression_list_8 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_10(self, p):
        'expression_list_10 : expression_list_9 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_11(self, p):
        'expression_list_11 : expression_list_10 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_12(self, p):
        'expression_list_12 : expression_list_11 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_13(self, p):
        'expression_list_13 : expression_list_12 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_14(self, p):
        'expression_list_14 : expression_list_13 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_15(self, p):
        'expression_list_15 : expression_list_14 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_16(self, p):
        'expression_list_16 : expression_list_15 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_17(self, p):
        'expression_list_17 : expression_list_16 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_18(self, p):
        'expression_list_18 : expression_list_17 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_19(self, p):
        'expression_list_19 : expression_list_18 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_20(self, p):
        'expression_list_20 : expression_list_19 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_21(self, p):
        'expression_list_21 : expression_list_20 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_22(self, p):
        'expression_list_22 : expression_list_21 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_23(self, p):
        'expression_list_23 : expression_list_22 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_24(self, p):
        'expression_list_24 : expression_list_23 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_25(self, p):
        'expression_list_25 : expression_list_24 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_26(self, p):
        'expression_list_26 : expression_list_25 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_27(self, p):
        'expression_list_27 : expression_list_26 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_28(self, p):
        'expression_list_28 : expression_list_27 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_29(self, p):
        'expression_list_29 : expression_list_28 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_30(self, p):
        'expression_list_30 : expression_list_29 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_31(self, p):
        'expression_list_31 : expression_list_30 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_32(self, p):
        'expression_list_32 : expression_list_31 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_33(self, p):
        'expression_list_33 : expression_list_32 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_34(self, p):
        'expression_list_34 : expression_list_33 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_35(self, p):
        'expression_list_35 : expression_list_34 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_36(self, p):
        'expression_list_36 : expression_list_35 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_37(self, p):
        'expression_list_37 : expression_list_36 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_38(self, p):
        'expression_list_38 : expression_list_37 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_39(self, p):
        'expression_list_39 : expression_list_38 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_40(self, p):
        'expression_list_40 : expression_list_39 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_41(self, p):
        'expression_list_41 : expression_list_40 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_42(self, p):
        'expression_list_42 : expression_list_41 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_43(self, p):
        'expression_list_43 : expression_list_42 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_44(self, p):
        'expression_list_44 : expression_list_43 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_45(self, p):
        'expression_list_45 : expression_list_44 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_46(self, p):
        'expression_list_46 : expression_list_45 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_47(self, p):
        'expression_list_47 : expression_list_46 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_48(self, p):
        'expression_list_48 : expression_list_47 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_49(self, p):
        'expression_list_49 : expression_list_48 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_50(self, p):
        'expression_list_50 : expression_list_49 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_51(self, p):
        'expression_list_51 : expression_list_50 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_52(self, p):
        'expression_list_52 : expression_list_51 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_53(self, p):
        'expression_list_53 : expression_list_52 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_54(self, p):
        'expression_list_54 : expression_list_53 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_55(self, p):
        'expression_list_55 : expression_list_54 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_56(self, p):
        'expression_list_56 : expression_list_55 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_57(self, p):
        'expression_list_57 : expression_list_56 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_58(self, p):
        'expression_list_58 : expression_list_57 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_59(self, p):
        'expression_list_59 : expression_list_58 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_60(self, p):
        'expression_list_60 : expression_list_59 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_61(self, p):
        'expression_list_61 : expression_list_60 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_62(self, p):
        'expression_list_62 : expression_list_61 expression'
        p[0] = [p[2], *p[1]]

    def p_expression_list_63(self, p):
        'expression_list_63 : expression_list_62 expression'
        p[0] = [p[2], *p[1]]

