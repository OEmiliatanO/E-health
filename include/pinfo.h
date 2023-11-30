#ifndef __PATIENT_INFO_T_H__
#define __PATIENT_INFO_T_H__
#include <ctime>
#include <string>
#include <vector>
#include <map>
#include "image.h"

class reports_t
{
private:
    std::vector<bin_image_t> images_records;
    std::map<std::string, double> numerical_records;
    std::string lab_report, diagnosis, prescription;
public:
    reports_t() = default;
    reports_t(std::vector<bin_image_t> image_records, 
            std::map<std::string, double> numerical_records, 
            std::string lab_report, 
            std::string diagnosis,
            std::string prescription): 
        images_records{image_records}, 
        numerical_records{numerical_records}, 
        lab_report{lab_report}, 
        diagnosis{diagnosis}, 
        prescription{prescription} {}

    reports_t(const reports_t& another)
    {
        this->images_records = another.get_images_records();
        this->numerical_records = another.get_numerical_records();
        this->lab_report = another.get_lab_report();
        this->diagnosis = another.get_diagnosis();
        this->prescription = another.get_prescription();
    }
    reports_t& operator=(const reports_t& another)
    {
        this->images_records = another.get_images_records();
        this->numerical_records = another.get_numerical_records();
        this->lab_report = another.get_lab_report();
        this->diagnosis = another.get_diagnosis();
        this->prescription = another.get_prescription();
        return *this;
    }

    std::vector<bin_image_t> get_images_records() const
    {
        return images_records;
    }
    std::map<std::string, double> get_numerical_records() const
    {
        return numerical_records;
    }
    std::string get_lab_report() const
    {
        return lab_report;
    }
    std::string get_diagnosis() const
    {
        return diagnosis;
    }
    std::string get_prescription() const
    {
        return prescription;
    }

    void append_images(bin_image_t img)
    {
        this->images_records.emplace_back(img);
    }
    void set_numerical_records(std::map<std::string, double> numerical_records)
    {
        this->numerical_records = numerical_records;
    }
    void set_lab_report(std::string lab_report)
    {
        this->lab_report = lab_report;
    }
    void set_diagnosis(std::string diagnosis)
    {
        this->diagnosis = diagnosis;
    }
    void set_prescription(std::string prescription)
    {
        this->prescription = prescription;
    }
};

class med_record_t
{
private:
public:
    std::tm date;
    reports_t reports;
    med_record_t() = default;
    med_record_t(std::tm date, reports_t reports): date{date}, reports{reports} {}
    med_record_t(const med_record_t& another)
    {
        this->date = another.get_date();
        this->reports = another.get_reports();
    }
    med_record_t& operator=(const med_record_t& another)
    {
        this->date = another.get_date();
        this->reports = another.get_reports();

        return *this;
    }
    std::tm get_date() const
    {
        return date;
    }
    reports_t get_reports() const
    {
        return reports;
    }
    void set_date(std::tm date)
    {
        this->date = date;
    }
    void set_reports(reports_t reports)
    {
        this->reports = reports;
    }
};

class patient_info_t
{
private:
    std::string UID, name;
    std::tm birth_date, last_update_time;
    std::vector<med_record_t> med_records;
public:
    patient_info_t() = default;
    patient_info_t(std::string UID): UID{UID} {}
    patient_info_t(std::string UID, std::string name): UID{UID}, name{name} {}
    patient_info_t(std::string UID, 
            std::string name, 
            std::tm birth_date, 
            std::tm last_update_time, 
            std::vector<med_record_t> med_records): 
        UID{UID}, 
        name{name}, 
        birth_date{birth_date},
        last_update_time{last_update_time},
        med_records{med_records} {}
    patient_info_t(const patient_info_t& another)
    {
        this->birth_date = another.get_birth_date();
        this->last_update_time = another.get_last_update_time();
        this->UID = another.UID;
        this->name = another.name;
        this->med_records = another.med_records;
    }
    patient_info_t& operator=(const patient_info_t& another)
    {
        this->birth_date = another.get_birth_date();
        this->last_update_time = another.get_last_update_time();
        this->UID = another.UID;
        this->name = another.name;
        this->med_records = another.med_records;

        return *this;
    }

    std::string get_UID() const
    {
        return UID;
    }
    std::string get_name() const
    {
        return name;
    }
    std::tm get_birth_date() const
    {
        return birth_date;
    }
    std::tm get_last_update_time() const
    {
        return last_update_time;
    }
    std::vector<med_record_t> get_med_records() const
    {
        return med_records;
    }

    void set_UID(std::string UID)
    {
        this->UID = UID;
    }
    void set_name(std::string name)
    {
        this->name = name;
    }
    void set_birth_date(std::tm birth_date)
    {
        this->birth_date = birth_date;
    }
    void set_last_update_time(std::tm last_update_time)
    {
        this->last_update_time = last_update_time;
    }
    void set_med_records(std::vector<med_record_t> med_records)
    {
        this->med_records = med_records;
    }
};
#endif
