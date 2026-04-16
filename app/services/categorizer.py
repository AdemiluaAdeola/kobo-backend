"""
Rule-based transaction categorizer for Nigerian bank SMS descriptions.
Matches patterns like 'POS PURCHASE JUMIA', 'TRANSFER TO OLAOLUWA', etc.
"""
import re


# Category rules: (pattern, category, base_confidence)
CATEGORY_RULES: list[tuple[str, str, float]] = [
    # Food & Dining
    (r"jumia\s*food|uber\s*eats|chowdeck|food|restaurant|eatery|suya|shawarma", "Food & Dining", 0.92),
    # Transport
    (r"bolt|uber|taxify|indriver|bus|brt|transport|fuel|petrol|filling\s*station", "Transport", 0.90),
    # Shopping
    (r"jumia|konga|shoprite|spar|mall|market|pos\s*purchase", "Shopping", 0.85),
    # Bills & Utilities
    (r"dstv|gotv|startimes|ikeja\s*electric|eko\s*disco|nepa|phcn|electricity|water\s*bill|airtime|mtn|glo|airtel|9mobile|data", "Bills & Utilities", 0.93),
    # Transfer
    (r"transfer\s*to|trf\s*to|nip\s*trf|sent\s*to", "Transfer", 0.88),
    # Salary / Income
    (r"salary|wage|payroll|nip\s*cr|credit\s*alert|received\s*from", "Income", 0.91),
    # Savings
    (r"piggyvest|cowrywise|kuda\s*save|save|savings|investment", "Savings & Investment", 0.89),
    # ATM
    (r"atm|withdrawal|cash", "ATM Withdrawal", 0.94),
    # Entertainment
    (r"netflix|spotify|showmax|cinema|bet9ja|sportybet|betking|1xbet", "Entertainment", 0.90),
    # Health
    (r"pharmacy|hospital|clinic|medical|health", "Health", 0.87),
    # Education
    (r"school|tuition|course|udemy|coursera|education", "Education", 0.88),
]


def categorize_transaction(description: str) -> tuple[str, float]:
    """
    Categorize a transaction based on its description.

    Returns:
        (category, confidence_score)
    """
    desc_lower = description.lower().strip()

    for pattern, category, confidence in CATEGORY_RULES:
        if re.search(pattern, desc_lower):
            return category, confidence

    return "Uncategorized", 0.50
