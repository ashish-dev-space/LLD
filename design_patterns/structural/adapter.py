# Adapter Pattern
#
# Converts the interface of a class into another interface the client expects.
# Lets classes work together that otherwise couldn't due to incompatible interfaces.
#
# Use Case                      Why Adapter
# Third-party payment SDKs      Each SDK has a different API; unify behind one interface
# Legacy system integration     Old code has different method names/signatures
# Multiple cloud storage SDKs   S3, GCS, Azure Blob all differ; adapt to one interface
# Data format conversion        XML library exposed to a JSON-expecting client
from abc import ABC
from abc import abstractmethod


# ── Target Interface (what the client expects) ────────────────────────────────


class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


# ── Example 1 : Stripe Adapter ────────────────────────────────────────────────

# Adaptee — third-party Stripe SDK (incompatible interface, cannot be changed)
class StripeSDK:
    def charge_customer(self, usd_amount: float) -> None:
        print(f"[Stripe SDK] Charging ${usd_amount:.2f} via Stripe")


# Adapter — wraps StripeSDK, exposes the PaymentGateway interface
class StripeAdapter(PaymentGateway):
    def __init__(self):
        self._stripe = StripeSDK()

    def pay(self, amount: float) -> None:
        self._stripe.charge_customer(amount)


# ── Example 2 : PayPal Adapter ────────────────────────────────────────────────

# Adaptee — third-party PayPal SDK (different method name + signature)
class PayPalSDK:
    def send_payment(self, receiver: str, amount_usd: float) -> None:
        print(f"[PayPal SDK] Sending ${amount_usd:.2f} to {receiver}")


# Adapter — translates pay(amount) → send_payment(receiver, amount)
class PayPalAdapter(PaymentGateway):
    DEFAULT_RECEIVER = "merchant@store.com"

    def __init__(self):
        self._paypal = PayPalSDK()

    def pay(self, amount: float) -> None:
        self._paypal.send_payment(self.DEFAULT_RECEIVER, amount)


# ── Example 3 : Class Adapter (inheritance style) ─────────────────────────────


class RazorpaySDK:
    def deduct(self, inr_amount: float) -> None:
        print(f"[Razorpay SDK] Deducting ₹{inr_amount:.2f} via Razorpay")


# Inherits from both Target and Adaptee (multiple inheritance)
class RazorpayAdapter(PaymentGateway, RazorpaySDK):
    def pay(self, amount: float) -> None:
        self.deduct(amount)  # delegates to RazorpaySDK.deduct


# ── Client code ───────────────────────────────────────────────────────────────
# Works with PaymentGateway only — has no idea which SDK is underneath


class Checkout:
    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway

    def complete_order(self, amount: float) -> None:
        print(f"Processing order of ${amount:.2f}...")
        self._gateway.pay(amount)
        print("Order complete.\n")


# ── Driver Code ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Swap any adapter in — client code (Checkout) never changes
    Checkout(StripeAdapter()).complete_order(49.99)
    Checkout(PayPalAdapter()).complete_order(149.00)
    Checkout(RazorpayAdapter()).complete_order(999.00)

# Output:
# Processing order of $49.99...
# [Stripe SDK] Charging $49.99 via Stripe
# Order complete.
#
# Processing order of $149.00...
# [PayPal SDK] Sending $149.00 to merchant@store.com
# Order complete.
#
# Processing order of $999.00...
# [Razorpay SDK] Deducting ₹999.00 via Razorpay
# Order complete.
