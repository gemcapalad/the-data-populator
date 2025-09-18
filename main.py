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
    invalid_mask = ~df["email"].astype(str).str.contains("@", na=False)

    df.loc[invalid_mask, "email"] = ""

    df.to_excel("data/cleaned_emails.xlsx", index=False)

def email_reader(df):
    invalid_mask = ~df["email"].astype(str).str.contains("@", na=False)

    print(df.loc[invalid_mask, ["first_name", "family_name", "email"]])

def number_cleaner(df):
    df["digits_only"] = df["contact_no"].astype(str).str.replace(r"\D", "", regex=True)

    mask = (df["digits_only"].str.len() > 0) & (df["digits_only"].str.len() != 11)  

    empty_landline_mask = df["landline"].isna()

    final_mask = mask & empty_landline_mask

    df.loc[final_mask, "landline"] = df.loc[final_mask, "contact_no"]
    df.loc[mask, "contact_no"] = ""

    df = df.drop(columns=["digits_only"])

    df.to_excel("data/old_version_4.xlsx", index=False)

def number_checker(df):
    df["digits_only"] = df["contact_no"].astype(str).str.replace(r"\D", "", regex=True)

    mask = (df["digits_only"].str.len() != 11) & (df["digits_only"].str.len() > 0)

    print("digits only")
    invalid_contacts = df.loc[mask, ["family_name", "contact_no", "digits_only"]]
    print(invalid_contacts)

    [print("empty landlines")]
    empty_landline_mask = df["landline"].isna()
    print(df.loc[empty_landline_mask, ["family_name", "landline"]])

    print("final")
    final_mask = mask & empty_landline_mask
    print(df.loc[final_mask, ["family_name", "landline"]])

def number_landline_checker(df):
    mask = (df["contact_no"].isna()) & (df["landline"].isna())
    print(df.loc[mask, ["family_name", "first_name", "contact_no", "landline"]])

def number_dash_remover(df):
    df["contact_no"] = df["contact_no"].str.replace("-", "", regex=False)
    df.to_excel("data/old_version_5.xlsx", index=False)

def landline_checker(df):
    print(df.loc[df["landline"].astype(str).str.match(r"^\(\d{3}\)\d{3}-\d{4}$"), ["family_name", "landline"]])

def main():
    old_df = pd.read_excel("data/old_version_1.xlsx")
    new_df = pd.read_excel("data/new_version_2.xlsx")
    test_df = pd.read_excel("data/old_version_5.xlsx")

    proper_birthdays = [] # i put d bdays here
    
    # replace_invalid_birthday(new_df, proper_birthdays)
    # filter_tin(new_df)
    # no_bday(new_df)
    # tin_checker(test_df)
    # replace_invalid_tin(old_df)
    # email_reader(test_df)
    # number_checker(test_df)
    # number_landline_checker(test_df)
    # number_dash_remover(test_df)
    landline_checker(test_df)

if __name__ == '__main__':
    main()