def orderCancelMessage(name):
    template = """
                      Your package has been cancelled!
Hi [name],

Sorry to be the bearer of bad news, but your order # [transaction_id] was cancelled. You can reorder foods from our site.
Thank You,
    """
    PLACEHOLDER = "[name]"
    message = template.replace(PLACEHOLDER, name)
    return message


def orderPlacedMessage(name):
    template = """
                      Your Ordrer has been cancelled!
Hi [name],

Your Order has been Placed.
 You can order more foods from our site.

Thank You For Choosing Us,
The Food Ordering System TEAM
    """
    PLACEHOLDER = "[name]"
    message = template.replace(PLACEHOLDER, name)
    return message
