import time

Time_format = "%m/%d/%Y,%H:%M:%S"

class reports_t:
    def __init__(self, 
                 image_records = [], 
                 numerical_records = {}, 
                 lab_report = "", 
                 diagnosis = "", 
                 prescription = ""):
        self.images_records = image_records
        self.numerical_records = numerical_records;
        self.lab_report = lab_report
        self.diagnosis = diagnosis
        self.prescription = prescription

    def __str__(self):
        numerical_reports = f"{len(self.numerical_records)}\n"
        for k, v in self.numerical_records.items():
            numerical_reports += f"{k} {v}\n"
        lab_report = "[__START__]\n" + self.lab_report.strip() + "\n[__END__]\n"
        diagnosis = "[__START__]\n" + self.diagnosis.strip() + "\n[__END__]\n"
        prescription = "[__START__]\n" + self.prescription.strip() + "\n[__END__]"
        return numerical_reports + lab_report + diagnosis + prescription

class med_record_t:
    def __init__(self, 
                 date = None, 
                 reports = None):
        self.date = date
        self.reports = reports

    def __str__(self):
        return time.strftime(Time_format, self.date) + '\n' + str(self.reports)

class patient_info_t:
    def __init__(self, 
                 UID = None, 
                 name = None, 
                 birth_date = None, 
                 last_update_time = None,
                 med_records = []):
        self.UID = UID
        self.name = name
        self.birth_date = birth_date
        self.last_update_time = last_update_time
        self.med_records = med_records

    def __str__(self):
        return self.UID + '\n' + self.name + '\n' + time.strftime(Time_format, self.birth_date) + '\n' + time.strftime(Time_format, self.last_update_time) + '\n' + f"{len(self.med_records)}" + '\n' + "\n".join([str(med_record) for med_record in self.med_records])
