#include <iostream>
#include <ctime>
#include <map>
#include <memory>
#include "./include/API.h"
#include "./include/pinfo.h"
#include "./include/pinfo_preprocessor.h"
#include "./include/pinfo_detector.h"
int main()
{
    Status_t status;
    DB_API api;
    /*
    api.set_DB(DB_factory::create(DB_factory::plain_text_DB), "./DB/central_DB/", status);
    patient_info_t Jager{"0001", "Jager"};
    std::istringstream ss{"01/01/2000,01:24:00"};
    std::tm tm;
    ss >> std::get_time(&tm, "%m/%d/%Y,%T");
    Jager.set_birth_date(tm);
    std::time_t time = std::time(0);
    tm = *localtime(&time);
    Jager.set_last_update_time(tm);
    std::vector<med_record_t> med_records;

    reports_t report;
    std::map<std::string, double> numerical_records;
    numerical_records["height(m)"] = 1.88;
    numerical_records["weight(kg)"] = 70.0;
    numerical_records["BMI"] = 70 / (1.88 * 1.88);
    numerical_records["body_fat_percentage"] = 15.0;
    numerical_records["blood_sugar(mg/dL)"] = 100.0;
    numerical_records["heart_rate(bpm)"] = 65.0;
    numerical_records["testosterone(ng/mL)"] = 5.5;
    numerical_records["estradiol(pg/mL)"] = 10.2;
    report.set_numerical_records(numerical_records);

    std::string lab_report = "All numerical reports are in normal range.";
    report.set_lab_report(lab_report);
    std::string diagnosis = "A normal person.";
    report.set_diagnosis(diagnosis);
    std::string prescription = "Vitamin D tablet(10);calcium tablet(10);";
    report.set_prescription(prescription);

    med_records.emplace_back(tm, report);
    Jager.set_med_records(med_records);

    api.write_back(Jager.get_UID(), Jager, status);
    */
    
    api.set_DB(DB_factory::create(DB_factory::plain_text_DB), "./DB/central_DB/", status);
    patient_info_t patient = api.load_info("0001", status);
    std::cout << patient.get_UID() << '\n';
    std::cout << patient.get_name() << '\n';
    std::tm tm = patient.get_birth_date();
    std::cout << std::asctime(&tm) << '\n';
    tm = patient.get_last_update_time();
    std::cout << std::asctime(&tm) << '\n';
    for (auto med_record : patient.get_med_records())
    {
        tm = med_record.get_date();
        std::cout << std::asctime(&tm) << '\n';
        reports_t reports = med_record.get_reports();
        for (auto [k, v] : reports.get_numerical_records())
        {
            std::cout << "[" << k << "] = " << v << '\n';
        }
        std::cout << "lab report:\n" << reports.get_lab_report() << '\n' << '\n';
        std::cout << "diagnosis:\n" << reports.get_diagnosis() << '\n' << '\n';
        std::cout << "prescription:\n" << reports.get_prescription() << '\n' << '\n';
    }


    std::vector<std::unique_ptr<CheckerModule>> checkers;
    checkers.emplace_back(std::make_unique<BMICheckerModule>());
    checkers[0]->check_last(patient);
    checkers.emplace_back(std::make_unique<IsNANCheckerModule>());
    Preprocessor preprocessor(std::move(checkers),patient);
    patient_info_t checked_patient =  preprocessor.preprocess_last();

    for (auto med_record : patient.get_med_records())
    {
        tm = med_record.get_date();
        std::cout << std::asctime(&tm) << '\n';
        reports_t reports = med_record.get_reports();
        for (auto [k, v] : reports.get_numerical_records())
        {
            std::cout << "[" << k << "] = " << v << '\n';
        }
        std::cout << "lab report:\n" << reports.get_lab_report() << '\n' << '\n';
        std::cout << "diagnosis:\n" << reports.get_diagnosis() << '\n' << '\n';
        std::cout << "prescription:\n" << reports.get_prescription() << '\n' << '\n';
    }

    std::vector<std::unique_ptr<DetectorModule>> detectors;
    detectors.emplace_back(std::make_unique<BMIDetectorModule>());
    detectors.emplace_back(std::make_unique<HeartRateDetectorModule>());
    Detector detector(std::move(detectors),checked_patient);
    std::vector<std::string> descs;
    std::vector<Detector_Status_t> statuss;
    detector.detect(descs,statuss);

    for(auto& x:descs){
        std::cout << x << std::endl;
    }
    return 0;
}
