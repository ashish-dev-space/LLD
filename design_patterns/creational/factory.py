# Factory Pattern
#
# Creates objects without exposing the instantiation logic to the client.
# The client asks a factory for an object by type; the factory decides
# which concrete class to instantiate.
#
# Use Case                  Why Factory
# Notifications             Different channels (email, SMS, push)
# Payment Processing        Different gateways (Stripe, PayPal, Razorpay)
# Data Parsers              Different file formats (JSON, XML, CSV)
# Logistics                 Different transport modes (road, air, sea)
from abc import ABC
from abc import abstractmethod
from typing import Callable


# ── Example 1 : Notification ──────────────────────────────────────────────────


class Notification(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotification(Notification):
    def send(self, message: str):
        print(f"[Email] {message}")


class SMSNotification(Notification):
    def send(self, message: str):
        print(f"[SMS] {message}")


class PushNotification(Notification):
    def send(self, message: str):
        print(f"[Push] {message}")


class NotificationFactory:
    # Adding a new channel = one new dict entry, zero logic changes
    _registry: dict[str, Callable[[], Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @staticmethod
    def get(channel: str) -> Notification:
        cls = NotificationFactory._registry.get(channel.lower())
        if cls is None:
            raise ValueError(f"Unknown notification channel: {channel}")
        return cls()


class NotificationService:
    def notify(self, channel: str, message: str):
        NotificationFactory.get(channel).send(message)


# ── Example 2 : Payment Gateway ───────────────────────────────────────────────


class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass


class StripeGateway(PaymentGateway):
    def pay(self, amount: float):
        print(f"[Stripe] Charged ${amount:.2f}")


class PayPalGateway(PaymentGateway):
    def pay(self, amount: float):
        print(f"[PayPal] Charged ${amount:.2f}")


class RazorpayGateway(PaymentGateway):
    def pay(self, amount: float):
        print(f"[Razorpay] Charged ₹{amount:.2f}")


class PaymentFactory:
    _registry: dict[str, Callable[[], PaymentGateway]] = {
        "stripe": StripeGateway,
        "paypal": PayPalGateway,
        "razorpay": RazorpayGateway,
    }

    @staticmethod
    def get(provider: str) -> PaymentGateway:
        cls = PaymentFactory._registry.get(provider.lower())
        if cls is None:
            raise ValueError(f"Unknown payment provider: {provider}")
        return cls()


class PaymentService:
    def charge(self, provider: str, amount: float):
        PaymentFactory.get(provider).pay(amount)


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    notifier = NotificationService()
    notifier.notify("email", "Your order has been placed.")
    notifier.notify("sms", "Your OTP is 482910.")
    notifier.notify("push", "Flash sale starts now!")

    print()

    payments = PaymentService()
    payments.charge("stripe", 49.99)
    payments.charge("paypal", 149.00)
    payments.charge("razorpay", 999.00)

# Output:
# [Email] Your order has been placed.
# [SMS] Your OTP is 482910.
# [Push] Flash sale starts now!
#
# [Stripe] Charged $49.99
# [PayPal] Charged $149.00
# [Razorpay] Charged ₹999.00
