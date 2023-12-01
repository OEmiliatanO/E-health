#include <map>
#include <vector>
#include "pinfo.h"

using df = double;
using str = std::string;
using m_str_df = std::map<str, df>;
using v_df = std::vector<df>;
using v_str = std::vector<str>;

/* vector<string> */
v_str* new_v_str()
{
    return new v_str();
}
void v_str_append(v_str* v, const char *s)
{
    v->emplace_back(s);
}
void v_str_assign(v_str* v, int i, const char *s)
{
    v->at(i) = s;
}
const char* v_str_get(v_str* v, int i)
{
    return v->at(i).c_str();
}
int v_str_size(v_str* v, const char *s)
{
    return v->size();
}

/* vector<double> */
v_df* new_v_df()
{
    return new v_df();
}
void v_df_append(v_df* v, df x)
{
    v->emplace_back(x);
}
void v_df_assign(v_str* v, int i, df x)
{
    v->at(i) = x;
}
int v_df_size(v_df* v)
{
    return v->size();
}
df v_df_get(v_df* v, int i)
{
    return v->at(i);
}

/* map<string, double> */
m_str_df* new_map_str_df()
{
    return new m_str_df();
}
void m_str_df_set(m_str_df* m, const char* s, df v)
{
    m->at(s) = v;
}
df m_str_df_get(m_str_df* m, const char* s)
{
    return m->at(s);
}
v_str* get_map_str_df_keys(m_str_df* m)
{
    v_str* keys = new v_str();
    for (auto [k, v] : m)
        keys->emplace_back(k);
    return keys;
}
v_df* get_map_str_df_values(m_str_df* m)
{
    v_df* values = new v_df();
    for (auto [k, v] : m)
        values->emplace_back(v);
    return values;
}
m_str_df* get_map_str_df_from_v(const v_str* keys, const v_df* values)
{
    m_str_df* m = new m_str_df();
    for (int i = 0; i < std::min(keys->size(), values->size()); ++i)
        m->at(keys->at(i)) = values;
    return m;
}

/* string */
const char* get_str(str* s)
{
    return s->c_str();
}
char str_get_i(str* s, int i)
{
    return s->at(i);
}

/* reports_t */
reports_t* new_reports_t()
{
    return new reports_t();
}
const char* get_lab_report(reports_t* reports)
{
    return reports->get_lab_report().c_str();
}
const char* get_diagnosis(reports_t* reports)
{
    return reports->get_diagnosis().c_str();
}
const char* get_prescription(reports_t* reports)
{
    return reports->get_prescription().c_str();
}
void set_numerical_records(reports_t *reports, const m_str_df *numerical_records)
{
    reports->numerical_records = *numerical_records;
}
void set_lab_report(reports_t *reports, const char *lab_report)
{
    reports->lab_report = lab_report;
}
void set_diagnosis(reports_t *reports, const char *diagnosis)
{
    reports->diagnosis = diagnosis;
}
void set_prescription(reports_t *reports, const char *prescription)
{
    reports->prescription = prescription;
}

/* tm */
std::tm* new_tm()
{
    return new std::tm();
}
void tm_set_sec(std::tm* tm, int sec)
{
    tm->tm_sec = sec;
}
void tm_set_min(std::tm* tm, int min)
{
    tm->tm_min = min;
}
void tm_set_hour(std::tm* tm, int hour)
{
    tm->tm_hour = hour;
}
void tm_set_mday(std::tm* tm, int mday)
{
    tm->tm_mday = mday;
}
void tm_set_mon(std::tm* tm, int mon)
{
    tm->tm_mon = mon;
}
void tm_set_year(std::tm* tm, int year)
{
    tm->tm_year = year;
}
void tm_set_wday(std::tm* tm, int wday)
{
    tm->tm_wday = wday;
}
void tm_set_yday(std::tm* tm, int yday)
{
    tm->tm_yday = yday;
}
void tm_set_isdst(std::tm* tm, int isdst)
{
    tm->tm_isdst = isdst;
}
void mktime(std::tm* tm)
{
    std::mktime(tm);
}
int tm_get_sec(std::tm* tm)
{
    return tm->tm_sec;
}
int tm_get_min(std::tm* tm)
{
    return tm->tm_min;
}
int tm_get_hour(std::tm* tm)
{
    return tm->tm_hour;
}
int tm_get_mday(std::tm* tm)
{
    return tm->tm_mday;
}
int tm_get_mon(std::tm* tm)
{
    return tm->tm_mon;
}
int tm_get_year(std::tm* tm)
{
    return tm->tm_year;
}
int tm_get_wday(std::tm* tm)
{
    return tm->tm_wday;
}
int tm_get_yday(std::tm* tm)
{
    return tm->tm_yday;
}
int tm_get_isdst(std::tm* tm)
{
    return tm->tm_isdst;
}


/* med_record_t */
med_record_t* new_med_record()
{
    return new med_record_t();
}
reports_t* get_reports(med_record_t* med_record)
{
    reports_t *r = new reports_t();
    *r = med_record->get_reports();
    return r;
}
void set_reports(med_records_t* med_record, const reports_t* reports)
{
    med_record->reports = *reports;
}
std::tm* get_date(med_records_t* med_record)
{
    std::tm* tm = new std::tm();
    *tm = med_record->get_date();
    return tm;
}
void set_date(med_records_t* med_record, std::tm* tm)
{
    med_record->set_date(*tm);
}

/* vector<med_record_t> */
std::vector<med_record_t>* new_vector_med_record_t()
{
    return new std::vector<med_record_t>();
}
med_record_t* vector_med_record_t_get(std::vector<med_record_t>* v, int i)
{
    med_record_t *m = new med_record_t();
    *m = v->at(i);
    return m;
}
void vector_med_record_t_append(std::vector<med_record_t>* v, med_record_t* m)
{
    v->emplace_back(*m);
}
void vector_med_record_t_assign(std::vector<med_record_t>* v, int i, med_record_t* m)
{
    v->at(i) = *m;
}
int vector_med_record_t_size(std::vector<med_record_t>* v)
{
    return v->size();
}

/* patient_info_t */
patient_info_t* new_patient_info_t()
{
    return new patient_info_t();
}
const char* get_UID(patient_info_t* patient_info)
{
    return patient_info->get_UID()->c_str();
}
const char* get_name(patient_info_t* patient_info)
{
    return patient_info->get_name()->c_str();
}
std::tm* get_birth_date(patient_info_t* patient_info)
{
    std::tm* tm = new std::tm();
    *tm = patient_info->get_birth_date();
    return tm;
}
std::tm* get_last_update_time(patient_info_t* patient_info)
{
    std::tm* tm = new std::tm();
    *tm = patient_info->get_last_update_time();
    return tm;
}
std::vector<med_records_t>* get_med_records(patient_info_t* patient_info)
{
    std::vector<med_records_t>* v = new std::vector<med_records_t>();
    *v = patient_info->get_med_records();
    return v;
}
void set_UID(patient_info_t* patient_info, const char* UID)
{
    std::string s = UID;
    patient_info->set_UID(s);
}
void set_name(patient_info_t* patient_info, const char* name)
{
    std::string s = name;
    patient_info->set_name(s);
}
void set_birth_date(patient_info_t* patient_info, const std::tm* tm)
{
    patient_info->set_birth_date(*tm);
}
void set_last_update_time(patient_info_t* patient_info, const std::tm* tm)
{
    patient_info->set_last_update_time(*tm);
}
void set_med_records(patient_info_t* patient_info, const vector<med_record_t>* v)
{
    patient_info->set_med_records(*v);
}
