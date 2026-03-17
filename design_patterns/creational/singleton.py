# Singleton Pattern
#
# Ensures a class has only ONE instance and provides a global access point to it.
# No matter how many times you call the constructor, you always get the same object.
#
# Use Case                  Why Singleton
# Logger                    Avoid multiple loggers writing simultaneously
# Configuration Manager     One shared config loaded once
# Database Connection Pool  Prevent redundant connections
# Cache Manager             Shared in-memory cache across the app
# Feature Flag Manager      Same flags visible everywhere
import sqlite3


# ── Example 1 : Logger ────────────────────────────────────────────────────────


class Logger:
    _instance: "Logger | None" = None
    _logs: list[str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._logs = []
        return cls._instance

    def log(self, message: str):
        self._logs.append(message)
        print(f"[LOG] {message}")

    def history(self):
        return self._logs


# ── Example 2 : Database Connection Manager ───────────────────────────────────


class DBManager:
    _instance: "DBManager | None" = None
    _connection: sqlite3.Connection

    def __new__(cls):
        if cls._instance is None:
            print("[DB] Opening new connection...")
            cls._instance = super().__new__(cls)
            cls._instance._connection = sqlite3.connect(":memory:")
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        return self._connection


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Logger — both variables point to the same instance
    logger1 = Logger()
    logger2 = Logger()

    logger1.log("User logged in")
    logger2.log("Payment completed")

    print(f"Same logger instance : {logger1 is logger2}")  # True
    print(f"Log history          : {logger1.history()}")
    print()

    # DBManager — connection is created only once
    db1 = DBManager()
    db2 = DBManager()

    print(f"Same DB instance     : {db1 is db2}")  # True
    print(
        f"Same connection obj  : {db1.get_connection() is db2.get_connection()}"
    )  # True

# Output:
# [LOG] User logged in
# [LOG] Payment completed
# Same logger instance : True
# Log history          : ['User logged in', 'Payment completed']
#
# [DB] Opening new connection...
# Same DB instance     : True
# Same connection obj  : True
