#ifndef __API_H__
#define __API_H__
#include <string>
#include <memory>

#include "pinfo.h"
#include "Database.h"

class DB_API
{
private:
    std::string DB_path, IDB_path;
    meta_DB_t *DB_p = nullptr, *IDB_p = nullptr;
public:
    DB_API() = default;

    patient_info_t load_info(std::string UID, Status_t& status)
    {
        status = Status_t::OK;
        if (DB_p->connect() == Status_t::OK)
            return DB_p->require_by_UID(UID);
        status = Status_t::Error;
        return patient_info_t{};
    }

    void write_back(std::string UID, const patient_info_t& new_info, Status_t& status)
    {
        status = Status_t::OK;
        if (DB_p->connect() == Status_t::OK)
            status = DB_p->set_by_UID(UID, new_info);
        else
            status = Status_t::Error;
    }
    void set_DB(meta_DB_t *DB_p, std::string DB_path, Status_t& status)
    {
        if (this->DB_p != nullptr) delete this->DB_p;
        this->DB_path = DB_path;
        this->DB_p = DB_p;
        this->DB_p->set_DB_dir(DB_path);
        status = this->DB_p->connect();
    }
    void set_image_db(meta_DB_t *IDB_p, std::string IDB_path, Status_t& status)
    {
        if (this->DB_p != nullptr) delete this->DB_p;
        this->IDB_path = IDB_path;
        this->IDB_p = IDB_p;
        this->IDB_p->set_DB_dir(IDB_path);
        status = this->IDB_p->connect();
    }
};

class DB_factory
{
public:
    constexpr static std::string_view plain_text_DB = "plain text DB";
    constexpr static std::string_view SQL = "SQL";
    constexpr static std::string_view LiteSQL = "LiteSQL";
    constexpr static std::string_view MySQL = "MySQL";

    static meta_DB_t create(std::string_view which_DB)
    {
        if (which_DB == plain_text_DB)
            return new Plain_text_DB_t();
        return nullptr;
    }
};
#endif
