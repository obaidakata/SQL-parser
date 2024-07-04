# SQLParser
The project checks if a given query is a validate or not.

examples :
Assuming we have 2 schemas :

Customers(Name: STRING, Age: INTEGER)
Orders(CustomerName: STRING, Product: STRING, Price: INTEGER)

The code will return true for the following queries :
SELECT Customers.Name FROM Customers WHERE Customers.Age=25;
SELECT Customers.Name FROM Customers WHERE Customers.Name=’Mike’;


and false for the following queries :

-SELECT Customers.Name,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>1000; 
reason: The rounded brackets is not balanced

-SELECT Customers.Color,Orders.Price FROM Customers,Orders WHERE (Customers.Name=Orders.CustomerName) OR (Orders.Price>1000);
reson: Customers.Color doesnt exists.
