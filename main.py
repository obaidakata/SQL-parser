from SQLParser import SQLParser

def main():
    validSQL = open('valid.txt', 'r')
    validQueries = validSQL.readlines()
    print("All should be valid")
    for query in validQueries:
        sql = SQLParser(query)
        if not sql.IsQueryValid():
            sql.Print()

    # validSQL = open('invalid.txt', 'r')
    # validQueries = validSQL.readlines()
    # print("All should be invalid")
    # for query in validQueries:
    #     sql = SQLParser(query)
    #     if sql.IsQueryValid():
    #         sql.Print()

if __name__ == '__main__':
    main()
