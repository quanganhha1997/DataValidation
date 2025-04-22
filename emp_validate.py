import pandas as pd

# Load the data
df = pd.read_csv('employees.csv')

# Convert date fields
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
df['salary'] = pd.to_numeric(df['salary'], errors='coerce')

# Existence assertion: for null or empty fields
null_name_records = df['name'].isnull() | (df['name'].astype(str).str.strip() == '')

# Existence assertion: birth_dates cannot be null
null_birthdate_records = df['birth_date'].isnull() | (df['birth_date'].astype(str).str.strip() == '')

# Intra-record assertion: birth_date should be before hire_date
invalid_birth_before_hire = df['birth_date'] >= df['hire_date']

# Intra-record assertion: salary should be > 0
invalid_salary_records = df['salary'].isnull() | (df['salary'] <= 0)

# Limit Assertion: hire_date should be in 2015 or later
invalid_hire_before_2015 = df['hire_date'] < pd.to_datetime('2015-01-01')

# Limit Assertion: birth_date must be later than 1/1/1940
invalid_birth_before_1940 = df['birth_date'] < pd.to_datetime('1940-01-01')
invalid_records = df[invalid_birth_before_1940]
# Inter-Record Assertion: each employee has a manager who is a known employee (every 'reports_to' (manager ID) exists in the 'eid' list)
invalid_manager_records = ~df['reports_to'].isin(df['eid']) & df['reports_to'].notnull()

# Inter-Record Assertion: employees cannot share phone numbers(check for duplicate phone numbers)
duplicate_phones = df['phone'].duplicated(keep=False) & df['phone'].notnull()
#invalid_phones = df[duplicate_phones]

# Summary Assertion: each city has more than one emplyee
city_counts = df['city'].value_counts()


# Count invalid records
null_name_count = null_name_records.sum()
null_birthdate_count = null_birthdate_records.sum()
invalid_birth_hire_count = invalid_birth_before_hire.sum()
invalid_salary_count = invalid_salary_records.sum()
invalid_hire_before_2015_count = invalid_hire_before_2015.sum()
invalid_birth_before_1940_count = invalid_birth_before_1940.sum()
invalid_manager_count = invalid_manager_records.sum()
invalid_phone_dup_count = duplicate_phones.sum()
invalid_cities_with_one_employee = city_counts[city_counts == 1].sum()


# Is the dataset valid overall?
is_valid_summary = invalid_cities_with_one_employee.empty

# Print results
print(f"Number of null fields in column 'name': {null_name_count}")
print(f"Number of null fields in column 'birth_date': {null_birthdate_count}")
print(f"Number of records that violate the birth-before-hire assertion: {invalid_birth_hire_count}")
print(f"Number of records that violate the salary > 0 assertion: {invalid_salary_count}")
print(f"Number of records that violate the hire-after-2015 assertion: {invalid_hire_before_2015_count}")
print(f"Number of records that violate the birth_date after 01/01/1940 assertion: {invalid_birth_before_1940_count}")
#print(invalid_records)
print(f"Number of records that violate the manager must be a known employee assertion: {invalid_manager_count}")
print(f"Number of records that violate the unique phone number assertion: {invalid_phone_dup_count}")
print(f"Number of records that violate the cities has more than only one employee assertion: {invalid_cities_with_one_employee}")
#print(invalid_phones)

