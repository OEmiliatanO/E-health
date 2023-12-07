import pandas as pd

def process_patient_info(text_info):
    lines = text_info.split('\n')
    patient_data = {}
    
    for line in lines:
        key, value = line.split(' ')
        patient_data[key] = value
    print(patient_data)

    # Creating a DataFrame from the dictionary
    df = pd.DataFrame([patient_data])

    return df

# Example usage:
text_info = """id 0001
name Jager
birthdate 01/01/2000,01:24:00
last_visit 11/30/2023,08:04:09
times 1
age 8
BMI 0.000383673
blood_sugar(mg/dL) 100.0
body_fat_percentage 15.0
estradiol(pg/mL) 10.2
heart_rate(bpm) 65.0
height(m) 1.88
testosterone(ng/mL) 5.5
weight(kg) 70.0"""

# other
# [__START__]
# All numerical reports are in normal range.
# [__END__]
# [__START__]
# A normal person.
# [__END__]
# [__START__]
# Vitamin D tablet(10);calcium tablet(10);
# [__END__]
df = process_patient_info(text_info)
# print(text_info)
# print(text_info.split('\n'))
