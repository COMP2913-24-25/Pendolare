import stripe

# Set your secret API key
stripe.api_key = "sk_test_51R01XVJJfevYXm7DQZlpUnTFEirQaRSDQfy6TJZ3kBdf2oVXnjl3hV1TSzfUiiSdmuXuZoOP6tBlKsn9hJbkdha900jFkB9ZZ8"

id = "11857ed2-e4b2-41a3-aae7-de4966800f13"
josh = stripe.Customer.create(
    id = id,
    name = "Joshy Mundray",
    email = "oui@baguette.com",
)
print(josh)

print(josh.id)

josh2 = stripe.Customer.retrieve(id)

# Create a SetupIntent and attach the new payment method
pm_items = [
    "pm_card_visa",
    "pm_card_visa_debit",
    "pm_card_mastercard",
    "pm_card_mastercard_debit",
    "pm_card_mastercard_prepaid",
    "pm_card_amex",
    "pm_card_discover",
    "pm_card_diners",
    "pm_card_jcb",
    "pm_card_unionpay"
]

for method in pm_items:
    setup_intent = stripe.SetupIntent.create(
        customer=id,
        payment_method=method,
        confirm=True,
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never"
        }
    )

# Fetch saved payment methods (e.g., cards)
payment_methods = stripe.Customer.list_payment_methods(id)

# Print the response
print(payment_methods)



## PAYMENT FLOW
# https://www.youtube.com/watch?v=O6TWFuZw2uk
# Collect payment methods