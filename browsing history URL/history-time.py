import sqlite3
import os
import getpass
import shutil
from win32com.client import Dispatch
from datetime import datetime, timedelta

def list_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

def convert_chrome_time(timestamp):
    try:
        return datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
    except OverflowError:
        return None

def convert_firefox_time(timestamp):
    try:
        return datetime(1970, 1, 1) + timedelta(microseconds=timestamp * 1000)
    except OverflowError:
        return None

def get_chrome_history(history_path):
    history_db = os.path.join(history_path, 'History')
    if not os.path.exists(history_db):
        print(f"Chrome history file not found at {history_db}")
        return []
    
    temp_db = history_db + '_copy'
    shutil.copy2(history_db, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT url, last_visit_time FROM urls")
    rows = cursor.fetchall()
    conn.close()
    os.remove(temp_db)

    urls = [(row[0], convert_chrome_time(row[1])) for row in rows if convert_chrome_time(row[1])]
    return urls

def get_firefox_history(history_path):
    history_db = os.path.join(history_path, 'places.sqlite')
    if not os.path.exists(history_db):
        print(f"Firefox history file not found at {history_db}")
        return []

    tables = list_tables(history_db)
    print(f"Available tables in {history_db}: {tables}")

    if 'moz_places' in tables:
        temp_db = history_db + '_copy'
        shutil.copy2(history_db, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, last_visit_date FROM moz_places")
        rows = cursor.fetchall()
        conn.close()
        os.remove(temp_db)

        urls = [(row[0], convert_firefox_time(row[1])) for row in rows if row[1] and convert_firefox_time(row[1])]
        return urls
    else:
        print("Table 'moz_places' not found.")
        return []

def get_ie_history():
    ie_history = []
    try:
        obj_shell = Dispatch('Shell.Application')
        obj_folder = obj_shell.Namespace(34)
        for item in obj_folder.Items():
            ie_history.append((item.Path, item.ModifyDate))
    except Exception as e:
        print(f"Error accessing IE history: {e}")
    return ie_history

def get_edge_history(history_path):
    history_db = os.path.join(history_path, 'History')
    if not os.path.exists(history_db):
        print(f"Edge history file not found at {history_db}")
        return []
    
    temp_db = history_db + '_copy'
    shutil.copy2(history_db, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT url, last_visit_time FROM urls")
    rows = cursor.fetchall()
    conn.close()
    os.remove(temp_db)

    urls = [(row[0], convert_chrome_time(row[1])) for row in rows if convert_chrome_time(row[1])]
    return urls

def save_to_txt(file_path, urls):
    with open(file_path, 'w') as f:
        for url, timestamp in urls:
            f.write(f"{url}\t{timestamp}\n")

# Lấy tên người dùng hiện tại
username = getpass.getuser()

# Đường dẫn tới thư mục lịch sử của Chrome, Edge và Firefox
chrome_history_path = os.path.join('C:\\Users', username, 'AppData\\Local\\Google\\Chrome\\User Data\\Default')
edge_history_path = os.path.join('C:\\Users', username, 'AppData\\Local\\Microsoft\\Edge\\User Data\\Default')
firefox_profiles_path = os.path.join('C:\\Users', username, 'AppData\\Roaming\\Mozilla\\Firefox\\Profiles')

# Trích xuất URL từ lịch sử của Chrome
chrome_urls = get_chrome_history(chrome_history_path)

# Trích xuất URL từ lịch sử của Edge
edge_urls = get_edge_history(edge_history_path)

# Trích xuất URL từ lịch sử của Firefox
firefox_urls = []

# Tìm tất cả các hồ sơ Firefox
if os.path.exists(firefox_profiles_path):
    for profile in os.listdir(firefox_profiles_path):
        profile_path = os.path.join(firefox_profiles_path, profile)
        if os.path.isdir(profile_path):
            firefox_urls.extend(get_firefox_history(profile_path))
else:
    print(f"Firefox profiles folder not found at {firefox_profiles_path}")

# Trích xuất URL từ lịch sử của IE
ie_urls = get_ie_history()

# Lưu URL vào file txt
save_to_txt('chrome_history.txt', chrome_urls)
save_to_txt('edge_history.txt', edge_urls)
save_to_txt('firefox_history.txt', firefox_urls)
save_to_txt('ie_history.txt', ie_urls)

print("Lịch sử duyệt web đã được trích xuất và lưu vào file txt.")
