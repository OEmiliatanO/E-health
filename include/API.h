#ifndef __API_H__
#define __API_H__
#include <string>
#include <sys/types.h>
#include <sys/stat.h>
#include <filesystem>
#include <vector>
#include <ctime>
#include <iomanip>
#include <memory>
#include <fstream>
#include "pinfo.h"

enum class Status_t
{
    OK=0,
    Not_Exists,
    Error
};

class meta_DB_t
{
protected:
    std::string DB_dir;
public:
    meta_DB_t() = default;
    virtual ~meta_DB_t() = default;
    virtual void set_DB_dir(std::string DB_dir) { this-> DB_dir = DB_dir; }
    virtual Status_t connect() = 0;
    virtual patient_info_t require_by_UID(std::string UID) = 0;
    virtual Status_t set_by_UID(std::string UID, const patient_info_t& obj) = 0;
};

class DB_API
{
public:
    static std::string DB_path, Image_DB_path;
    static meta_DB_t *DB, *IDB;
    static patient_info_t load_info(std::string UID, Status_t& status)
    {
        status = Status_t::OK;
        if (DB->connect() == Status_t::OK)
            return DB->require_by_UID(UID);
        status = Status_t::Error;
        return patient_info_t{};
    }

    static void write_back(std::string UID, const patient_info_t& new_info, Status_t& status)
    {
        status = Status_t::OK;
        if (DB->connect() == Status_t::OK)
            status = DB->set_by_UID(UID, new_info);
        else
            status = Status_t::Error;
    }
    static void set_DB(meta_DB_t *DB_, std::string DB_p, Status_t& status)
    {
        if (DB != nullptr) delete DB;
        DB_path = DB_p;
        DB = DB_;
        DB->set_DB_dir(DB_p);
        status = DB->connect();
    }
    static void set_Image_DB(meta_DB_t *IDB_, std::string IDB_p, Status_t& status)
    {
        if (IDB != nullptr) delete IDB;
        Image_DB_path = IDB_p;
        IDB = std::move(IDB_);
        IDB->set_DB_dir(IDB_p);
        status = IDB->connect();
    }
};


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
class Plain_text_DB_t : public meta_DB_t
{
private:
public:
    Plain_text_DB_t() = default;
    ~Plain_text_DB_t() = default;
    Status_t connect() override
    {
        // DB_p is a dir
        if (std::filesystem::exists(this->DB_dir) and std::filesystem::is_directory(this->DB_dir))
            return Status_t::OK;
        return Status_t::Not_Exists;
    }

    patient_info_t require_by_UID(std::string UID) override
    {
        std::fstream fs(std::filesystem::path{this->DB_dir} / (UID + ".info"), std::ios_base::in);
        std::getline(fs, UID);
        std::string name;
        std::getline(fs, name);
        patient_info_t info{UID, name};
        std::vector<med_record_t> med_records;
        std::tm tm;
        fs >> std::get_time(&tm, "%m/%d/%Y,%T");
        info.set_birth_date(tm);
        fs >> std::get_time(&tm, "%m/%d/%Y,%T");
        info.set_last_update_time(tm);

        int N;
        fs >> N;
        for (int _ = 0; _ < N; ++_)
        {
            med_record_t med_record;
            reports_t reports;
            std::map<std::string, double> numerical_report;
            fs >> std::get_time(&tm, "%m/%d/%Y,%T");
            med_record.set_date(tm);
            int M;
            fs >> M;
            for (int __ = 0; __ < M; ++__)
            {
                std::string key;
                double value;
                fs >> key >> value;
                numerical_report[key] = value;
            }
            std::string s;
            for (int i = 0; i < 3; ++i)
            {
                std::string res;
                do
                {
                    std::getline(fs, s);
                }while (s != "[__START__]");
                while (true)
                {
                    std::getline(fs, s);
                    if (s == "[__END__]") break;
                    res += s + '\n';
                }
                if (i == 0)
                    reports.set_lab_report(res);
                else if (i == 1)
                    reports.set_diagnosis(res);
                else
                    reports.set_prescription(res);
            }
            reports.set_numerical_records(numerical_report);
            med_record.set_reports(reports);
            med_records.emplace_back(med_record);
        }
        info.set_med_records(med_records);
        return info;
    }

    Status_t set_by_UID(std::string UID, const patient_info_t& obj) override
    {
        std::fstream fs(std::filesystem::path{this->DB_dir} / (UID + ".info"), std::ios_base::out);
        fs << UID << '\n';
        fs << std::move(obj.get_name()) << '\n';
        std::tm tm = obj.get_birth_date();
        char time[80]{};
        strftime(time, 80, "%m/%d/%Y,%T", &tm);
        fs << time << '\n';
        tm = std::move(obj.get_last_update_time());
        strftime(time, 80, "%m/%d/%Y,%T", &tm);
        fs << time << '\n';
        std::vector<med_record_t> med_records = std::move(obj.get_med_records());
        int N = med_records.size();
        fs << N << '\n';
        for (int i = 0; i < N; ++i)
        {
            tm = med_records[i].get_date();
            strftime(time, 80, "%m/%d/%Y,%T", &tm);
            fs << time << '\n';
            reports_t reports = med_records[i].get_reports();
            std::map<std::string, double> numerical_report = reports.get_numerical_records();
            fs << numerical_report.size() << '\n';
            for (auto [k, v] : numerical_report)
                fs << k << ' ' << v << '\n';
            for (int j = 0; j < 3; ++j)
            {
                std::string res;
                if (j == 0)
                    res = reports.get_lab_report();
                else if (j == 1)
                    res = reports.get_diagnosis();
                else
                    res = reports.get_prescription();
                if (res.back() != '\n') res.push_back('\n');
                fs << "[__START__]\n" << res << "[__END__]\n";
            }
        }
        return Status_t::OK;
    }
};

class DB_factory
{
public:
    constexpr static std::string_view plain_text_DB = "plain text DB";
    constexpr static std::string_view SQL = "SQL";
    constexpr static std::string_view LiteSQL = "LiteSQL";
    constexpr static std::string_view MySQL = "MySQL";

    static meta_DB_t* create(std::string_view which_DB)
    {
        if (which_DB == plain_text_DB)
            return new Plain_text_DB_t();
        return nullptr;
    }
};
#endif
