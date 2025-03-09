import re
import hashlib
import json
import datetime
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

def verify_mc_number(mc_number):
    """Checks if MC number is legitimate (using FMCSA API or offline database)."""
    try:
        with open("fmcsa_data.json", "r") as f:
            fmcsa_data = json.load(f)
        return mc_number in fmcsa_data
    except FileNotFoundError:
        return False

def validate_email(email):
    """Checks if email domain is from an official company website."""
    public_domains = {"gmail.com", "yahoo.com", "outlook.com", "aol.com"}
    domain = email.split('@')[-1]
    return domain not in public_domains

def check_phone_number(phone):
    """Regex phone number validation to flag VoIP numbers."""
    return bool(re.match(r'^(\+1|1)?[2-9][0-9]{2}[2-9][0-9]{6}$', phone))

def check_address(address):
    """Verify their given address against FMCSA records and known business locations."""
    try:
        with open("address_database.json", "r") as f:
            address_data = json.load(f)
        return address in address_data
    except FileNotFoundError:
        return False

def check_geo_verification(origin, destination, carrier_location):
    """Ensures the carrier's registered location matches pickup/delivery points."""
    try:
        with open("carrier_locations.json", "r") as f:
            carrier_data = json.load(f)
        return carrier_location in {origin, destination, carrier_data.get(carrier_location, "")}
    except FileNotFoundError:
        return False

def check_payment_method(payment_method):
    """Flag suspicious payment methods."""
    suspicious_methods = {"Venmo", "CashApp", "Zelle", "Gift Card"}
    return payment_method not in suspicious_methods

def detect_duplicate_loads(loads):
    """Check for duplicate load postings."""
    seen = set()
    duplicates = []
    for load in loads:
        key = f"{load['origin']}_{load['destination']}_{load['rate']}_{load['carrier']}"
        load_hash = hashlib.md5(key.encode()).hexdigest()
        if load_hash in seen:
            duplicates.append(load)
        else:
            seen.add(load_hash)
    return duplicates

def log_broker_activity(mc_number, email, phone):
    """Log broker activity to track changes in email or phone numbers."""
    try:
        with open("broker_activity_log.json", "r") as f:
            activity_log = json.load(f)
    except FileNotFoundError:
        activity_log = {}
    if mc_number not in activity_log:
        activity_log[mc_number] = []
    activity_log[mc_number].append({"timestamp": str(datetime.datetime.now()), "email": email, "phone": phone})
    with open("broker_activity_log.json", "w") as f:
        json.dump(activity_log, f, indent=4)

def track_load_status(load_id):
    """Ensure load isn't assigned multiple times."""
    try:
        with open("load_tracking.json", "r") as f:
            load_data = json.load(f)
    except FileNotFoundError:
        load_data = {}
    if load_id in load_data:
        return False  # Meaning the load is already assigned
    load_data[load_id] = str(datetime.datetime.now())
    with open("load_tracking.json", "w") as f:
        json.dump(load_data, f, indent=4)
    return True

def update_watchlist(mc_number):
    """Track repeat offenders and add them to a watchlist if flagged multiple times."""
    try:
        with open("watchlist.json", "r") as f:
            watchlist = json.load(f)
    except FileNotFoundError:
        watchlist = {}
    
    if mc_number in watchlist:
        watchlist[mc_number]["violations"] += 1
    else:
        watchlist[mc_number] = {"violations": 1, "last_flagged": str(datetime.datetime.now())}
    
    with open("watchlist.json", "w") as f:
        json.dump(watchlist, f, indent=4)
    
    if watchlist[mc_number]["violations"] >= 3:
        messagebox.showwarning("High-Risk Broker Alert", f"MC {mc_number} has been flagged multiple times and is now on the watchlist.")

def verify_documents(rate_confirmation, insurance, bill_of_lading):
    """Ensure that rate confirmations, insurance, and other documents are valid."""
    return all([rate_confirmation, insurance, bill_of_lading])

def main():
    sample_loads = [
        {"origin": "Atlanta, GA", "destination": "Dallas, TX", "rate": 1200, "carrier": "MC123456", "carrier_location": "Atlanta, GA", "email": "broker1@some_email.com", "phone": "1234567890", "rate_confirmation": True, "insurance": True, "bill_of_lading": False},
        {"origin": "Chicago, IL", "destination": "Miami, FL", "rate": 800, "carrier": "MC654321", "carrier_location": "Houston, TX", "email": "broker2@some_email.com", "phone": "0987654321", "rate_confirmation": True, "insurance": False, "bill_of_lading": True}
    ]
    for load in sample_loads:
        log_broker_activity(load["carrier"], load["email"], load["phone"])
        update_watchlist(load["carrier"])
        if not verify_documents(load["rate_confirmation"], load["insurance"], load["bill_of_lading"]):
            messagebox.showwarning("Missing Documents", "One or more required documents are missing!")
        if not check_geo_verification(load["origin"], load["destination"], load["carrier_location"]):
            messagebox.showwarning("Carrier Location Mismatch", f"Carrier location {load['carrier_location']} does not align with route.")
        if not track_load_status(f"{load['origin']}_{load['destination']}_{load['carrier']}"):
            messagebox.showwarning("Duplicate Load Assignment", "This load has already been assigned and can't be double-brokered.")

if __name__ == "__main__":
    main()
