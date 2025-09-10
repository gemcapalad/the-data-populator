import pandas as pd

def replace_invalid(bday):
    df = pd.read_excel("data/new_member_data.xlsx")

    invalid = df["birthday"].astype(str).str.contains(r"\.")
    invalid_indices = df[invalid].index

    for i, idx in enumerate(invalid_indices):
        df.at[idx, "birthday"] = bday[i]

    df.to_excel("data/test.xlsx", index=False)

def main():
    proper_birthdays = [] # i put d bdays here
    
    replace_invalid(proper_birthdays)
    
if __name__ == '__main__':
    main()