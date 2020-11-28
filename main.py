from SQLParser import SQLParser

def main():
    queryToParse = input("Enter your query: ")
    sql = SQLParser(queryToParse)
    if sql.IsQueryValid():
        print("Query valid")
    else:
        print("Query invalid")

if __name__ == '__main__':
    main()
