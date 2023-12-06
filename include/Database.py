import os
import time
import pinfo

class meta_DB_t:
    def __init__(self):
        self._DB_dir = None

    def set_DB_dir(self, DB_dir: str):
        self.DB_dir = DB_dir

    def connect(self):
        NotImplementedError("")

    def require_by_UID(self, UID: str):
        NotImplementedError("")

    def set_by_UID(self, UID: str, obj):
        NotImplementedError("")

"""
/* format
 * UID
 * name
 * %m/%d/%Y,%T  // birth_date: %m/%d/%Y,%H:%M:%S
 * %m/%d/%Y,%T  // last_update_time: %m/%d/%Y,%H,%M,%S
 * N
 * date
 * M
 * key1 value1
 * key2 value2
 * ...
 * keyM valueM
 * [__START__]
 * Lab reports
 * [__END__]
 * [__START__]
 * Diagnosis
 * [__END__]
 * [__START__]
 * Prescription Note
 * [__END__]
 * date
 * M
 * key1 value1
 * key2 value2
 * ...
 * keyM valueM
 * [__START__]
 * Lab reports
 * [__END__]
 * [__START__]
 * Diagnosis
 * [__END__]
 * [__START__]
 * Prescription Note
 * [__END__]
 *
 * ... repeat N times
 */
"""

class Plain_text_DB_t(meta_DB_t):
    def __init__(self):
        self.postfix = ".info"
        super(Plain_text_DB_t).__init__()

    def skip_newline(self, fs):
        nextl = fs.readline().strip()
        while nextl == "\n":
            nextl = fs.readline().strip()
        return nextl

    def connect(self):
        return os.path.exists(self.DB_dir) and os.path.isdir(self.DB_dir)

    def require_by_UID(self, UID: str):
        patient_info = pinfo.patient_info_t()
        patient_info.med_records = []

        with open(os.path.join(self.DB_dir, UID + self.postfix), 'r') as fs:
            fUID = self.skip_newline(fs)
            fName = self.skip_newline(fs)
            fBirth_date = self.skip_newline(fs)
            fLast_update_time = self.skip_newline(fs)

            patient_info.UID = UID
            patient_info.name = fName
            patient_info.birth_date = time.strptime(fBirth_date, pinfo.Time_format)
            patient_info.last_update_time = time.strptime(fLast_update_time, pinfo.Time_format)
            
            fN = self.skip_newline(fs)
            N = int(fN)
            for _ in range(N):
                tmp_med_record = pinfo.med_record_t()
                tmp_reports = pinfo.reports_t()
                fDate = self.skip_newline(fs)
                tmp_med_record.date = time.strptime(fDate, pinfo.Time_format)
                fM = self.skip_newline(fs)
                if fM.lower() == "none": M = 0
                else: M = int(fM)

                for __ in range(M):
                    k, v = fs.readline().split()
                    tmp_reports.numerical_records[str(k)] = float(v)

                for i in range(3):
                    s = fs.readline().strip()
                    while True:
                        s = fs.readline().strip()
                        if s == "[__END__]":
                            break
                        if i == 0:
                            tmp_reports.lab_report += s.strip() + '\n'
                        elif i == 1:
                            tmp_reports.diagnosis += s.strip() + '\n'
                        else:
                            tmp_reports.prescription += s.strip() + '\n'

                tmp_med_record.reports = tmp_reports
                patient_info.med_records.append(tmp_med_record)
        return patient_info

    def set_by_UID(self, UID: str, info: pinfo.patient_info_t):
        with open(os.path.join(self.DB_dir, UID + self.postfix), 'w') as fs:
            fs.write(str(info))
