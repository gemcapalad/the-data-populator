import pandas as pd
import cleaners

def main():
    old_df = pd.read_excel("data/old/old_version_5.xlsx")
    new_df = pd.read_excel("data/new/new_version_2.xlsx")
    share_capital_df = pd.read_excel("data/misc/share_capital_august.xlsx")
    test_df = pd.read_excel("data/misc/cleaned_emails.xlsx")
    current_df = pd.read_excel("data/update_templates/update_template_version_2.xlsx")
    loans_df = pd.read_excel("data/misc/cleaned_loans.xlsx")

    proper_birthdays = [] # i put d bdays here
    
    # cleaners.replace_invalid_birthday(new_df, proper_birthdays)
    # cleaners.filter_tin(new_df)
    # cleaners.no_bday(new_df)
    # cleaners.tin_checker(test_df)
    # cleaners.replace_invalid_tin(old_df)
    # cleaners.email_reader(test_df)
    # cleaners.number_checker(test_df)
    # cleaners.number_landline_checker(test_df)
    # cleaners.number_dash_remover(test_df)
    # cleaners.landline_checker(test_df)
    # cleaners.tin_matcher(old_df, new_df)
    # cleaners.tin_matcher_enhanced(old_df, new_df)
    # cleaners.name_matcher(old_df, new_df)
    # cleaners.duplicate_checker(current_df, "emails")
    # cleaners.share_capital_duplicate_checker(share_capital_df)
    # cleaners.get_share_capital(current_df, share_capital_df)
    # cleaners.check_active_members(test_df)
    # cleaners.format_numbers(test_df)
    # cleaners.get_members_for_insert(test_df, current_df)
    # cleaners.clean_update_template(test_df, current_df)
    # cleaners.clean_loans(loans_df)
    cleaners.separate_loans(loans_df)

if __name__ == '__main__':
    main()