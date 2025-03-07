import stripe

# Set your secret API key
stripe.api_key = "sk_test_51R01XVJJfevYXm7DQZlpUnTFEirQaRSDQfy6TJZ3kBdf2oVXnjl3hV1TSzfUiiSdmuXuZoOP6tBlKsn9hJbkdha900jFkB9ZZ8"

id = "11856ed2-e4b2-41a3-aae7-de4966800e98"
josh = stripe.Customer.create(
    id = id,
    name = "Joshy Mundray",
    email = "oui@baguette.com",
)
print(josh)

print(josh.id)

josh2 = stripe.Customer.retrieve(id)

# Create a SetupIntent and attach the new payment method
setup_intent = stripe.SetupIntent.create(
    customer=id,
    payment_method="pm_card_visa_debit",
    confirm=True
)

# Fetch saved payment methods (e.g., cards)
payment_methods = stripe.Customer.list_payment_methods(id)

# Print the response
print(payment_methods)



## PAYMENT FLOW
# https://www.youtube.com/watch?v=O6TWFuZw2uk
# Collect payment methods