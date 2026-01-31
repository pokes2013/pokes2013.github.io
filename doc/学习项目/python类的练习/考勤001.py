import xlrd
import pandas as pd
from datetime import datetime, timedelta
import calendar


def get_standard_work_time(file_path, employee_name):
    """
    从Excel的人员信息表中获取指定员工的标准上班时间
    参数:
        file_path: Excel文件路径
        employee_name: 要查询的员工姓名
    返回:
        标准上班时间（datetime.time对象），若未找到返回None
    """
    try:
        # 读取"人员信息"工作表（按位置索引列，B列=1，D列=3）
        df_info = pd.read_excel(file_path, sheet_name="人员信息", header=None)
        # 查找B列中等于employee_name的行
        matched_rows = df_info[df_info[1] == employee_name]
        # 未找到匹配员工
        if matched_rows.empty:
            print(f"⚠️ 未找到员工【{employee_name}】的信息")
            return None
        # 获取D列的标准上班时间
        standard_time_str = matched_rows.iloc[0, 3]
        # 处理空值情况
        if pd.isna(standard_time_str):
            print(f"⚠️ 员工【{employee_name}】的标准上班时间为空")
            return None
        # 转换为datetime.time对象（兼容不同格式的时间字符串）
        try:
            # 处理 HH:MM:SS 或 HH:MM 格式
            if len(str(standard_time_str).split(':')) >= 2:
                standard_time = datetime.strptime(str(standard_time_str), "%H:%M:%S").time()
            else:
                standard_time = datetime.strptime(str(standard_time_str), "%H:%M").time()
            return standard_time
        except ValueError:
            print(f"⚠️ 员工【{employee_name}】的标准上班时间格式错误：{standard_time_str}")
            return None
    except FileNotFoundError:
        print(f"❌ 错误：未找到文件【{file_path}】")
        return None
    except Exception as e:
        print(f"❌ 读取人员信息时发生错误：{str(e)}")
        return None


def round_to_half_hour(dt):
    """
    将时间四舍五入到最近的0.5小时（30分钟）
    例如：17:59 → 18:00，17:14 → 17:00，17:15 → 17:30
    参数:
        dt: datetime对象
    返回:
        四舍五入后的datetime对象
    """
    # 计算总分钟数
    total_minutes = dt.hour * 60 + dt.minute
    # 按30分钟为单位四舍五入
    rounded_minutes = round(total_minutes / 30) * 30
    # 处理跨小时/跨天情况
    rounded_hours = rounded_minutes // 60
    rounded_min_remainder = rounded_minutes % 60
    # 构建新的datetime对象（日期保持不变）
    rounded_dt = datetime(
        dt.year, dt.month, dt.day,
        hour=rounded_hours % 24,
        minute=rounded_min_remainder,
        second=0
    )
    # 处理跨天（如23:45 → 00:00）
    if rounded_hours >= 24:
        rounded_dt += timedelta(days=1)
    return rounded_dt


def calculate_work_hours(row, standard_work_time):
    """
    最终优化版工时计算规则：
    1. 迟到≤5分钟 → 视为按标准时间打卡，工时=最后打卡-标准时间
    2. 迟到>5分钟 → 工时=最后打卡-首次打卡
    3. 工时计算时，打卡时间先四舍五入到0.5小时单位
    4. 请假≥4小时：不扣除中午休息时间
    5. 请假<4小时/未请假：扣除1小时中午休息时间
    参数:
        row: DataFrame的行数据
        standard_work_time: 标准上班时间（datetime.time对象）
    返回:
        工时字符串（如 "8:00"）或 NaN
    """
    # 无标准上班时间/无首次打卡/无最后打卡，返回NaN
    if (standard_work_time is None or
            pd.isna(row['首次打卡']) or
            pd.isna(row['最后打卡'])):
        return pd.NA
    first_punch_str = row['首次打卡']
    last_punch_str = row['最后打卡']
    base_date = datetime(2024, 1, 1)  # 基准日期（仅用于time转datetime）
    try:
        # 转换首次打卡时间为datetime.time对象
        if len(str(first_punch_str).split(':')) >= 2:
            first_punch_time = datetime.strptime(str(first_punch_str), "%H:%M:%S").time()
        else:
            first_punch_time = datetime.strptime(str(first_punch_str), "%H:%M").time()
        # 转换最后打卡时间为datetime.time对象
        if len(str(last_punch_str).split(':')) >= 2:
            last_punch_time = datetime.strptime(str(last_punch_str), "%H:%M:%S").time()
        else:
            last_punch_time = datetime.strptime(str(last_punch_str), "%H:%M").time()
        # 转换为datetime对象
        first_punch_dt = datetime.combine(base_date, first_punch_time)
        last_punch_dt = datetime.combine(base_date, last_punch_time)
        standard_dt = datetime.combine(base_date, standard_work_time)
        # 1. 四舍五入打卡时间到0.5小时单位
        first_punch_rounded = round_to_half_hour(first_punch_dt)
        last_punch_rounded = round_to_half_hour(last_punch_dt)
        standard_rounded = round_to_half_hour(standard_dt)
        # 2. 获取迟到分钟数，判断是否≤5分钟
        late_minutes = row['迟到分钟数']
        if pd.isna(late_minutes) or late_minutes <= 5:
            # 迟到≤5分钟：视为按标准时间打卡，基准=标准时间
            time_diff = last_punch_rounded - standard_rounded
        else:
            # 迟到>5分钟：基准=首次打卡时间
            time_diff = last_punch_rounded - first_punch_rounded
        # 处理跨天情况（如最后打卡时间早于计算基准）
        if time_diff.total_seconds() < 0:
            time_diff += timedelta(days=1)
        # 3. 判断是否请假≥4小时（240分钟）
        leave_4h_flag = False
        if not pd.isna(late_minutes) and late_minutes >= 240:
            leave_4h_flag = True
        # 4. 扣除休息时间逻辑
        if leave_4h_flag:
            total_seconds = time_diff.total_seconds()  # 请假≥4小时：不扣休息
        else:
            total_seconds = time_diff.total_seconds() - 3600  # 否则扣1小时休息
        # 处理扣除休息后时长为负的情况
        if total_seconds < 0:
            total_seconds = 0
        # 转换为小时和分钟（确保显示为0.5小时单位）
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        # 确保分钟数为0或30（0.5小时单位）
        if minutes > 15:
            minutes = 30
        elif minutes > 0:
            minutes = 0
        return f"{hours}:{minutes:02d}"
    except ValueError as e:
        print(f"⚠️ 时间格式错误（员工：{row['姓名']}，日期：{row['日期']}）：{str(e)}")
        return pd.NA


def calculate_late_info(row, standard_work_time):
    """
    最终优化版迟到规则：
    - 迟到≤5分钟：不算迟到，视为按标准时间打卡（空标记+空分钟数）
    - 5<迟到<60分钟：算迟到（标记+分钟数）
    - 迟到≥60分钟：算请假（后续由calculate_leave_info处理）
    参数:
        row: DataFrame的行数据
        standard_work_time: 标准上班时间（datetime.time对象）
    返回:
        (迟到标记, 迟到分钟数)：标记为"迟到"/""，分钟数为数字/NaN
    """
    # 无标准上班时间或无首次打卡时间，返回空值
    if standard_work_time is None or pd.isna(row['首次打卡']):
        return "", pd.NA
    first_punch_str = row['首次打卡']
    try:
        # 转换首次打卡时间为datetime.time对象
        if len(str(first_punch_str).split(':')) >= 2:
            first_punch_time = datetime.strptime(str(first_punch_str), "%H:%M:%S").time()
        else:
            first_punch_time = datetime.strptime(str(first_punch_str), "%H:%M").time()
        # 转换为datetime对象计算差值
        base_date = datetime(2024, 1, 1)
        standard_dt = datetime.combine(base_date, standard_work_time)
        first_punch_dt = datetime.combine(base_date, first_punch_time)
        # 计算时间差（首次打卡 - 标准上班时间）
        time_diff = first_punch_dt - standard_dt
        late_seconds = time_diff.total_seconds()
        late_minutes = int(late_seconds // 60)
        # 最终规则：≤5分钟不算迟到，>5分钟才标记
        if late_minutes > 5:
            return "迟到", late_minutes
        else:
            return "", pd.NA  # ≤5分钟返回空标记+空分钟数
    except ValueError:
        print(f"⚠️ 首次打卡时间格式错误（员工：{row['姓名']}，日期：{row['日期']}）：{first_punch_str}")
        return "", pd.NA


def calculate_leave_info(row):
    """
    请假规则：
    - 迟到≥60分钟视为请假
    - 显示格式："请假1小时"/"请假90分钟"
    - 请假≥4小时：后续工时计算不扣休息时间
    参数:
        row: DataFrame的行数据
    返回:
        请假字符串（如"请假1小时"/"请假90分钟"）或空字符串
    """
    late_minutes = row['迟到分钟数']
    # 无迟到分钟数（未迟到/≤5分钟）返回空值
    if pd.isna(late_minutes):
        return ""
    # 迟到≥60分钟（1小时）视为请假
    if late_minutes >= 60:
        hours = late_minutes // 60
        mins = late_minutes % 60
        # 整小时显示"请假x小时"，非整小时显示"请假x分钟"
        if mins == 0:
            return f"请假{hours}小时"
        else:
            return f"请假{late_minutes}分钟"
    else:
        return ""  # 迟到<60分钟不标记请假


def check_work_hours_exception(row):
    """
    判断工时是否异常（阈值为7.5小时）
    参数:
        row: DataFrame的行数据
    返回:
        "工时异常" / "" / NaN
    """
    work_hours_str = row['工时']
    # 无工时数据（休息天/格式错误）返回空值
    if pd.isna(work_hours_str):
        return pd.NA
    try:
        # 拆分工时为小时和分钟（如 "7:30" → 7小时30分钟）
        hours, minutes = map(int, work_hours_str.split(':'))
        # 转换为总小时数（保留两位小数）
        total_hours = hours + minutes / 60
        # 小于7.5小时才标记为工时异常
        if total_hours < 7.5:
            return "工时异常"
        else:
            return ""
    except (ValueError, IndexError):
        print(f"⚠️ 工时格式错误（员工：{row['姓名']}，日期：{row['日期']}）：{work_hours_str}")
        return pd.NA


def check_missing_punch(row):
    """
    判断是否缺卡（打卡次数<4，休息天除外）
    参数:
        row: DataFrame的行数据
    返回:
        "缺卡" / ""
    """
    punch_count = row['打卡次数']
    # 休息天（打卡次数0）不标记缺卡
    if punch_count == 0:
        return ""
    # 仅打卡次数<4时标记缺卡
    elif punch_count < 4:
        return "缺卡"
    else:
        return ""


# ==================== 主程序 ====================
if __name__ == "__main__":
    # ==================== 配置参数（请根据实际情况修改）====================
    file_path = "ceshi.xlsx"  # Excel文件路径
    # 员工姓名配置：支持3种模式
    # 模式1：处理所有员工（推荐）
    process_all_employees = True
    # 模式2：处理指定单个员工（将process_all_employees设为False）
    # target_employee = "严钰"
    # 模式3：处理指定多个员工（将process_all_employees设为False）
    # target_employees = ["严钰", "李丹", "林卓诚"]

    # ==================== 读取数据 ====================
    # 读取考勤数据（默认第一个工作表）
    df = pd.read_excel(file_path)
    # 读取人员信息表，获取所有在职员工姓名
    df_employees = pd.read_excel(file_path, sheet_name="人员信息")
    all_employee_names = df_employees['姓名'].dropna().unique().tolist()

    # ==================== 筛选要处理的员工 ====================
    if process_all_employees:
        # 处理所有员工
        employees_to_process = all_employee_names
        print(f"📋 开始处理所有员工（共{len(employees_to_process)}人）")
    else:
        # 处理指定员工（根据需要选择下面一种）
        # 单个员工
        # employees_to_process = [target_employee]
        # 多个员工
        # employees_to_process = target_employees
        pass

    # ==================== 数据预处理 ====================
    # 定义打卡列名列表
    punch_columns = ['早上上班', '早上下班', '下午上班', '下午下班', '末次打卡']


    # 新增"打卡次数"列
    def count_punch(row):
        count = 0
        for col in punch_columns:
            if pd.notna(row[col]) and row[col] != '休息':
                count += 1
        return count


    df['打卡次数'] = df.apply(count_punch, axis=1)


    # 新增"首次打卡"和"最后打卡"列
    def get_first_last_punch(row):
        punch_times = []
        for col in punch_columns:
            val = row[col]
            if pd.notna(val) and val != '休息':
                punch_times.append(val)
        if not punch_times:
            return pd.NA, pd.NA
        punch_times_sorted = sorted(punch_times)
        first_punch = punch_times_sorted[0]
        last_punch = punch_times_sorted[-1]
        return first_punch, last_punch


    df[['首次打卡', '最后打卡']] = df.apply(
        lambda row: pd.Series(get_first_last_punch(row)),
        axis=1
    )

    # ==================== 按员工逐个处理 ====================
    result_dfs = []
    for employee_name in employees_to_process:
        print(f"\n===== 正在处理员工：{employee_name} =====")

        # 筛选当前员工的数据
        df_employee = df[df['姓名'] == employee_name].copy()
        if df_employee.empty:
            print(f"⚠️ 未找到员工【{employee_name}】的考勤数据，跳过")
            continue

        # 获取当前员工的标准上班时间
        standard_work_time = get_standard_work_time(file_path, employee_name)
        if not standard_work_time:
            print(f"⚠️ 员工【{employee_name}】无有效标准上班时间，跳过工时计算")
            continue

        # 计算迟到信息
        df_employee[['迟到', '迟到分钟数']] = df_employee.apply(
            lambda row: pd.Series(calculate_late_info(row, standard_work_time)),
            axis=1
        )

        # 计算工时
        df_employee['工时'] = df_employee.apply(
            lambda row: calculate_work_hours(row, standard_work_time),
            axis=1
        )

        # 新增"中午休息"列（固定值1小时，仅作展示）
        df_employee['中午休息'] = "1小时"

        # 计算请假信息
        df_employee['请假'] = df_employee.apply(calculate_leave_info, axis=1)

        # 检查工时异常
        df_employee['工时异常'] = df_employee.apply(check_work_hours_exception, axis=1)

        # 检查缺卡
        df_employee['缺卡'] = df_employee.apply(check_missing_punch, axis=1)

        # 保存结果
        result_dfs.append(df_employee)

        # 打印当前员工的统计信息
        work_days = len(df_employee[df_employee['打卡次数'] > 0])
        late_days = len(df_employee[df_employee['迟到'] == '迟到'])
        leave_days = len(df_employee[df_employee['请假'] != ''])
        missing_punch_days = len(df_employee[df_employee['缺卡'] == '缺卡'])
        abnormal_hours_days = len(df_employee[df_employee['工时异常'] == '工时异常'])

        print(f"📊 员工【{employee_name}】统计：")
        print(f"   工作日数：{work_days}天")
        print(f"   迟到天数：{late_days}天")
        print(f"   请假天数：{leave_days}天")
        print(f"   缺卡天数：{missing_punch_days}天")
        print(f"   工时异常天数：{abnormal_hours_days}天")

    # ==================== 合并结果并保存 ====================
    if result_dfs:
        # 合并所有员工的结果
        final_df = pd.concat(result_dfs, ignore_index=True)

        # 定义展示列顺序（你想要的顺序）
        display_cols = [
            '姓名', '日期', '打卡次数', '首次打卡', '最后打卡', '缺卡',
            '中午休息', '迟到', '迟到分钟数', '请假', '工时异常', '工时'
        ]

        # 关键修复：重新排列DataFrame的列顺序
        # 先筛选出存在的列（避免列名错误导致报错）
        valid_cols = [col for col in display_cols if col in final_df.columns]
        final_df = final_df[valid_cols]

        # 显示完整结果（可选）
        print("\n===== 所有员工完整考勤统计结果 =====")
        print(final_df.to_string(index=False))  # 这里不需要再指定display_cols

        # 保存到新Excel文件（现在会按display_cols顺序保存）
        output_file = "处理后的考勤表_多员工.xlsx"
        final_df.to_excel(output_file, index=False)
        print(f"\n✅ 结果已保存到：{output_file}")

        # 显示员工标准信息汇总
        print("\n===== 员工标准信息汇总 =====")
        for employee_name in employees_to_process:
            standard_time = get_standard_work_time(file_path, employee_name)
            if standard_time:
                print(f"员工姓名：{employee_name}")
                print(f"标准上班时间：{standard_time.strftime('%H:%M:%S')}")
                print("-" * 30)
    else:
        print("\n❌ 未生成任何考勤结果，请检查员工姓名和考勤数据")