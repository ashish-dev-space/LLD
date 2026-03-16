# Factory Pattern
# Creates objects without exposing the creation logic
# # The Factory Pattern is a creational design pattern that
# provides an interface for creating objects but allows
# subclasses to alter the type of objects that will be created.
# In simpler terms:
# Rather than calling a constructor directly to create an
# object, we use a factory method to create that object
# based on some input or condition.
# Use Case                  Why Factory
# Notifications             Different notification types (email, SMS, push)
# Payment Processing        Different payment gateways (Stripe, PayPal)
# Data Parsers              Different file formats (JSON, XML, CSV)
# Logistics Interface
from abc import ABC
from abc import abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self):
        pass


# Class implementing the Notification Interface
class EmailNotification(Notification):
    def send(self):
        print("Sending email notification")


# Class implementing the Notification Interface
class SMSNotification(Notification):
    def send(self):
        print("Sending SMS notification")


# Factory Class taking care of Logistics
class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
    }

    @staticmethod
    def get_service(mode):
        cls = NotificationFactory._registry.get(mode.lower())
        if cls is None:
            raise ValueError(f"Unknown notification mode: {mode}")
        return cls()


# Class implementing the Notification Services
class NotificationService:
    def send(self, mode):
        # Using the Notification Factory to get the desired object based on the mode
        notification = NotificationFactory.get_service(mode)
        notification.send()


# Driver Code
if __name__ == "__main__":
    service = NotificationService()
    service.send("email")
    service.send("sms")
