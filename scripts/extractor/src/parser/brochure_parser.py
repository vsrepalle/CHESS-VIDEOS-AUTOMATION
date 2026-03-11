import re


def parse_brochure(text):

    data = {}

    headline = re.search(r"ELITE RAPID OPEN.*?2026", text, re.I)
    if headline:
        data["headline"] = headline.group(0)

    date = re.search(r"Sunday.*?April.*?2026", text, re.I)
    if date:
        data["date"] = date.group(0)

    location = re.search(r"Sri Sai Garden.*?Hyderabad", text, re.I)
    if location:
        data["location"] = location.group(0)

    prize = re.search(r"Cash Prize.*?([\d,]+)", text, re.I)
    if prize:
        data["total_prize_pool_rupees"] = prize.group(1).replace(",", "")

    entry = re.search(r"Entry\s*Fee\s*₹?(\d+)", text, re.I)
    if entry:
        data["entry_fee_rupees"] = entry.group(1)

    phone = re.search(r"\b\d{10}\b", text)
    if phone:
        data["contact_number"] = phone.group(0)

    organiser = re.search(r"Organiser\s*:\s*(.*)", text)
    if organiser:
        data["organiser"] = organiser.group(1)

    return data