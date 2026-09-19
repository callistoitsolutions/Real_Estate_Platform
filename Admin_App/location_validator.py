import requests


def verify_pincode_location(pincode, state=None, city=None, locality=None, city_label="City"):
    """
    Cross-references pincode/state/city (or district) against India Post's
    real records — the external source of truth for all 10 active property
    forms sharing this validator.

    city_label: what to call the "city" field in error messages. Pass
    "District" only when calling this for AgriculturalResaleProperty, since
    that model has no city field and uses district instead. All other 9
    models use the default "City".

    Returns: (is_valid, error_message, real_state, real_city, real_localities)
    """
    pincode = (pincode or '').strip()

    if not pincode.isdigit() or len(pincode) != 6:
        return False, "Please enter a valid 6-digit pincode.", None, None, []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }

    try:
        resp = requests.get(f'https://api.postalpincode.in/pincode/{pincode}', headers=headers, timeout=5)
        data = resp.json()
    except requests.RequestException:
        return False, "Could not verify pincode right now. Please check your connection and try again.", None, None, []

    if not data or data[0].get('Status') != 'Success':
        return False, f"Pincode {pincode} was not found. Please re-check it.", None, None, []

    post_offices = data[0]['PostOffice']
    real_state = post_offices[0]['State']
    real_city = post_offices[0]['District']
    real_localities = [po['Name'] for po in post_offices]

    if state and state.strip().lower() != real_state.strip().lower():
        return False, f"State does not match pincode {pincode} — it belongs to {real_state}.", real_state, real_city, real_localities

    if city and city.strip().lower() != real_city.strip().lower():
        return False, f"{city_label} does not match pincode {pincode} — it belongs to {real_city}.", real_state, real_city, real_localities

    # Locality is advisory only — manual entries are always allowed since
    # real localities often aren't official India Post post-office names.
    return True, None, real_state, real_city, real_localities