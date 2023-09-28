"""

"""
import config as conf
from MyHomeMyCastle import DataBaseAlchemy as DBAl

if __name__ == "__main__":
    print("--- SQLite ---")
    db_path = conf.DATABASE_NAME
    session = DBAl.createSession(db_path=db_path, style="SQLite")

    print("--- {:^15} ---".format("users"))
    usr_results = session.query(DBAl.User).all()
    usr_rs_list = [_.return_as_dict() for _ in usr_results]
    for line in usr_rs_list:
        print(line)

    print("--- {:^15} ---".format("documents"))
    doc_results = session.query(DBAl.Document).all()
    doc_rs_list = [_.return_as_dict() for _ in doc_results]
    for line in doc_rs_list:
        print(line)

    print("--- {:^15} ---".format("records"))
    rec_results = session.query(DBAl.Record).all()
    rec_rs_list = [_.return_as_dict() for _ in rec_results]
    for line in rec_rs_list:
        print(line)

    print("--- {:^15} ---".format("merkletrees"))
    mtr_results = session.query(DBAl.MerkleTree).all()
    mtr_rs_list = [_.return_as_dict() for _ in mtr_results]
    for line in mtr_rs_list:
        print(line)

    print("--- {:^15} ---".format("scheduledtasks"))
    sch_results = session.query(DBAl.ScheduledTask).all()
    sch_rs_list = [_.return_as_dict() for _ in sch_results]
    for line in sch_rs_list:
        print(line)

    print("--- {:^15} ---".format("restrictedips"))
    ips_results = session.query(DBAl.RestrictedIP).all()
    ips_rs_list = [_.return_as_dict() for _ in ips_results]
    for line in ips_rs_list:
        print(line)

    session.close()
