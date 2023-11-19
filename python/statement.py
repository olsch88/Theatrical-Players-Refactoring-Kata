import math


BASE_FEE = {"tragedy": 40000, "comedy": 30000}
AUDIENCE_THRESHOLD = {"tragedy": 30, "comedy": 20}


def tragedy_payment(audience: int):
    this_amount = 40000
    if audience > 30:
        this_amount += 1000 * (audience - 30)
    return this_amount


def comedy_payment(audience: int):
    this_amount = 30000
    if audience > 20:
        this_amount += 10000 + 500 * (audience - 20)

    this_amount += 300 * audience
    return this_amount


def default_credits(audience: int):
    volume_credits = max(audience - 30, 0)
    return volume_credits


def comedy_credits(audience: int):
    volume_credits = max(audience - 30, 0)
    volume_credits += math.floor(audience / 5)
    return volume_credits


payment_methods = {"tragedy": tragedy_payment, "comedy": comedy_payment}
credits_methods = {"comedy": comedy_credits}


def format_as_dollars(amount: float):
    return f"${amount:0,.2f}"


def format_as_euros(amount: float):
    return f"€{amount:0,.2f}"


def default_output_formater(unformated_text: str):
    return unformated_text


def html_output_formater(unformated_text: str):
    # just an oversimplified version for demonstration
    """<head>
    <title> Statement</title>
    </head>
    <body>"""
    +unformated_text
    +""" </body>"""


def statement(
    invoice,
    plays,
    currency_format: callable,
    output_format: callable = default_output_formater,
):
    total_amount = 0
    volume_credits = 0
    statement_text = f'Statement for {invoice["customer"]}\n'

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        try:
            this_amount = payment_methods[play["type"]](perf["audience"])

        except KeyError:
            raise ValueError(f'unknown type: {play["type"]}')

        # add volume credits

        volume_credits += credits_methods.get(play["type"], default_credits)(
            perf["audience"]
        )

        # print line for this order
        statement_text += f' {play["name"]}: {currency_format(this_amount/100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    statement_text += f"Amount owed is {format_as_dollars(total_amount/100)}\n"
    statement_text += f"You earned {volume_credits} credits\n"
    return output_format(statement_text)
