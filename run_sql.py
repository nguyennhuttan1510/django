import sqlite3
import time
from datetime import datetime


def create_connection(db_file):
    """Tạo kết nối đến cơ sở dữ liệu SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    """Tạo bảng mẫu nếu chưa tồn tại"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sample_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL,
        timestamp TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def optimize_connection(conn):
    """Tối ưu hóa kết nối cho việc chèn dữ liệu số lượng lớn"""
    conn.execute("PRAGMA synchronous = OFF")
    conn.execute("PRAGMA journal_mode = MEMORY")


def insert_records(conn, num_records):
    """Chèn số lượng bản ghi đã chỉ định vào bảng"""
    sql = "INSERT INTO sample_table (name, value, timestamp) VALUES (?, ?, ?)"
    try:
        cur = conn.cursor()
        start_time = time.time()
        for i in range(num_records):
            name = f"Name_{i}"
            value = i * 1.1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(sql, (name, value, timestamp))
            if (i + 1) % 1000 == 0:
                conn.commit()
                print(f"Đã chèn {i + 1} bản ghi")
        conn.commit()
        end_time = time.time()
        print(f"Đã chèn {num_records} bản ghi trong {end_time - start_time:.2f} giây")
    except sqlite3.Error as e:
        print(e)


def main():
    database = "db.sqlite3"
    num_records = 10000

    # Tạo kết nối
    conn = create_connection(database)

    if conn is not None:
        # Tạo bảng
        create_table(conn)

        # Tối ưu hóa kết nối
        optimize_connection(conn)

        # Chèn bản ghi
        insert_records(conn, num_records)

        # Đóng kết nối
        conn.close()
    else:
        print("Lỗi! Không thể tạo kết nối đến cơ sở dữ liệu.")


if __name__ == '__main__':
    main()