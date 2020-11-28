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
        self.m_LegalOperators = ["<=", ">=", "<>", "<", ">", "="]

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
            print("Parsing <", words[len - 1], "> failed")
            return False
        else:
            return self.select_parse_Helper(words, len - 1)

    def checkIfSelectedColumnNameIsValid(self, i_columnName):
        i_columnName = i_columnName.replace(" ", "")
        if i_columnName == "*":
            return True
        elif i_columnName == "DISTINCT":
            return True
        else:
            for x in self.m_Schema:
                if i_columnName == x:
                    return True
                for y in self.m_Schema[x]:
                    if i_columnName == x + "." + y:
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
            # Maybe there is easier way
            str1 = ''.join(str(e) + " " for e in words)
            strToPrint = str1.split("FROM")
            strToPrint[1] = strToPrint[1].strip()
            print("Parsing <", strToPrint[1], "> failed")
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
        query = self.m_Query.split("WHERE")
        where_sub_query = query[1].strip().strip(";")

        if not self.areBracketsBalanced(where_sub_query):
            print("Parsing <", where_sub_query, "> failed")
            return False
        return self.where_parse_helper(where_sub_query)

    def where_parse_helper(self, i_Query):
        if i_Query is None:
            return False
        elif len(i_Query) == 1:
            return False
        elif self.IsSimpleCondition(i_Query):
            isConditionValid = self.checkCondition(i_Query)
            if not isConditionValid:
                print("Parsing <", i_Query, "> failed")
            return isConditionValid
        else:
            splittedCondition = self.splitCondition(i_Query)
            if splittedCondition is not None:
                leftSubCondition = self.checkCondition(splittedCondition[0])
                if not leftSubCondition:
                    print("Parsing <", i_Query, "> failed")
                    return False
                else:
                    rightSubCondition = self.where_parse_helper(splittedCondition[2])
                    return (leftSubCondition is not None) and rightSubCondition
            else:
                return False

    def splitCondition(self, condition):
        firstAnd = None
        firstOR = None
        toAdd = None
        minIndex = None
        if "AND" in condition:
            firstAnd = condition.find("AND")
        if "OR" in condition:
            firstOR = condition.find("OR")

        if firstAnd is None and firstOR is not None:
            minIndex = firstOR
            toAdd = 2
        elif firstOR is None and firstAnd is not None:
            minIndex = firstAnd
            toAdd = 3
        elif firstOR is not None and firstAnd is not None:
            if firstAnd < firstOR:
                toAdd = 3
                minIndex = firstAnd
            else:
                toAdd = 2
                minIndex = firstOR
        else:
            print("Error")
            return None

        if toAdd is None:
            print("Error")
            return None
        else:
            leftCondition = condition[0:minIndex].strip(" ")
            logicOperator = condition[minIndex:minIndex + toAdd]
            rightCondition = condition[minIndex + toAdd:len(condition)].strip(" ")
            return [leftCondition, logicOperator, rightCondition]

    def IsSimpleCondition(self, condition):
        andExist = "AND" in condition
        orExist = "OR" in condition
        return (not andExist) and (not orExist)

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
            # check if not double check
            isLeftOperandValid = self.checkIfSelectedColumnNameIsValid(leftOperand)
            isRightOperandValid = self.checkTypes(leftOperand, rightOperand)
            return isLeftOperandValid and isRightOperandValid

        return False

    def checkTypes(self, leftOperand, rightOperand):
        leftOperandType = self.getOperandType(leftOperand)
        rightOperandType = self.getOperandType(rightOperand)
        return leftOperandType == rightOperandType

    def IsOperatorLegal(self, i_Operator):
        for operator in self.m_LegalOperators:
            if operator != i_Operator:
                return False
        return True

    def getOperandType(self, operand):
        if operand.isdecimal():
            return "int"
        elif self.isString(operand):
            return "string"
        else:
            sp = operand.split(".")
            typeAsString = None
            if sp[0] in self.m_Schema:
                if (sp[1] in self.m_Schema[sp[0]]):
                    typeAsString = self.m_Schema[sp[0]][sp[1]]
            if typeAsString is not None:
                return typeAsString

    def isString(self, toCheck):
        if '"' in toCheck:
            toCheck = toCheck.replace('"', '')
        if '\'' in toCheck:
            toCheck = toCheck.replace('\'', '')
        if '’' in toCheck:
            toCheck = toCheck.replace('’', '')

        return toCheck.isalpha()


    #########################################################################################
    def areBracketsBalanced(self, i_Query):
        stack = []
        for char in i_Query:
            if char == "(":
                stack.append(char)
            else:
                if char == ")":
                    if not stack:  # check if stack is empty.
                        return False
                    stack.pop()

        # Check Empty Stack
        if stack:
            return False
        return True