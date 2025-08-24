from enum import Enum

class PaymentStatus(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"

def simulate_payment(amount_cents: int, provider: str = "mock") -> dict:
    # simulation of payment gateway : success if > 0
    if amount_cents > 0:
        return {"status": PaymentStatus.success, "provider": provider}
    else:
        return {"status": PaymentStatus.failed, "provider": provider}