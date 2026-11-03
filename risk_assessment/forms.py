"""Prototype Django ModelForms; fields match current borrower models."""
from django import forms
from .models import IndividualBorrower, BusinessBorrower


class IndividualBorrowerForm(forms.ModelForm):
    class Meta:
        model = IndividualBorrower
        fields = ["income", "dti", "loan_amnt", "term", "int_rate", "grade", "sub_grade"]


class BusinessBorrowerForm(forms.ModelForm):
    class Meta:
        model = BusinessBorrower
        fields = ["name", "no_of_employees", "term", "disbursement_gross", "gross_approved", "sba_approved"]
