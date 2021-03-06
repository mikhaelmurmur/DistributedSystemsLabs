import psycopg2
from configparser import ConfigParser
 
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db



def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        paramsflight = config('databaseflight.ini')
        paramshotel = config('databasehotel.ini')
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connFlight = psycopg2.connect(**paramsflight)
        connHotel = psycopg2.connect(**paramshotel)


        connFlight.tpc_begin(connFlight.xid(42, 'transaction ID', 'connection 1'))
        connHotel.tpc_begin(connHotel.xid(42, 'transaction ID', 'connection 2'))
        
        try:
            
            curFlight = connFlight.cursor()
            curHotel = connHotel.cursor()
            curHotel.execute('Insert into booking (clientname,hotelname,arrival,departure) VALUES ( \'Paul\', \'Ritz\', to_date(\'21-02-2010\', \'DD-MM-YYYY\') , to_date(\'21-03-2010\', \'DD-MM-YYYY\') );')
            
            connFlight.tpc_prepare()    
            connHotel.tpc_prepare()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            
            connFlight.tpc_rollback()
            connHotel.tpc_rollback()
        else:
            connFlight.tpc_commit()
            connHotel.tpc_commit()

        # create a cursor
        # cur = conn.cursor()

        # cur.execute('SELECT version()')
        # print('PostgreSQL database version:')
        
        # db_version = cur.fetchone()
        # print(db_version)

        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def main():
    connect()


if __name__ == "__main__":
    main()