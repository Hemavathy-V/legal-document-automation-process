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
        "exclusions": [
            {"description": "Describe Exclusion 1: "}
        ],
        "terminationCondition": "Describe Termination Conditions: ",
        "governingLawJrisdiction": "Enter Governing Law Jurisdiction (Country/State): ",
        "signatures": [
            {"party": "Enter Party Name: ",
            "title": "Enter Signatory Title: ",
            "date": "Enter Signature Date: ",
            }
        ]
    },

    "MSA": {
        "effectiveDate": "Enter Effective Date: ",
        "clientName": "Enter Client Name: ",
        "serviceProviderName": "Enter Service Provider Name: ",
        "governingLaw": "Enter Governing Law (Country/State): "
    },

    "SOW": {
        "Project_Title": "Enter Project Title: ",
        "Client_Company_Name": "Enter Client Company Name: ",
        "Service_Provider_Name": "Enter Service Provider Name: ",
        "Effective_Date": "Enter Effective Date: ",
        "SOW_Reference_Number": "Enter SOW Reference Number: ",
        "Project_Name": "Enter Project Name: ",
        "Primary_Objective": "Describe Primary Objective: ",
        "Secondary_Objectives": "Describe Secondary Objectives (if none, type 'None'): ",
        "Business_Goal": "Describe Business Goal: ",
        "In_Scope_Activities": [
            {"activity": "Conduct requirements gathering"}
        ],
        "Technical_Implementation_Details": [
            {"detail": "Describe technical implementation detail 1: "}
        ],
        "Documentation_and_Reporting_Details": [
            {"doc": "Describe documentation/reporting detail 1: "}
        ],
        "Out_of_Scope_Items": [
            {"item": "Describe out-of-scope item 1: "}
        ],
        "deliverable.name": "Enter Deliverable Name: ",
        "deliverable.description": "Describe Deliverable Description: ",
        "deliverable.format": "Enter Deliverable Format (e.g., PDF, DOCX, etc.): ",
        "deliverable.due_date": "Enter Deliverable Due Date: ",
        "milestone.name": "Enter Milestone Name: ",
        "milestone.description": "Describe Milestone Description: ",
        "milestone.date": "Enter Milestone Date: ",
        "Start_Date": "Enter Project Start Date: ",
        "End_Date": "Enter Project End Date: ",
        "SP_Responsibilities": [
            {"responsibility": "Describe Service Provider Responsibility 1: "}
        ],
        "SP_Project_Manager_Name": "Enter Service Provider Project Manager Name: ",
        "SP_QA_Process_Description": "Describe Service Provider QA Process: ",
        "Client_Provided_Resources": "Describe Client-Provided Resources (if none, type 'None'): ",
        "Approval_Timeframe": "Enter Approval Timeframe (e.g., 5 business days): ",
        "Client_POC_Name": "Enter Client POC Name: ",
        "Assumptions": [
            {"assumption": "Describe Assumption 1: "}
        ],
        "Total_Project_Cost": "Enter Total Project Cost: ",
        "Currency": "Enter Currency (e.g., USD, EUR, etc.): ",
        "Payment_Method": "Enter Payment Method : ",
        "Payment_Terms": "Describe Payment Terms : ",
        "Change_Request_Form_ID": "Enter Change Request Form ID (if applicable, else type 'None'): ",
        "MSA_Date": "Enter MSA Date (if applicable, else type 'None'): ",
        "Requirements_Document_Name": "Enter Requirements Document Name (if applicable, else type 'None'): ",
        "Acceptance_Period_Days": "Enter Acceptance Period in Days (e.g., 30): ",
        "Termination_Notice_Period": "Enter Termination Notice Period (e.g., 30 days): ",
        "Termination_Effective_Date": "Enter Termination Effective Date (if applicable, else type 'None'): ",
        "Delivery_Format_On_Termination": "Describe Delivery Format Upon Termination: ",
        "Client_Signatory_Name": "Enter Client Signatory Name: ",
        "Client_Signatory_Title": "Enter Client Signatory Title: ",
        "Client_Signature_Date": "Enter Client Signature Date: ",
        "SP_Signatory_Name": "Enter Service Provider Signatory Name: ", 
        "SP_Signatory_Title": "Enter Service Provider Signatory Title: ",
        "SP_Signature_Date": "Enter Service Provider Signature Date: "
    },

    "Service Agreement": {
        "providerName": "Enter Service Provider Name: ",
        "clientName": "Enter Client Name: ",
        "effectiveDate": "Enter Effective Date: ",
        "terminationDate": "Enter Termination Date: ",
        "serviceTitle": "Enter Service Title: ",
        "serviceDescription": "Describe Service Description: ",
        "rate": "Enter Service Rate (e.g., $100/hour): ",
        "rateUnit": "Enter Rate Unit (e.g., hour, project, etc.): ",
        "payementDue": "Enter Payment Due Date (e.g., within 30 days of invoice): ",
        "payementMethod": "Enter Payment Method (e.g., bank transfer, check, etc.): ",
        "providerResponsibilities": [
            {"responsibility": "Describe Provider Responsibility 1: "}
        ],
        "clientResponsibilities": [
            {"responsibility": "Describe Client Responsibility 1: "}
        ],
        "terminationNoticePeriod": "Enter Termination Notice Period (e.g., 30 days): ",
        "disputeResolutionMethod": "Enter Dispute Resolution Method (e.g., mediation, arbitration, etc.): ",
        "additionalClauses": [
            {"clause": "Describe Additional Clause 1: "}
        ],
        "signatures": [
            {"party": "Enter Party Name: ",
             "fullName": "Enter Signatory Full Name: ",
             "title": "Enter Signatory Title: ",
             "signature": "Enter Signature Date: ",
             "date": "Enter Signature Date: "
            }
        ]
    },

    "Termination Agreement": {
        "PartyA_Name": "Enter Party A Name: ",
        "PartyB_Name": "Enter Party B Name: ",
        "PartyA_Address": "Enter Party A Address: ",
        "PartyB_Address": "Enter Party B Address: ",
        "PartyA_Rep_Name": "Enter Party A Representative Name: ",
        "PartyB_Rep_Name": "Enter Party B Representative Name: ",
        "PartyA_Rep_Title": "Enter Party A Representative Title: ",
        "PartyB_Rep_Title": "Enter Party B Representative Title: ",
        "Original_Agreement_Type": "Enter Original Agreement Type (e.g., MSA, SOW, etc.): ",
        "Original_Agreement_Date": "Enter Original Agreement Date: ",
        "Termination_Effective_Date": "Enter Termination Effective Date: ",
        "Outstanding_Amount": "Enter Outstanding Amount (if any, else type 'None'): ",
        "Payment_Due_Date": "Enter Payment Due Date for Outstanding Amount (if any, else type 'None'): ",
        "Return_Period_Days": "Enter Return Period in Days for any materials or equipment (if any, else type 'None'): ",
        "Confidentiality_Survival_Period": "Enter Confidentiality Survival Period in Months (if any, else type 'None'): ",
        "Governing_Law_Jurisdiction": "Enter Governing Law Jurisdiction (Country/State): ",
        "Dispute_Location": "Enter Dispute Location (City, Country): ",
        "PartyA_Sign_Date": "Enter Party A Signature Date: ",
        "PartyB_Sign_Date": "Enter Party B Signature Date: "
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
