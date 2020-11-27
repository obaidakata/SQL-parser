from SQLParser import SQLParser

def main():
    query_to_parse = "SELECT     Customers.Name   ,   Orders.Price    FROM    Customers,   Orders    WHERE Customers.Name=Orders.CustomerName AND y = 5 AND Orders.Price>1000 AND y = 3;"
    query_to_parse2 = "SELECT Customers.Name, Orders.Price FROM Customers, Orders WHERE (Customers.Name = Orders.CustomerName) OR(Orders.Price > 59);"
    file1 = open('test.txt', 'r')
    queries = file1.readlines()
    for query in queries:
        sql = SQLParser(query)
        if not sql.IsQueryValid():
            sql.Print()


    # sql = SQLParser(query_to_parse2)
    # if sql.IsQueryValid():
    #     sql.Print()
    # else:
    #     print("Errrrrororor")
    #
    #     # print("Parsing <condition> failed")
    #     # print("Parenthess are not balanced.")
    #     # print("Invalid")
    # # print(sql_parser.IsQueryValid())

if __name__ == '__main__':
    main()
