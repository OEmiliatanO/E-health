import pandas as pd

def process_patient_info(text_info):
    lines = text_info.split('\n')
    patient_data = {}
    current_key = None

    for line in lines:
        if line.startswith("[__START__]"):
            current_key = line[11:-9].strip()
            patient_data[current_key] = []
        elif line.startswith("[__END__]"):
            current_key = None
        elif current_key is not None:
            patient_data[current_key].append(line)

    # Creating a dictionary with patient information
    patient_dict = {
        'ID': lines[0],
        'Name': lines[1],
        'Birthdate': lines[2],
        'LastVisit': lines[3],
    }

    # Adding numerical reports to the dictionary
    numerical_reports = {}
    for line in patient_data.get(''):
        key, value = line.split(' ')
        numerical_reports[key] = float(value)

    patient_dict.update(numerical_reports)

    # Creating a DataFrame from the dictionary
    df = pd.DataFrame([patient_dict])

    return df

# Example usage:
text_info = """0001
Jager
01/01/2000,01:24:00
11/30/2023,08:04:09
1
11/30/2023,08:04:09
8
BMI 0.000383673
blood_sugar(mg/dL) 100.0
body_fat_percentage 15.0
estradiol(pg/mL) 10.2
heart_rate(bpm) 65.0
height(m) 1.88
testosterone(ng/mL) 5.5
weight(kg) 70.0
[__START__]
All numerical reports are in normal range.
[__END__]
[__START__]
A normal person.
[__END__]
[__START__]
Vitamin D tablet(10);calcium tablet(10);
[__END__]"""

df = process_patient_info(text_info)
print(df)
