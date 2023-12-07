import sys
path = "/Users/liushiwen/Desktop/大四上/物件導向程式設計/E-health"
sys.path.append(f'{path}/include')
from API import DB_API
from API import DB_factory

def main():
    api = DB_API()
    api.set_DB(DB_factory.create(DB_factory.plain_text_DB), f"{path}/DB/central_DB")
    info = api.load_info("0001")
    print(str(info))

if __name__ == "__main__":
    main()
    