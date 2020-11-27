from SQLParser import SQLParser

def main():
    query_to_parse = "SELECT     Customers.Name   ,   Orders.Price    FROM    Customers,   Orders    WHERE Customers.Name=Orders.CustomerName AND y = 5 AND Orders.Price>1000 AND y = 3;"
    query_to_parse2 = "SELECT Customers.Name, Orders.Price FROM Customers, Orders WHERE (Customers.Name = Orders.CustomerName) OR(Orders.Price > 59);"

    validSQL = open('valid.txt', 'r')
    validQueries = validSQL.readlines()
    print("All shoud be valid")
    for query in validQueries:
        sql = SQLParser(query)
        if not sql.IsQueryValid():
            sql.Print()

    validSQL = open('invalid.txt', 'r')
    validQueries = validSQL.readlines()
    print("All shoud be invalid")
    for query in validQueries:
        sql = SQLParser(query)
        if sql.IsQueryValid():
            sql.Print()

if __name__ == '__main__':
    main()
