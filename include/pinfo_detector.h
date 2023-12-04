#ifndef __PINFO_DETECTOR_H__
#define __PINFO_DETECTOR_H__
#include <cmath>
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <iostream>
#include "pinfo.h"

enum class Detector_Status_t
{
    OK=0,
    DATA_NOT_FOUND,
    DETECTED,
    NOT_IMPLEMENTED //You have to know something is too complex for programmer
};

class DetectorModule{
public:
    virtual std::string detect(patient_info_t&,Detector_Status_t&) = 0; //Return sickness description or normal if there is no sickness. Return empty string when DATA_NOT_FOUND or NOT_IMPLEMENTED is triggered.
                                                                        //Only detect latest report
};



class BMIDetectorModule: public DetectorModule{
public:
    BMIDetectorModule() = default;
    std::string detect(patient_info_t& patient_info,Detector_Status_t& detector_status) override{
        std::vector<med_record_t> med_records = std::move(patient_info.get_med_records());
        med_record_t med_record = std::move(med_records.back());
        reports_t reports = std::move(med_record.get_reports());
        std::map<std::string,double>  numerical_record = std::move(reports.get_numerical_records());
        std::tm birthdate = patient_info.get_birth_date();
        std::tm checkdate = patient_info.get_last_update_time();
        if(numerical_record.find("BMI") == numerical_record.end()){
            detector_status=Detector_Status_t::DATA_NOT_FOUND;
            return "";
        }
        double bmi = numerical_record["BMI"];
        int age = checkdate.tm_year - birthdate.tm_year;
        // Adjust years based on months and days
        if (checkdate.tm_mon < birthdate.tm_mon ||
            (checkdate.tm_mon == birthdate.tm_mon && checkdate.tm_mday < birthdate.tm_mday)) {
            age--;
        }

        if (age < 18) {
            detector_status=Detector_Status_t::NOT_IMPLEMENTED;
            return "";
        } else if (age >= 18 && age <= 65) {
            if (bmi < 18.5) {
                detector_status=Detector_Status_t::DETECTED;
                return "Underweight";
            } else if (bmi >= 18.5 && bmi < 24) {
                detector_status=Detector_Status_t::OK;
                return "Normal";
            } else if (bmi >= 24 && bmi < 27) {
                detector_status=Detector_Status_t::DETECTED;
                return "Overweight";
            } else {
                detector_status=Detector_Status_t::DETECTED;
                return "Obese";
            }
        } else {
            detector_status=Detector_Status_t::NOT_IMPLEMENTED;
            return "";
        }
        return "";
    }
};

class HeartRateDetectorModule: public DetectorModule{
public:
    HeartRateDetectorModule() = default;
    std::string detect(patient_info_t& patient_info,Detector_Status_t& detector_status) override{
        std::vector<med_record_t> med_records = std::move(patient_info.get_med_records());
        med_record_t med_record = std::move(med_records.back());
        reports_t reports = std::move(med_record.get_reports());
        std::map<std::string,double>  numerical_record = std::move(reports.get_numerical_records());
        if(numerical_record.find("heart_rate(bpm)") == numerical_record.end()){
            detector_status=Detector_Status_t::DATA_NOT_FOUND;
            return "";
        }
        int heart_rate = numerical_record["heart_rate(bpm)"];
        if(heart_rate >= 60 && heart_rate <= 100){
            detector_status = Detector_Status_t::OK;
            return "Normal";
        }
        else if(heart_rate < 60){
            detector_status = Detector_Status_t::DETECTED;
            return "Heart rate is too low.";
        }
        else{
            detector_status = Detector_Status_t::DETECTED;
            return "Heart rate is too high";
        }
        return "";
    }
};

class Detector{
public:
    Detector() = default;
    // Detector(std::vector<std::unique_ptr<DetectorModule>>& detectors_,patient_info_t& patient_info_):
    //     patient_info{patient_info_}
    // {
    //     detectors.reserve(detectors_.size());
    //     for(auto& detector : detectors_){
    //         detectors.emplace_back(std::make_unique<DetectorModule>(*detector));
    //     }
    // }
    Detector(std::vector<std::unique_ptr<DetectorModule>>&& detectors_,patient_info_t& patient_info_):
        detectors{std::move(detectors_)},
        patient_info{patient_info_}
    {}; 
    // Detector& operator=(Detector& another){
    //     patient_info=another.get_patient_info();
    //     detectors=std::move(another.get_detectors());
    //     return *this;
    // }
    //detect
    void detect(std::vector<std::string>& descs,std::vector<Detector_Status_t>& status){
        status.resize(detectors.size());
        descs.resize(detectors.size());
        for(int i=0;i<status.size();++i){
            descs[i] = detectors[i]->detect(patient_info,status[i]);
        }
    }
    //Detectors Editting
    void move_detector(std::unique_ptr<DetectorModule> detector){
        detectors.emplace_back(std::move(detector));
    }
    void remove_detector(){
        detectors.pop_back();
    }
    void detector_clear(){
        detectors.clear();
    }
    //Get and Set
    // std::vector<std::unique_ptr<DetectorModule>>& get_detectors(){
    //     return detectors;
    // }
    patient_info_t get_patient_info(){
        return patient_info;
    }
    void set_patient_info(patient_info_t& patient_info_){
        patient_info = patient_info_;
    }
    void set_detectors(std::vector<std::unique_ptr<DetectorModule>>& detectors_){
        detectors = std::move(detectors_);
    }
    
private:
    std::vector<std::unique_ptr<DetectorModule>> detectors;
    patient_info_t patient_info;
};

#endif
