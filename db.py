import sqlite3
def insert_db(info_dict):
    # 建立資料庫
    conn = sqlite3.connect("104job.db")
    cursor = conn.cursor()
    # 建立資料表
    sql = '''CREATE TABLE IF NOT EXISTS job_info(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            job_time TEXT,
            company_name TEXT,
            job_name TEXT,
            job_area TEXT,
            job_years TEXT,
            education TEXT,
            job_describe TEXT,
            job_info TEXT,
            job_104url TEXT)'''
    cursor.execute(sql)
    cursor.close()
    conn.close()
    
    conn = sqlite3.connect("104job.db")
    temp_id = info_dict['job_id']
    info = conn.execute("SELECT * FROM job_info WHERE job_id = '%s'" % temp_id).fetchall()   
    if info:
        # 元組資料轉陣列
        info_list = list(info[0])
        info_list[1] = info_dict.get('job_id','')
        info_list[2] = info_dict.get('job_time','')
        info_list[3] = info_dict.get('company_name','')
        info_list[4] = info_dict.get('job_name','')
        info_list[5] = info_dict.get('job_area','')
        info_list[6] = info_dict.get('job_years','')
        info_list[7] = info_dict.get('education','')
        info_list[8] = info_dict.get('job_describe','')
        info_list[9] = info_dict.get('job_info','')
        info_list[10] = info_dict.get('job_104url','')
        sql = '''UPDATE job_info
        SET (job_id, job_time, company_name, job_name, job_area, job_years, education, job_describe, job_info, job_104url) 
        = ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")
        WHERE job_id = "%s" ''' % (info_list[1], info_list[2], info_list[3], info_list[4], info_list[5],
                                   info_list[6], info_list[7], info_list[8], info_list[9], info_list[10], temp_id)
        conn.execute(sql)
        conn.commit()
    else:
        job_id = info_dict.get('job_id','')
        job_time = info_dict.get('job_time','')
        company_name = info_dict.get('company_name','')
        job_name = info_dict.get('job_name','')
        job_area = info_dict.get('job_area','')
        job_years = info_dict.get('job_years','')
        education = info_dict.get('education','')
        job_describe = info_dict.get('job_describe','')
        job_info = info_dict.get('job_info','')
        job_104url = info_dict.get('job_104url','')
        insert_data = (job_id, job_time, company_name, job_name, job_area, job_years,
                    education, job_describe, job_info, job_104url)
        sql = '''INSERT into job_info(job_id, job_time, company_name, job_name, job_area,
            job_years, education, job_describe, job_info, job_104url) values(?,?,?,?,?,?,?,?,?,?)'''
        conn.execute(sql, insert_data)
        conn.commit()
    conn.close()        
        