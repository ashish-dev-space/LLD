# The Singleton Pattern is a creational design pattern that ensures:
# 1️⃣ Only one instance of a class exists in the application
# 2️⃣ A global access point to that instance is provided
# In simple words:
# No matter how many times you create the object, the system always returns the same object.
# Use Case                  Why Singleton
# Logger                    Avoid multiple loggers writing simultaneously
# Configuration Manager     One shared configuration
# Database Connection Pool  Prevent multiple connections being created
# Cache Manager             Shared cache across application
# Feature Flag Manager      Same configuration across services


class Logger:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def log(self, message):
        print(f"[LOG]: {message}")


# logger1 = Logger()
# logger2 = Logger()

# logger1.log("User logged in")
# logger2.log("Payment completed")

# print(logger1 is logger2)

# Output:
# [LOG]: User logged in
# [LOG]: Payment completed
# True


import sqlite3


class DBManager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new database connection")
            cls._instance = super().__new__(cls)
            cls._instance.connection = sqlite3.connect("app.db")
        return cls._instance

    def get_connection(self):
        return self.connection


# db1 = DBManager()
# db2 = DBManager()
# print(db1.get_connection())
# print(db2.get_connection())

# Output:
# Creating new database connection
# <sqlite3.Connection object at 0x7f8c2c3e50>
# <sqlite3.Connection object at 0x7f8c2c3e50>
