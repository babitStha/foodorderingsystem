def prepareMessageFor(name):
    template = """
Mr/Mrs [name], Welcome to Food Ordering System!

You are now part of the family! Get ready to enjoy amazing and delicious food with us !

To make things extra special for you, starting today, we will notify you the updates and information through email.

If you prefer something more personal, you can always contact our support team through live chat or at call at +977 9992554455.

Best Regards,
The Food Ordering System team
    """
    PLACEHOLDER = "[name]"
    message = template.replace(PLACEHOLDER, name)
    return message
