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

def tin_matcher(old_df, new_df):
    old_df["tin_in_new_excel"] = old_df["tin_no"].isin(new_df["tin_no"])
    all = old_df["tin_no"].count()
    matches = old_df["tin_in_new_excel"].sum()

    print(f'TIN matches: {matches} All TIN: {all}')

    print(old_df.loc[~old_df["tin_no"].isin(new_df["tin_no"]), ["first_name", "family_name", "tin_no"]])

def tin_matcher_enhanced(old_df, new_df):
    # old_df_no_match = old_df.loc[~old_df["tin_no"].isin(new_df["tin_no"]), ["tin_no"]].rename(columns={"tin_no": "tin_in_old"})
    # new_df_no_match = new_df.loc[~new_df["tin_no"].isin(old_df["tin_no"]), ["tin_no"]].rename(columns={"tin_no": "tin_in_new"})

    # no_matches = pd.concat([old_df_no_match.reset_index(drop=True), new_df_no_match.reset_index(drop=True)], axis=1)

    # no_matches.to_excel("data/no_matches.xlsx")

    new_df["tin_in_old_excel"] = new_df["tin_no"].isin(old_df["tin_no"])
    all = new_df["tin_no"].count()
    matches = new_df["tin_in_old_excel"].sum()

    print(f'TIN matches: {matches} | All TIN: {all} | Total Missing: {all - matches}')

    valid = new_df.loc[~new_df["tin_no"].isin(old_df["tin_no"]), ["first_name", "family_name", "tin_no"]]

    valid[["family_name", "first_name", "tin_no"]].to_excel("data/matches.xlsx", index=False)

def name_matcher(old_df, new_df):
    merged_df = pd.merge(
        new_df,
        old_df,
        on="tin_no",
        how="left",
        suffixes=("", "_old") 
    )

    merged_df.to_excel("data/merged_version_1.xlsx", index=False)
    
    print("Merge success!")

def duplicate_checker(df, d):
    if d == 'tins': 
        duplicate_tins = df[df.duplicated(subset="tin_no", keep=False)]
        print("Duplicate TINs")
        print(duplicate_tins)
    elif d == 'ids':
        duplicate_ids = df[df.duplicated(subset="id", keep=False)]
        print("Duplicate IDs")
        print(duplicate_ids)
    elif d == 'names':
        duplicate_names = df[df.duplicated(subset=["family_name", "first_name"], keep=False)]
        print("Duplicate names")
        print(duplicate_names)
    elif d == 'emails':
        duplicate_emails = df[df.duplicated(subset="email", keep=False) & ~df["email"].isna()]
        print("Duplicate emails")
        print(duplicate_emails)
    
def share_capital_duplicate_checker(df):
    duplicate_names = df[df.duplicated(subset="name", keep=False)]

    print(duplicate_names)

def get_share_capital(merged_df, share_capital_df):
    merged_df["full_name"] = merged_df["family_name"].str.strip() + ", " + merged_df["first_name"].str.strip()
    # merged_df["full_name_initialed"] = merged_df["family_name"].str.strip() + ", " + merged_df["first_name"].str.strip() + " " + merged_df["middle_name"].str[0] + "."
    # merged_df["middle_initial"] = merged_df["middle_name"].str[0] + "."

    share_capital_df[["family_name", "first_middle"]] = share_capital_df["name"].str.split(",", n=1, expand=True)
    share_capital_df["family_name"] = share_capital_df["family_name"].str.strip()
    share_capital_df["first_middle"] = share_capital_df["first_middle"].str.strip()
    share_capital_df["first_name"] = share_capital_df["first_middle"].str.split(" ").str[:-1].str.join(" ")
    # share_capital_df["middle_initial"] = share_capital_df["first_middle"].str.split(" ").str[-1] + "."
    share_capital_df["formatted_name"] = share_capital_df["family_name"] + ", " + share_capital_df["first_name"]

    share_capital_df["match"] = share_capital_df["formatted_name"].isin(merged_df["full_name"])
    # all = share_capital_df["formatted_name"].count()
    # matches = share_capital_df["match"].sum()

    # print(f'Full name matches: {matches} | All share capital names in merged: {all} | Total missing: {all - matches}')

    # no_match = share_capital_df.loc[~share_capital_df["formatted_name"].isin(merged_df["full_name"])]

    # probably_wed = no_match.loc[~share_capital_df["middle_initial"].str.strip().isin(merged_df["middle_initial"])]

    # print("All no matches")
    # print(no_match)
    # print("Probably wed no matches")
    # print(probably_wed)
    # no_match["name"].to_excel("data/current_members_not_in_database.xlsx")

    final_df = pd.merge(
        merged_df,
        share_capital_df["August"],
        left_on="full_name",
        right_on=share_capital_df["formatted_name"],
        how="left" 
    )

    final_df["match"] = final_df["amount"] == final_df["August"]
    mismatches = final_df[final_df["match"] == False]
    print(mismatches)

    # final_df.to_excel("data/merged_version_2.xlsx", index=False)
    
    print("Merge success!")

def check_active_members(df):
    df.loc[~df["August"].isna()].to_excel("data/merged_version_3.xlsx", index=False)

def format_numbers(df):
    df["id"] = df["id"].astype(str).str.replace("1984-", "")
    df["gender"] = df["gender"].str.strip().replace("F", "Female").replace("M", "Male")
    df["email"] = df["email"].str.lower()

    df.to_excel("data/merged_version_4.xlsx", index=False)

def get_members_for_insert(final_df, current_df):
    invalid_mask = final_df["email"].astype(str).str.contains("@", na=False)

    valid = final_df.loc[invalid_mask]

    valid.to_excel("data/cleaned_emails.xlsx", index=False)
    
def clean_update_template(final_df, current_df):
    valid = final_df.loc[~final_df["id"].isin(current_df["id"])]

    valid.to_excel("data/update_template_version_2.xlsx")

def main():
    old_df = pd.read_excel("data/old_version_5.xlsx")
    new_df = pd.read_excel("data/new_version_2.xlsx")
    share_capital_df = pd.read_excel("data/share_capital_august.xlsx")
    test_df = pd.read_excel("data/cleaned_emails.xlsx")
    current_df = pd.read_excel("data/update_template_version_2.xlsx")

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
    # landline_checker(test_df)
    # tin_matcher(old_df, new_df)
    # tin_matcher_enhanced(old_df, new_df)
    # name_matcher(old_df, new_df)
    # duplicate_checker(current_df, "emails")
    # share_capital_duplicate_checker(share_capital_df)
    get_share_capital(current_df, share_capital_df)
    # check_active_members(test_df)
    # format_numbers(test_df)
    # get_members_for_insert(test_df, current_df)
    # clean_update_template(test_df, current_df)

if __name__ == '__main__':
    main()