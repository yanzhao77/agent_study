import sys

menu_dict = {1: "添加学生(学生编号，学生姓名，手机号)",
             2: "删除学生(根据编号删除)",
             3: "修改学生信息(只能改姓名，手机号)",
             4: "查询单个学生信息(根据姓名查)",
             5: "查询所有学生信息",
             6: "退出系统",
             }
student_dict = {
    1: ["张三", "男", 110],
    2: ["李四", "女", 120],
    3: ["王麻子", "男", 119],
}


def add_student(student_arr: list):
    # 修复：编号统一转为 int 作为字典的 key
    student_num = int(student_arr[0])
    if student_num not in student_dict:
        student_dict[student_num] = student_arr
        return True
    return False


def delete_student(student_num: int):
    if student_num in student_dict:
        del student_dict[student_num]


def update_student(student_num: int, student_arr: list):
    if student_num in student_dict:
        # 原数组: [姓名, 性别, 手机号]
        # 新的列表保留原来的性别，只更新姓名和手机号
        old_sex = student_dict[student_num][1]
        # 注意：传入的 student_arr 是 [姓名, 手机号]
        student_dict[student_num] = [student_arr[0], old_sex, student_arr[1]]
        return True
    return False


def find_student(student_num: int):
    if student_num in student_dict:
        return student_dict[student_num]


def find_student_by_name(student_name: str):
    # 修复：不要在循环里盲目 print，找到后再返回
    for student_num, student_arr in student_dict.items():
        if student_name == student_arr[0]:  # 姓名通常在索引 0
            return student_num, student_arr
    return None, None


def show_student(student_arr: list = None):
    if student_arr is not None:
        print(student_arr)
    else:
        if not student_dict:
            print("暂无学生信息")
        for student_num, student_arr in student_dict.items():
            print(f"编号: {student_num}, 信息: {student_arr}")
    print()


def show_menu():
    for menu_num, menu_value in menu_dict.items():
        print(menu_num, menu_value)
    print()


# ============ 下面是各个功能菜单的交互逻辑 ============

def add_student_menu():
    student_num = user_input_str("编号")
    # 防止编号重复
    if int(student_num) in student_dict:
         print("添加失败：该编号已存在！")
         return

    student_name = user_input_str("名字")
    student_sex = user_input_str("性别")
    student_phone_num = user_input_str("手机号")
    
    add_student([student_num, student_name, student_sex, student_phone_num])
    
    print("添加完成！")
    show_student(find_student(int(student_num)))
    return


def delete_student_menu():
    student_num = user_input_str("要删除的学生编号")
    if int(student_num) not in student_dict:
        print("删除失败：找不到该编号的学生！")
        return
        
    student_arr = find_student(int(student_num))
    delete_student(int(student_num))
    
    print("删除完成！已删除的学生信息：")
    show_student(student_arr)


def update_student_menu():
    student_num = user_input_str("要修改的学生编号")
    
    if int(student_num) not in student_dict:
        print("修改失败：找不到该编号的学生！")
        return
        
    print("当前学生信息：", student_dict[int(student_num)])
    print("--- 修改学生信息 (只能改姓名和手机号) ---")
    
    new_name = user_input_str("新姓名")
    new_phone = user_input_str("新手机号")
    
    # 传入只包含 [姓名, 手机号] 的列表
    update_student(int(student_num), [new_name, new_phone])
    
    print("修改完成！最新信息如下：")
    show_student(find_student(int(student_num)))


def find_student_menu():
    student_name = user_input_str("要查询的学生姓名")
    stu_num, stu_info = find_student_by_name(student_name)
    
    if stu_info is not None:
        print(f"查询到学生 -> 编号: {stu_num}, 信息: {stu_info}")
    else:
        print("未查询到该姓名的学生。")


def show_all_menu():
    print("--- 所有学生信息 ---")
    show_student()


# ============ 主流程控制 ============

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
        print("退出系统，再见！")
        sys.exit(0)


def user_input_str(str_type: str = ''):
    # 简化了你的逻辑，直接判断空字符串即可
    if not str_type:
        print("请输入：")
    else:
        print(f"请输入{str_type}：", end="")
    return str(input()).strip()


if __name__ == '__main__':
    while True:
        show_menu()
        cont = input("请选择操作(1-6)：").strip()
        
        # 优化：先判断输入是否为空，然后再尝试转换 int
        if cont.isdigit() and int(cont) in menu_dict:
            main_menu(int(cont))
        else:
            print("输入错误，请输入 1-6 之间的数字！\n")