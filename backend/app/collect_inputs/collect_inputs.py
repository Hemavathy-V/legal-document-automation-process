import os
import json
from datetime import datetime
from pathlib import Path

# -----------------------------------
# CONFIGURATION
# -----------------------------------

OUTPUT_DIR = Path(__file__).parent / ".." / ".." / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------------
# CONTRACT QUESTION MAPPING
# -----------------------------------

CONTRACT_QUESTIONS = {

    "NDA": {
        "effectiveDate": "Enter Effective Date (e.g., 17th of February 2026): ",
        "disclosingPartyName": "Enter Disclosing Party Name: ",
        "disclosingPartyAddress": "Enter Disclosing Party Address: ",
        "receivingPartyName": "Enter Receiving Party Name: ",
        "receivingPartyAddress": "Enter Receiving Party Address: ",
        "purposeOfDisclosure": "Describe Purpose of Disclosure: ",
        "#exclusions": "List any Exclusions (if none, type 'None'): ",
        "description": "Provide a brief Description of the exclusions: ",
        "/exclusions": "List any Exclusions (if none, type 'None'): ",
        "terminationCondition": "Describe Termination Conditions: ",
        "governingLawJrisdiction": "Enter Governing Law Jurisdiction (Country/State): ",
        "#signatures": "List Parties Required to Sign (if none, type 'None'): ",
        "party": "Enter Party Name: ",
        "title": "Enter Signatory Title: ",
        "date": "Enter Signature Date: ",
        "/signatures": "List Parties Required to Sign (if none, type 'None'): "
    },

    "MSA": {
        "effectiveDate": "Enter Effective Date: ",
        "clientName": "Enter Client Name: ",
        "serviceProviderName": "Enter Service Provider Name: ",
        "governingLaw": "Enter Governing Law (Country/State): "
    },

    "SOW": {
        "effectiveDate": "Enter Effective Date: ",
        "projectName": "Enter Project Name: ",
        "servicesDescription": "Describe the Services: ",
        "paymentTerms": "Enter Payment Terms: "
    },

    "Service Agreement": {
        "effectiveDate": "Enter Effective Date: ",
        "clientName": "Enter Client Name: ",
        "serviceProviderName": "Enter Service Provider Name: ",
        "serviceDescription": "Describe the Service: ",
        "contractDuration": "Enter Contract Duration: "
    },

    "Termination Agreement": {
        "effectiveDate": "Enter Effective Date: ",
        "partyOneName": "Enter First Party Name: ",
        "partyTwoName": "Enter Second Party Name: ",
        "terminationReason": "Enter Reason for Termination: "
    }
}

# -----------------------------------
# SELECT CONTRACT TYPE
# -----------------------------------

def select_contract_type():
    print("\nSelect Contract Type:\n")

    contract_types = list(CONTRACT_QUESTIONS.keys())

    for index, contract in enumerate(contract_types, start=1):
        print(f"{index}. {contract}")

    while True:
        try:
            choice = int(input("\nEnter number: "))
            if 1 <= choice <= len(contract_types):
                return contract_types[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


# -----------------------------------
# COLLECT USER INPUTS
# -----------------------------------

def collect_user_inputs(contract_type):
    print(f"\nYou selected: {contract_type}\n")

    questions = CONTRACT_QUESTIONS[contract_type]
    user_data = {}

    for placeholder, question in questions.items():
        answer = input(question)
        user_data[placeholder] = answer

    return user_data


# -----------------------------------
# SAVE JSON TO OUTPUT FOLDER
# -----------------------------------

def save_to_json(contract_type, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{contract_type.replace(' ', '_')}_{timestamp}.json"
    filepath = OUTPUT_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\nJSON saved successfully at: {filepath}")


# -----------------------------------
# MAIN
# -----------------------------------

def main():
    contract_type = select_contract_type()
    user_inputs = collect_user_inputs(contract_type)
    save_to_json(contract_type, user_inputs)


if __name__ == "__main__":
    main()
