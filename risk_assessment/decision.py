"""Deterministic educational threshold decisions; not validated underwriting policy."""

THRESHOLDS = {
    "individual": {"profit_maximization": 0.41, "risk_minimization": 0.21, "market_expansion": 0.50},
    "business": {"profit_maximization": 0.35, "risk_minimization": 0.15, "market_expansion": 0.45},
}


def recommend_loan(default_probability, borrower_type="individual", lender_goal="profit_maximization"):
    """Return a prototype recommendation based on the selected threshold.

    Unknown lender goals retain the original prototype's 0.5 fallback.
    This function alone does not establish model validity or credit eligibility.
    """
    threshold = THRESHOLDS[borrower_type].get(lender_goal, 0.5)
    return "Approve" if default_probability < threshold else "Deny"
