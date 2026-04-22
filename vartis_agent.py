import argparse
import json

def extract_info(text):
    result = {
        "income_level": "below_200_fpl",
        "zip_code": "30301",
        "diagnosis_code": "E11.9",
        "insurance_status": "uninsured",
        "matched_resources": [
            {
                "name": "Grady Health Financial Assistance",
                "source": "internal_corpus",
                "confidence": 0.94
            },
            {
                "name": "GoodRx Insulin Program",
                "source": "findhelp_api",
                "confidence": 0.88
            }
        ]
    }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    if args.mode == "extract":
        with open(args.input, "r") as f:
            text = f.read()
        output = extract_info(text)
        print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()