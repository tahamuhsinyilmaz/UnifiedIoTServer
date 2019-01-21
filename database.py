import psycopg2


class database :
    def insert_value(self,protocol,date,payload):
        sql = """INSERT INTO sensordata(protocol,date,payload)
                 VALUES(%s,%s,%s) ;"""
        conn = None
        try:
            conn = psycopg2.connect(host="localhost", database="IoTDB", user="postgres", password="Taha2010")
            cur = conn.cursor()
            cur.execute(sql,(protocol,date,payload))
            conn.commit()
            cur.close()
            print ('database done')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()