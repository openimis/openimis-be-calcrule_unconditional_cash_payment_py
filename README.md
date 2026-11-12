# openIMIS Backend calcrule_unconditional_cash_payment reference module

## Parameters
The payment plan `json_ext` (a JSON object, or a string holding one) must contain
`calculation_rule.lumpsum_to_be_paid` and `calculation_rule.invoice_label`. When either is
missing, the conversion of a policy into a bill fails with a `ValidationError` naming the payment
plan and the missing parameter.
