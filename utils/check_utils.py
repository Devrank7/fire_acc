import phonenumbers
from email_validator import EmailNotValidError, validate_email


def is_valid_email_or_phone(s: str, regions=None) -> bool:
    # Проверка email
    if regions is None:
        regions = ["RU", "UA", "US", "IL"]
    try:
        validate_email(s)
        return True
    except EmailNotValidError:
        pass

    # Проверка номера телефона для каждого региона
    for region in regions:
        try:
            phone = phonenumbers.parse(s, region)
            if phonenumbers.is_valid_number(phone):
                return True
        except phonenumbers.NumberParseException:
            continue

    return False
