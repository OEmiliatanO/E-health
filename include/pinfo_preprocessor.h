#ifndef __PINFO_PREPROCESSOR_H__
#define __PINFO_PREPROCESSOR_H__
#include <cmath>
#include <string>
#include <vector>
#include <map>
#include "pinfo.h"

class CheckerModule{
public:
    void check_last(patient_info_t& patient_info){
        size_t med_records_size = patient_info.get_med_records().size();
        check(patient_info, med_records_size-1);

    }
    void check_all(patient_info_t& patient_info){
        size_t med_records_size = patient_info.get_med_records().size();
        for(int i=0;i<med_records_size;++i){
            check(patient_info, i);
        }
    }
    virtual bool check(patient_info_t&,int) = 0;//True: Error been found False: No Error found
};

class BMICheckerModule: public CheckerModule{
public:
    BMICheckerModule() = default;
    bool check(patient_info_t& patient_info,int idx) override{
        std::vector<med_record_t> med_records = std::move(patient_info.get_med_records());
        med_record_t med_record = std::move(med_records[idx]);
        reports_t reports = std::move(med_record.get_reports());
        std::map<std::string,double>  numerical_record = std::move(reports.get_numerical_records());
        if(numerical_record.find("BMI") != numerical_record.end() && std::isnan(numerical_record["BMI"]) && numerical_record["BMI"] > 6 && numerical_record["BMI"] < 300){
            return false;
        }
        double height,weight;
        for(auto& [key,value]:numerical_record){
            if(key.find("height") != std::string::npos) height = value;
            if(key.find("weight") != std::string::npos) weight = value;
        }
        numerical_record["BMI"] = weight / height / height;
        reports.set_numerical_records(numerical_record);
        med_record.set_reports(reports);
        med_records[idx] = med_record;
        patient_info.set_med_records(med_records);
        return true;
    }
};

class IsNANCheckerModule: public CheckerModule{
public:
    IsNANCheckerModule() = default;
    bool check(patient_info_t& patient_info,int idx) override{
        std::vector<med_record_t> med_records = std::move(patient_info.get_med_records());
        med_record_t med_record = std::move(med_records[idx]);
        reports_t reports = std::move(med_record.get_reports());
        std::map<std::string,double>  numerical_record = std::move(reports.get_numerical_records());
        bool isFoundNAN = false;
        for(auto& [key,value]:numerical_record){
            if(std::isnan(value)){
                value = 0.0;
                isFoundNAN = true;
            }
        }
        if(!(isFoundNAN)){
            return false;
        }
        else{
            reports.set_numerical_records(numerical_record);
            med_record.set_reports(reports);
            med_records[idx] = med_record;
            patient_info.set_med_records(med_records);
        }
        return true;
        
    }
};

class Preprocessor{
public:
    Preprocessor() = default;
    Preprocessor(std::vector<CheckerModule>& checkers_,patient_info_t& patient_info_):
        checkers{std::vector<CheckerModule>()},
        patient_info{patient_info_}
    {
        checkers.resize(checkers_.size());
        for(int i=0;i < checkers_.size() ; ++i){
            checkers[i] = checkers_[i];
        }
    }
    Preprocessor(std::vector<CheckerModule>&& checkers_,patient_info_t& patient_info_):
        checkers{checkers_},
        patient_info{patient_info_}
    {};
    Preprocessor& operator=(Preprocessor& another){
        patient_info=another.get_patient_info();
        checkers=another.get_checkers();
        return *this;
    }
    //Preprocess
    patient_info_t preprocess_last(){ 
        for(auto& x:checkers){
            x.check_last(patient_info);
        }
        return patient_info;
    }
    patient_info_t preprocess(int idx){
        for(auto& x:checkers){
            x.check(patient_info,idx);
        }
        return patient_info;

    }
    patient_info_t preprocess_all(){
        for(auto& x:checkers){
            x.check_all(patient_info);
        }
        return patient_info;
    }
    //Checkers Editting
    void append_checker(CheckerModule& checker){
        checkers.emplace_back(checker);
    }
    void remove_checker(){
        checkers.pop_back();
    }
    void preprocessor_clear(){
        checkers.clear();
    }
    //Get and Set
    std::vector<CheckerModule> get_checkers(){
        return checkers;
    }
    patient_info_t get_patient_info(){
        return patient_info;
    }
    void set_patient_info(patient_info_t& patient_info_){
        patient_info = patient_info_;
    }
    void set_checkers(std::vector<CheckerModule>& checkers_){
        checkers = checkers_;
    }
    
private:
    std::vector<CheckerModule> checkers;
    patient_info_t patient_info;
};

#endif
