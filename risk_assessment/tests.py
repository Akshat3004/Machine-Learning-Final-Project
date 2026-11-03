"""Focused unit tests for the decision layer and borrower form schemas.

Model inference is intentionally excluded until preprocessing is validated
against the persisted estimators' feature expectations.
"""
from django.test import SimpleTestCase

from .decision import recommend_loan
from .forms import IndividualBorrowerForm, BusinessBorrowerForm


class DecisionRuleTests(SimpleTestCase):
    def test_individual_risk_minimization(self):
        self.assertEqual(recommend_loan(0.20, "individual", "risk_minimization"), "Approve")
        self.assertEqual(recommend_loan(0.21, "individual", "risk_minimization"), "Deny")

    def test_business_threshold(self):
        self.assertEqual(recommend_loan(0.34, "business", "profit_maximization"), "Approve")
        self.assertEqual(recommend_loan(0.35, "business", "profit_maximization"), "Deny")

    def test_goal_changes_decision(self):
        self.assertEqual(recommend_loan(0.3, "individual", "risk_minimization"), "Deny")
        self.assertEqual(recommend_loan(0.3, "individual", "market_expansion"), "Approve")


class FormSchemaTests(SimpleTestCase):
    def test_individual_fields_exist(self):
        self.assertTrue({"income", "dti", "loan_amnt", "term"}.issubset(IndividualBorrowerForm.base_fields))

    def test_business_fields_exist(self):
        self.assertTrue({"name", "no_of_employees", "gross_approved"}.issubset(BusinessBorrowerForm.base_fields))
