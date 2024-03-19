# # # import time 
# # # import hashlib
# # # # data ="fsyj2022@163.com" + str(time.time())
# # # # print(data)
# # # # token = hashlib.sha256(data.encode()).hexdigest()
# # # # print(token)
# # # # token = token+"t"+str(int(time.time()))
# # # # print(token)



# # # data = "1234" + str(time.time())
# # # token = hashlib.sha256(data.encode()).hexdigest()
# # # token = token+"t"+str(int(time.time()))
# # # print(token)


# # # result = ((1 * 2.56 * 10**9 + 12 * 1.28 * 10**9) / 2.8 - 1 * 2.56 * 10**9 ) /1.28 / 10**9

# # # result =700 * ( 3*10**9 ) / (2.389 *10 **12 *0.85)
# # result =   (250-70-85-40)
# # print(result)
# def get_substring_after_last_occurrence(input_string, char="t"):
#     last_index = input_string.rfind(char)
    
#     if last_index != -1 and last_index < len(input_string) - 1:
#         substring_after_char = input_string[last_index + 1:]
#         return substring_after_char
#     else:
#         return "未找到字符{}或者{}是最后一个字符".format(char, char)

# # 示例用法
# token = "1231234127dhsdhafgsdt12345678907hhj"
# result = get_substring_after_last_occurrence(token)
# print(result)


import matplotlib.pyplot as plt

# 定义费用项目和对应金额
import matplotlib
cost_items = {'其他', '办公费用', '人工费用', '产品维护与质量检测', '数据库与决策模型完善'};
cost_values = [25000, 50000, 200000, 225000, 500000];
matplotlib.rc("font",family='YouYuan')

# 绘制饼状图
plt.figure(figsize=(8, 8))
plt.pie(cost_values, labels=cost_items, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('各项费用占比')
plt.show()
