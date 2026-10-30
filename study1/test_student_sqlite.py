import sys
import sqlite3

# ================= 数据库相关配置 =================
DB_FILE = 'student_system.db'


def init_db():
    """初始化数据库，如果表不存在则创建"""
    # 使用 with 语句可以自动管理连接的关闭和提交
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # 创建学生表 (编号为主键，姓名，性别，手机号)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS students
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY,
                           name
                           TEXT
                           NOT
                           NULL,
                           gender
                           TEXT,
                           phone
                           TEXT
                       )
                       ''')
        conn.commit()

        # 插入一些初始测试数据（如果表是空的）
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            test_data = [
                (1, "张三", "男", "110"),
                (2, "李四", "女", "120"),
                (3, "王麻子", "男", "119")
            ]
            cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", test_data)
            conn.commit()


# ================= 数据库操作层 (CRUD) =================

def db_add_student(student_id: int, name: str, gender: str, phone: str):
    """添加学生，返回是否成功"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (id, name, gender, phone) VALUES (?, ?, ?, ?)",
                (student_id, name, gender, phone)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        # 主键冲突（编号已存在）会触发这个错误
        return False


def db_delete_student(student_id: int):
    """删除学生，返回受影响的行数"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return cursor.rowcount  # 返回删除了几条数据


def db_update_student(student_id: int, name: str, phone: str):
    """修改学生姓名和手机号，返回受影响的行数"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, phone = ? WHERE id = ?",
            (name, phone, student_id)
        )
        conn.commit()
        return cursor.rowcount


def db_find_by_id(student_id: int):
    """根据编号查询，返回单条元组 (id, name, gender, phone)"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        return cursor.fetchone()


def db_find_by_name(name: str):
    """根据姓名查询，可能重名，返回列表"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # 使用模糊查询，支持模糊搜索
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
        return cursor.fetchall()


def db_get_all_students():
    """查询所有学生"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()


# ================= 交互界面层 =================

menu_dict = {
    1: "添加学生(学生编号，学生姓名，性别，手机号)",
    2: "删除学生(根据编号删除)",
    3: "修改学生信息(只能改姓名，手机号)",
    4: "查询单个学生信息(根据姓名查)",
    5: "查询所有学生信息",
    6: "退出系统",
}


def user_input_str(str_type: str = '') -> str:
    """获取字符串输入"""
    if not str_type:
        print("请输入：", end="")
    else:
        print(f"请输入{str_type}：", end="")
    return str(input()).strip()


def user_input_int(str_type: str = '') -> int:
    """获取整数输入，带容错处理"""
    while True:
        val = user_input_str(str_type)
        if val.isdigit():
            return int(val)
        print("⚠️ 输入无效，请输入纯数字！")


def show_menu():
    print("\n" + "=" * 40)
    for menu_num, menu_value in menu_dict.items():
        print(f"  {menu_num}. {menu_value}")
    print("=" * 40)


def print_student_table(students):
    """格式化打印学生列表（模拟表格）"""
    if not students:
        print("暂无学生信息。")
        return

    print("-" * 50)
    print(f"{'编号':<8}{'姓名':<10}{'性别':<8}{'手机号':<15}")
    print("-" * 50)
    for stu in students:
        # stu 是一个元组 (id, name, gender, phone)
        print(f"{stu[0]:<8}{stu[1]:<10}{stu[2]:<8}{stu[3]:<15}")
    print("-" * 50)


# ================= 菜单功能实现 =================

def add_student_menu():
    student_id = user_input_int("编号")
    # 先查一下编号是否存在
    if db_find_by_id(student_id):
        print("❌ 添加失败：该编号已存在！")
        return

    name = user_input_str("名字")
    gender = user_input_str("性别")
    phone = user_input_str("手机号")

    if db_add_student(student_id, name, gender, phone):
        print("✅ 添加成功！")
    else:
        print("❌ 添加失败，请稍后重试。")


def delete_student_menu():
    student_id = user_input_int("要删除的学生编号")
    affected = db_delete_student(student_id)
    if affected > 0:
        print("✅ 删除成功！")
    else:
        print("❌ 删除失败：找不到该编号的学生。")


def update_student_menu():
    student_id = user_input_int("要修改的学生编号")
    # 先查出来，确认存在
    student = db_find_by_id(student_id)

    if not student:
        print("❌ 修改失败：找不到该编号的学生。")
        return

    print(f"当前学生信息 -> 姓名: {student[1]}, 性别: {student[2]}, 手机号: {student[3]}")
    print("--- 请输入新信息 (性别不可改) ---")

    new_name = user_input_str("新姓名")
    new_phone = user_input_str("新手机号")

    affected = db_update_student(student_id, new_name, new_phone)
    if affected > 0:
        print("✅ 修改成功！最新信息：")
        print_student_table([db_find_by_id(student_id)])
    else:
        print("❌ 修改失败。")


def find_student_menu():
    name = user_input_str("要查询的学生姓名")
    students = db_find_by_name(name)
    if students:
        print(f"✅ 找到 {len(students)} 条记录：")
        print_student_table(students)
    else:
        print("❌ 未查询到该姓名的学生。")


def show_all_menu():
    students = db_get_all_students()
    print_student_table(students)


# ================= 主程序 =================

def main_menu(menu_num: int):
    if menu_num == 1:
        add_student_menu()
    elif menu_num == 2:
        delete_student_menu()
    elif menu_num == 3:
        update_student_menu()
    elif menu_num == 4:
        find_student_menu()
    elif menu_num == 5:
        show_all_menu()
    elif menu_num == 6:
        print("👋 退出系统，再见！")
        sys.exit(0)


if __name__ == '__main__':
    # 启动前先初始化数据库
    init_db()
    print("🎓 欢迎使用学生信息管理系统 (SQLite版)")

    while True:
        show_menu()
        cont = input("请选择操作(1-6)：").strip()

        if cont.isdigit() and int(cont) in menu_dict:
            main_menu(int(cont))
        else:
            print("⚠️ 输入错误，请输入 1-6 之间的数字！")