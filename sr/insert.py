import json
import pymysql
import traceback
sql = "INSERT INTO meta_info(info_hash, hash_name, hash_size, create_time, update_time, `delete`) VALUES \
      ('%s', '%s', '%s', now(), now(), '%s')"

sql2 = "INSERT INTO file_list(info_id, path, `length`, create_time, update_time, `delete`) \
                   VALUES ('%s', '%s', '%s', now(), now(), '%s') \
                   "

sql3 = "SELECT * FROM meta_info \
    WHERE info_hash = '%s'"
db = pymysql.connect("localhost", "root", "", "dht")
cursor = db.cursor()
test = '{"hash_id": "CB0196A8A64DD194E2D5871C1EDC3FA71BD35133", "hash_name": "Portable Microsoft Office 2007 SP2 Pro", "hash_size": "540097950", "files": [{"l": 539636234, "p": ["EQNEDT32.EXE"]}, {"l": 125823, "p": ["WINWORD.EXE"]}, {"l": 117337, "p": ["POWERPNT.EXE"]}, {"l": 111283, "p": ["MSACCESS.EXE"]}, {"l": 107273, "p": ["EXCEL.EXE"]}], "a_ip": "212.41.63.90"} '
with open(r"C:\Users\leftking\Desktop\part3-2", "r", encoding="utf-8") as f:
    for line in f:
        try:
            dt = json.loads(line)
            count = cursor.execute(sql3 % dt["hash_id"])
            if count > 0:
                continue
            cursor.execute(sql % (dt["hash_id"], dt["hash_name"], dt["hash_size"], 0))
            last_id = cursor.lastrowid
            if len(dt["files"]) > 0:
                for file in dt["files"]:
                    cursor.execute(sql2 % (last_id, "#>".join(file["p"]), file["l"], 0))
            db.commit()
        except:
            db.rollback()
db.close()