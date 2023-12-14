#include <iostream>
#include <fstream>
#include <ctime>
#include <map>
#include <memory>
#include <vector>
#include <string>
#include "./include/API.h"
#include "./include/pinfo.h"
#include "./include/pinfo_preprocessor.h"
#include "./include/pinfo_detector.h"
int main(int argc, char *argv[])
{
    Status_t status;
    DB_API api;

    std::string current_exec_name = argv[0]; // Name of the current exec program
    std::vector<std::string> all_args;

    if (argc > 1) {
        all_args.assign(argv + 1, argv + argc);
    }
    std::string patient_UID = all_args[1];
    std::string path = all_args[0]+"/"+patient_UID+".info";
    
    api.set_DB(DB_factory::create(DB_factory::plain_text_DB), "./DB/central_DB/", status);
    patient_info_t patient = api.load_info(patient_UID, status);
    // std::cout << patient.get_UID() << '\n';
    // std::cout << patient.get_name() << '\n';
    std::tm tm = patient.get_birth_date();
    // std::cout << std::asctime(&tm) << '\n';
    tm = patient.get_last_update_time();
    // std::cout << std::asctime(&tm) << '\n';

    std::vector<std::unique_ptr<CheckerModule>> checkers;
    checkers.emplace_back(std::make_unique<BMICheckerModule>());
    checkers[0]->check_last(patient);
    checkers.emplace_back(std::make_unique<IsNANCheckerModule>());
    Preprocessor preprocessor(std::move(checkers),patient);
    patient_info_t checked_patient =  preprocessor.preprocess_last();

    std::ofstream fout(path);
    for (auto med_record : patient.get_med_records())
    {
        tm = med_record.get_date();
        // std::cout << std::asctime(&tm) << '\n';
        reports_t reports = med_record.get_reports();
        // for (auto [k, v] : reports.get_numerical_records())
        // {
        //     std::cout << "[" << k << "] = " << v << '\n';
        // }
        fout << "lab report:\n" << reports.get_lab_report();
        fout << "diagnosis:\n" << reports.get_diagnosis();
        fout << "prescription:\n" << reports.get_prescription();
    }
    fout.close();

    std::vector<std::unique_ptr<DetectorModule>> detectors;
    detectors.emplace_back(std::make_unique<BMIDetectorModule>());
    detectors.emplace_back(std::make_unique<HeartRateDetectorModule>());
    Detector detector(std::move(detectors),checked_patient);
    std::vector<std::string> descs;
    std::vector<Detector_Status_t> statuss;
    // detector.detect(descs,statuss);

    // for(auto& x:descs){
    //     std::cout << x << std::endl;
    // }
    return 0;
}
