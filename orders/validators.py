import phonenumbers
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    """
    Validates and formats phone numbers to E.164 format.
    Supports international numbers from any region.
    """
    try:
        # Try to parse the number as is
        parsed_number = phonenumbers.parse(value)
        
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError('Invalid phone number')
            
        # Return the E.164 formatted number
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
    except phonenumbers.NumberParseException:
        raise ValidationError('Please enter a valid phone number with country code')