import africastalking
import phonenumbers
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)

def send_sms(phone_number: str, message: str) -> str:
    """
    Sends an SMS to the specified phone number using the Africa's Talking API.

    Args:
    phone_number (str): The recipient's phone number in international format (e.g., "+1234567890").
    message (str): The content of the SMS to be sent.

    Returns:
    str: A success message if the SMS is sent successfully.

    Raises:
    ValueError: If the phone number is invalid.
    RuntimeError: If there's an error sending the SMS.

    Note:
    This function assumes that the Africa's Talking API credentials are set up correctly.
    """
    try:
        # Try to parse with the number's own region info first
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except phonenumbers.NumberParseException:
            # If that fails, try to parse assuming it's a local number
            # This will work for numbers without country code
            for region in phonenumbers.SUPPORTED_REGIONS:
                try:
                    parsed_number = phonenumbers.parse(phone_number, region)
                    if phonenumbers.is_valid_number(parsed_number):
                        break
                except phonenumbers.NumberParseException:
                    continue
            else:
                raise ValueError("Could not determine the region for this number")
        
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")

        normalized_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )

        # Initialize the Africa's Talking SMS service
        sms = africastalking.SMS

        # Send the SMS
        response = sms.send(message, [normalized_number])
        
        # Get the recipients data from the response
        sms_data = response.get("SMSMessageData", {})
        recipients = sms_data.get("Recipients", [])
        
        if recipients:
            recipient = recipients[0]
            status = recipient.get("status")
            message_id = recipient.get("messageId")
            cost = recipient.get("cost")
            
            if status.lower() == "success":
                logger.info(f"SMS sent successfully to {phone_number}. MessageID: {message_id}, Cost: {cost}")
                return "SMS sent successfully"
            else:
                logger.error(f"Failed to send SMS. Status: {status}")
                return f"Failed to send SMS: {status}"
        else:
            logger.error("No recipient data in response")
            return "Failed to send SMS: No recipient data"

    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number format")
    except Exception as e:
        # we dont need to stop excution because sms didnt send so we can just log it
        logger.error(f"Error sending SMS: {str(e)}")
        return
