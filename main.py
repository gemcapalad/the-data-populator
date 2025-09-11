import pandas as pd

def replace_invalid_birthday(df, bday):
    invalid = df["birthday"].astype(str).str.contains(r"\.")
    invalid_indices = df[invalid].index

    for i, idx in enumerate(invalid_indices):
        df.at[idx, "birthday"] = bday[i]

    df.to_excel("data/test.xlsx", index=False)

def filter_tin(df):
    valid = df[df["tin_no"].astype(str).str.len() != 11]

    valid[["family_name", "first_name", "tin_no"]].to_excel("data/invalid-tin.xlsx")


    print(valid[["family_name", "first_name", "tin_no"]])

def no_bday(df):
    print(df[df["birthday"].isna()])

def tin_checker(df):
    invalid_tin = ~df["tin_no"].astype(str).str.match(r"^\d{3}-\d{3}-\d{3}$")

    print(df.loc[invalid_tin, "tin_no"])

def replace_invalid_tin(df):
    df["tin_no"] = df["tin_no"].astype(str)

    df["tin_no"] = df["tin_no"].astype(str).str.replace(r"^(\d{3})(\d{3})(\d{3})$", r"\1-\2-\3", regex=True)

    df.to_excel("data/old_member_test.xlsx", index=False)

def email_checker(df):
    invalid_mask = df["email"].astype(str).str.contains("/") & df["email"].astype(str).str.contains("@")

    print(df.loc[invalid_mask, ["family_name", "first_name", "email"]])

def main():
    old_df = pd.read_excel("data/old_member_data.xlsx")
    new_df = pd.read_excel("data/test.xlsx")
    test_df = pd.read_excel("data/old_member_test.xlsx")

    proper_birthdays = [] # i put d bdays here
    
    # replace_invalid_birthday(new_df, proper_birthdays)
    # filter_tin(new_df)
    # no_bday(new_df)
    # tin_checker(test_df)
    # replace_invalid_tin(old_df)
    email_checker(test_df)

if __name__ == '__main__':
    main()