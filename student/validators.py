from django.core.exceptions import ValidationError

def validate_domain(domain):
    def validator(email):
        if email.split('@')[-1] != domain:
            raise ValidationError(f"Email must be from the domain '{domain}'.")
        return email
    return validator