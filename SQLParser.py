class SQLParser:
    m_QuaryWords = None
    m_Query = None
    m_IsQueryValid = False
    m_Schema = {}
    m_LegalOperators = []

    def __init__(self, i_Query):
        self.InitSchema()
        self.InitLegalOperators()
        self.m_Query = i_Query.replace(",", " ")
        # fix whitespaces
        self.m_Query = " ".join(self.m_Query.split())

    def InitSchema(self):
        self.m_Schema["Customers"] = {"Name": "string", "Age": "int"}
        self.m_Schema["Orders"] = {"CustomerName": "string", "Product": "string", "Price": "int"}

    def InitLegalOperators(self):
        self.m_LegalOperators.append("<=")
        self.m_LegalOperators.append(">=")
        self.m_LegalOperators.append("<>")
        self.m_LegalOperators.append("<")
        self.m_LegalOperators.append(">")
        self.m_LegalOperators.append("=")

    def Print(self):
        print(self.m_Query)

    def IsQueryValid(self):
        self.m_IsQueryValid = self.select_parse()
        self.m_IsQueryValid = self.m_IsQueryValid and self.from_parse()
        self.m_IsQueryValid = self.m_IsQueryValid and self.where_parse()
        return self.m_IsQueryValid

    #######################################################################################################
    # SELECT

    def select_parse(self):
        selectIndex = self.m_Query.find("SELECT")
        length = self.m_Query.find("FROM") - 1

        splittedSelect = self.m_Query[selectIndex:length].split(" ")
        return self.select_parse_Helper(splittedSelect, len(splittedSelect))

    def select_parse_Helper(self, words, len):
        if len == 1:
            return True
        elif not self.checkIfSelectedColumnNameIsValid(words[len - 1]):
            return False
        else:
            return self.select_parse_Helper(words, len - 1)

    def checkIfSelectedColumnNameIsValid(self, i_columnName):
        if i_columnName == "*":
            return True
        elif i_columnName == "DISTINCT":
            return True
        else:
            for x in self.m_Schema:
                if i_columnName == x:
                    return True
                for y in self.m_Schema[x]:
                    sp = i_columnName.split(".")
                    print(sp)
                    # What if sp[1] do not exist for example blahblah=25
                    if i_columnName == x + "." + sp[1]:
                        return True
        return False

    ########################################################################################
    # FROM
    def from_parse(self):
        FromIndex = self.m_Query.find("FROM")
        length = self.m_Query.find("WHERE") - 1
        from_sub_query = self.m_Query[FromIndex:length].split(" ")
        return self.from_parse_Helper(from_sub_query, len(from_sub_query))

    def from_parse_Helper(self, words, len):
        if len == 1:
            return True
        elif not self.checkIfFromParams(words[len - 1]):
            print(words[len - 1], " Not Exist")
            return False
        else:
            return self.from_parse_Helper(words, len - 1)

    def checkIfFromParams(self, i_param):
        if i_param == "*":
            return True
        else:
            for y in self.m_Schema:
                if i_param == y:
                    return True

        return False

    #########################################################################################
    # WHERE
    def where_parse(self):
        whereIndex = self.m_Query.find("WHERE") + 6  # what if no space after WHERE
        length = self.m_Query.find(";")
        where_sub_query = self.m_Query[whereIndex:length]
        return self.where_parse_helper(where_sub_query)

    def where_parse_helper(self, i_Query):
        if i_Query is None:
            return False
        elif len(i_Query) == 0:
            return False
        elif self.IsSimpleCondition(i_Query):
            return True
        else:
            splittedCondition = self.splitCondition(i_Query)
            if splittedCondition is None:
                print(splittedCondition)
            #Change to meaningful names

            opxx = self.checkCondition(splittedCondition[0])
            opyy = self.where_parse_helper(splittedCondition[2])
            return (opxx is None) and opyy

    def splitCondition(self, condition):
        firstAnd = None
        firstOR = None
        toAdd = None
        minIndex = None
        if "AND" in condition:
            firstAnd = condition.find("AND")
            toAdd = 3
        if "OR" in condition:
            firstOR = condition.find("OR")
            toAdd = 2

        if firstAnd is None and firstOR is not None:
            minIndex = firstOR
        elif firstOR is None and firstAnd is not None:
            minIndex = firstAnd
        elif firstOR is not None and firstAnd is not None:
            minIndex = min(firstAnd, firstOR)
        else:
            print("Error")
            return False

        if toAdd is None:
            print("Error")
            return False
        else:
            leftCondition = condition[0:minIndex].strip(" ")
            logicOperator = condition[minIndex:minIndex + toAdd]
            rightCondition = condition[minIndex + toAdd:len(condition)].strip(" ")
            return [leftCondition, logicOperator, rightCondition]

    def IsSimpleCondition(self, condition):
        andExist = "AND" in condition
        orExist = "OR" in condition
        return (not andExist) and (not orExist) and self.checkCondition(condition)

    def checkCondition(self, condition):
        condition = condition.replace('(', '')
        condition = condition.replace(')', '')
        operatorIndex = None
        for operator in self.m_LegalOperators:
            if operator in condition:
                operatorIndex = condition.find(operator)
                operatorLength = len(operator)
                break
        if operatorIndex is not None:
            leftOperand = condition[0:operatorIndex]
            rightOperandStartInIndex = operatorIndex + operatorLength
            rightOperand = condition[rightOperandStartInIndex:len(condition)]
            return self.checkIfSelectedColumnNameIsValid(leftOperand) and self.checkTypes(leftOperand, rightOperand)

        return False

    def checkTypes(self, leftOperand, rightOperand):
        sp = leftOperand.split(".")
        typeAsString = None
        if sp[0] in self.m_Schema:
            if(sp[1] in self.m_Schema[sp[0]]):
                typeAsString = self.m_Schema[sp[0]][sp[1]]

        if typeAsString == "int":
            return rightOperand.isdecimal()
        elif typeAsString == "string":
            return True
        else:
            return False

    def IsOperatorLegal(self, i_Operator):
        for operator in self.m_LegalOperators:
            if operator != i_Operator:
                return False
        return True

    #########################################################################################
    # switch ["(", "{", "["] to array
    def areBracketsBalanced(self):
        stack = []
        for char in self.m_Query:
            if char == "(":
                stack.append(char)
            else:
                if char == ")":
                    if not stack:  # check if stack is empty.
                        return False
                    current_char = stack.pop()
                    if current_char == '(':
                        if char != ")":
                            return False

        # Check Empty Stack
        return not stack
