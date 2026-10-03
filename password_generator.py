import random
import re
import secrets
import string

CATEGORY_MAP = {
    1: "uppercase",
    2: "lowercase",
    3: "numbers",
    4: "symbols",
}

CHARACTER_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": string.punctuation,
}

AMBIGUOUS_CHARACTERS = set("0OIl1|`!{}[]()\\/" )


def validate_length(raw_value):
    if raw_value is None:
        raise ValueError("Invalid length!\nPassword length must be at least 8 characters.")

    value = str(raw_value).strip()
    if not value:
        raise ValueError("Invalid length!\nPassword length must be at least 8 characters.")

    if not re.fullmatch(r"-?\d+", value):
        raise ValueError("Invalid length!\nPassword length must be at least 8 characters.")

    length = int(value)
    if length < 8 or length == 0:
        raise ValueError("Invalid length!\nPassword length must be at least 8 characters.")

    return length


def parse_character_choices(raw_choices):
    if raw_choices is None:
        raise ValueError("Invalid selection! Please choose at least two valid character types.")

    cleaned = str(raw_choices).strip()
    if not cleaned:
        raise ValueError("No selection made. Please choose at least two character types.")

    selected_numbers = []
    for item in re.split(r"[\s,]+", cleaned):
        if not item:
            continue
        if not item.isdigit():
            raise ValueError("Invalid choices! Please select numbers from 1 to 4 only.")
        number = int(item)
        if number not in CATEGORY_MAP:
            raise ValueError("Invalid choices! Please select numbers from 1 to 4 only.")
        if number in selected_numbers:
            raise ValueError("Duplicate selection found. Please avoid repeating choices.")
        selected_numbers.append(number)

    if len(selected_numbers) < 2:
        raise ValueError("Please select at least two character types.")

    return [CATEGORY_MAP[number] for number in selected_numbers]


def get_allowed_characters(selected_types, exclude_ambiguous=False):
    result = "".join(CHARACTER_SETS[character_type] for character_type in selected_types)
    if exclude_ambiguous:
        result = "".join(ch for ch in result if ch not in AMBIGUOUS_CHARACTERS)
    return result


def generate_password(length, selected_types, exclude_ambiguous=False, secure=False):
    if not isinstance(length, int) or length < 8:
        raise ValueError("Invalid length!\nPassword length must be at least 8 characters.")
    if len(selected_types) < 2:
        raise ValueError("Please select at least two character types.")

    required_characters = []
    valid_characters = []

    for character_type in selected_types:
        charset = CHARACTER_SETS[character_type]
        if exclude_ambiguous:
            charset = "".join(ch for ch in charset if ch not in AMBIGUOUS_CHARACTERS)
        if not charset:
            raise ValueError(f"No valid characters available for {character_type} after exclusion.")
        required_characters.append(secrets.choice(charset) if secure else random.choice(charset))
        valid_characters.append(charset)

    all_characters = "".join(valid_characters)
    if exclude_ambiguous:
        all_characters = "".join(ch for ch in all_characters if ch not in AMBIGUOUS_CHARACTERS)

    password_chars = required_characters[:]
    remaining_slots = length - len(password_chars)
    for _ in range(remaining_slots):
        password_chars.append(secrets.choice(all_characters) if secure else random.choice(all_characters))

    if secure:
        secrets.SystemRandom().shuffle(password_chars)
    else:
        random.shuffle(password_chars)

    return "".join(password_chars)


def password_strength(password):
    score = 0
    if any(ch.isupper() for ch in password):
        score += 1
    if any(ch.islower() for ch in password):
        score += 1
    if any(ch.isdigit() for ch in password):
        score += 1
    if any(not ch.isalnum() for ch in password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score >= 5:
        return "STRONG"
    if score >= 3:
        return "MEDIUM"
    return "WEAK"
