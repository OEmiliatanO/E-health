#include <string>
#include "API.h"
#include "pinfo.h"

DB_API* new_DB_API()
{
    return new DB_API();
}
patient_info_t load_info(DB_API *api, std::string UID, Status_t& status)
{
    return api->load_info(UID, status);
}
void write_back(DB_API *api, std::string UID, const patient_info_t& new_info, Status_t& status)
{
    api->write_back(UID, new_info, status);
}
void set_DB(DB_API *api, meta_DB_t *DB_p, std::string DB_path, Status_t& status)
{
    api->set_DB(DB_p, DB_path, status);
}
void set_image_db(DB_API *api, meta_DB_t *IDB_p, std::string IDB_path, Status_t& status)
{
    api->set_image_db(IDB_p, IDB_path, status);
}
