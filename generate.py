import json
import random

# Helper lists
FIRST_NAMES = [
    "aditya", "neha", "sanjay", "deepak", "ananya", "rahul", "rakesh",
    "pratik", "meera", "sahana", "vikram", "kiran", "pooja", "ramesh"
]
LAST_NAMES = [
    "rao", "dubey", "krishnan", "singh", "mehta", "sharma", "joshi",
    "iyer", "patel", "verma"
]

CITIES = [
    "mumbai", "delhi", "bangalore", "chennai", "hyderabad",
    "pune", "kolkata", "coimbatore", "gurgaon", "singapore"
]

LOCATIONS = [
    "andheri east", "powai", "whitefield", "bandra west", "btm layout",
    "silk board junction", "fortis hospital", "lakeview apartments"
]

EMAIL_DOMAINS = ["gmail", "yahoo", "outlook", "hotmail", "example"]

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

ORDINALS = {
    1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
    6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
    11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth",
    15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth",
    19: "nineteenth", 20: "twentieth", 21: "twenty first",
    22: "twenty second", 23: "twenty third", 24: "twenty fourth",
    25: "twenty fifth", 26: "twenty sixth", 27: "twenty seventh",
    28: "twenty eighth", 29: "twenty ninth", 30: "thirtieth",
    31: "thirty first"
}

DIGIT_WORDS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
}


def digits_to_stt(digits: str) -> str:
    """Convert a string of digits to STT-style spaced words."""
    return " ".join(DIGIT_WORDS[d] for d in digits)


def make_phone_stt() -> str:
    # basic indian style 10 digit starting from 6-9
    first = random.choice(["6", "7", "8", "9"])
    rest = "".join(random.choice("0123456789") for _ in range(9))
    return digits_to_stt(first + rest)


def make_card_stt() -> str:
    digits = "".join(random.choice("0123456789") for _ in range(16))
    return digits_to_stt(digits)


def year_to_words(year: int) -> str:
    """Rough 'two thousand twenty four' style for 2000-2099."""
    if 2000 <= year <= 2099:
        last_two = year % 100
        tens = last_two // 10
        ones = last_two % 10
        tens_word = {
            0: "zero", 1: "ten", 2: "twenty", 3: "thirty",
            4: "forty", 5: "fifty", 6: "sixty", 7: "seventy",
            8: "eighty", 9: "ninety"
        }[tens]
        if ones == 0:
            last = tens_word
        else:
            last = tens_word + " " + DIGIT_WORDS[str(ones)]
        return "two thousand " + last
    return str(year)


def make_date_phrase() -> str:
    day = random.randint(1, 28)
    month = random.choice(MONTHS)
    year = random.choice([2023, 2024, 2025])
    return f"{ORDINALS[day]} {month} {year_to_words(year)}"


def make_person_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"


def make_email_stt(first: str, last: str) -> str:
    # 'aditya dot rao at gmail dot com'
    domain = random.choice(EMAIL_DOMAINS)
    return f"{first} dot {last} at {domain} dot com"


def span(text: str, substr: str, label: str):
    start = text.index(substr)
    end = start + len(substr)
    return {"start": start, "end": end, "label": label}


def pattern_name_city_email_phone_date(idx: int):
    name = make_person_name()
    first, last = name.split()
    city = random.choice(CITIES)
    email = make_email_stt(first, last)
    phone = make_phone_stt()
    date = make_date_phrase()
    text = (
        f"my name is {name} i am calling from {city} "
        f"my email is {email} "
        f"my phone number is {phone} "
        f"and the booking date is {date}"
    )
    entities = [
        span(text, name, "PERSON_NAME"),
        span(text, city, "CITY"),
        span(text, email, "EMAIL"),
        span(text, phone, "PHONE"),
        span(text, date, "DATE"),
    ]
    return {"id": f"utt_{2000+idx}", "text": text, "entities": entities}


def pattern_card_name_date(idx: int):
    name = make_person_name()
    card = make_card_stt()
    date = make_date_phrase()
    text = (
        "please update my credit card details the card number is "
        f"{card} "
        f"the name on card is {name} and it expires on {date}"
    )
    entities = [
        span(text, card, "CREDIT_CARD"),
        span(text, name, "PERSON_NAME"),
        span(text, date, "DATE"),
    ]
    return {"id": f"utt_{2100+idx}", "text": text, "entities": entities}


def pattern_travel_city_date_location(idx: int):
    city_from = random.choice(CITIES)
    city_to = random.choice([c for c in CITIES if c != city_from])
    loc_from = random.choice(LOCATIONS)
    date = make_date_phrase()
    text = (
        f"i want to book a cab from {loc_from} {city_from} to {city_to} "
        f"on {date} around ten thirty in the morning"
    )
    entities = [
        span(text, loc_from, "LOCATION"),
        span(text, city_from, "CITY"),
        span(text, city_to, "CITY"),
        span(text, date, "DATE"),
    ]
    return {"id": f"utt_{2200+idx}", "text": text, "entities": entities}


def pattern_phone_only(idx: int):
    name = make_person_name()
    phone = make_phone_stt()
    text = (
        f"this is {name} my contact number is {phone} please call me back"
    )
    entities = [
        span(text, name, "PERSON_NAME"),
        span(text, phone, "PHONE"),
    ]
    return {"id": f"utt_{2300+idx}", "text": text, "entities": entities}


def pattern_email_only(idx: int):
    name = make_person_name()
    first, last = name.split()
    email = make_email_stt(first, last)
    text = (
        f"you can send the invoice to {email} do not share it on whatsapp"
    )
    entities = [
        span(text, email, "EMAIL"),
    ]
    return {"id": f"utt_{2400+idx}", "text": text, "entities": entities}


def pattern_city_location_non_pii(idx: int):
    city = random.choice(CITIES)
    loc = random.choice(LOCATIONS)
    text = f"the office is near {loc} in {city} close to the main road"
    entities = [
        span(text, loc, "LOCATION"),
        span(text, city, "CITY"),
    ]
    return {"id": f"utt_{2500+idx}", "text": text, "entities": entities}


def pattern_date_dob_phone(idx: int):
    phone = make_phone_stt()
    date = make_date_phrase()
    text = (
        f"my registered mobile is {phone} "
        f"and my date of birth is {date}"
    )
    entities = [
        span(text, phone, "PHONE"),
        span(text, date, "DATE"),
    ]
    return {"id": f"utt_{2600+idx}", "text": text, "entities": entities}


def pattern_meeting_date_city(idx: int):
    date = make_date_phrase()
    city = random.choice(CITIES)
    text = (
        f"schedule a zoom meeting on {date} with the team in {city} office"
    )
    entities = [
        span(text, date, "DATE"),
        span(text, city, "CITY"),
    ]
    return {"id": f"utt_{2700+idx}", "text": text, "entities": entities}


def pattern_negative_no_pii(idx: int):
    text = "the internet connection is very slow today can you please check"
    entities = []
    return {"id": f"utt_{2800+idx}", "text": text, "entities": entities}


PATTERNS = [
    pattern_name_city_email_phone_date,
    pattern_card_name_date,
    pattern_travel_city_date_location,
    pattern_phone_only,
    pattern_email_only,
    pattern_city_location_non_pii,
    pattern_date_dob_phone,
    pattern_meeting_date_city,
    pattern_negative_no_pii,
]


def main(output_path: str = "data/dev_synth.jsonl", n_examples: int = 150):
    random.seed(42)
    examples = []
    for i in range(n_examples):
        pattern_fn = random.choice(PATTERNS)
        ex = pattern_fn(i)
        examples.append(ex)

    with open(output_path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
