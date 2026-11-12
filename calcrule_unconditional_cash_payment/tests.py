from django.core.exceptions import ValidationError
from django.test import TestCase

from calcrule_unconditional_cash_payment.calculation_rule import UnconditionalCashPaymentCalculationRule
from contribution_plan.models import PaymentPlan


class UnconditionalCashPaymentRuleTest(TestCase):
    """OP-3322: payment plan params are parsed, never substring-matched, and checked."""

    rule = UnconditionalCashPaymentCalculationRule

    def test_params_from_a_dict(self):
        payment_plan = PaymentPlan(json_ext={"calculation_rule": {"lumpsum_to_be_paid": 50, "invoice_label": "UC"}})
        self.assertEqual(self.rule._get_data_from_json_ext(payment_plan), {"lumpsum_to_be_paid": 50, "invoice_label": "UC"})

    def test_params_from_a_json_string(self):
        payment_plan = PaymentPlan(json_ext='{"calculation_rule": {"lumpsum_to_be_paid": 50, "invoice_label": "UC"}}')
        self.assertEqual(self.rule._get_data_from_json_ext(payment_plan), {"lumpsum_to_be_paid": 50, "invoice_label": "UC"})

    def test_a_string_mentioning_calculation_rule_is_not_params(self):
        # the raw text contains "calculation_rule", but not as a key holding the params
        payment_plan = PaymentPlan(json_ext='{"note": "calculation_rule"}')
        self.assertEqual(self.rule._get_data_from_json_ext(payment_plan), {})

    def test_no_params(self):
        for json_ext in (None, "", {}, {"calculation_rule": None}):
            with self.subTest(json_ext=json_ext):
                self.assertEqual(self.rule._get_data_from_json_ext(PaymentPlan(json_ext=json_ext)), {})

    def test_conversion_without_lumpsum_fails_clearly(self):
        payment_plan = PaymentPlan(code="UCPP", json_ext={})
        with self.assertRaises(ValidationError):
            self.rule._convert_policies('Bill', payment_plan, None, {"invoice_label": "UC"})
