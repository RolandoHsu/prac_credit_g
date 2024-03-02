# %% 
from bodun_package_file import bodun_package as bodun
import pandas as pd
import numpy as np
## 檢定
from scipy.stats import chi2_contingency
## 標準化
from sklearn.preprocessing import StandardScaler

# %%
######################################################### 原始資料
sql = f""" select * from practice.credit_g """
credit_g = bodun.pull_data_from_mysql(sql, 'practice')
credit_g.head(2)
# %%
######################################################### 字典檔
sql = f""" select * from practice.credit_g_dict"""
credit_g_dict = bodun.pull_data_from_mysql(sql, 'practice')
credit_g_dict.head(2)
# %%

credit_g_m = credit_g.copy()
# %%
######################################################### 因子建構
credit_g_m['sex'] = np.where(credit_g_m['personal_status'].str.contains('female'), 'female', 'male')

# %%
######################################################### 因子轉換
##### credit_history
credit_history_a = credit_g[credit_g['credit_history'].isin(['no credits/all paid'])]
credit_history_b = credit_g[credit_g['credit_history'].isin(['all paid'])]
print(credit_history_a[['credit_history', 'class']].groupby('class').count())
print(credit_history_b[['credit_history', 'class']].groupby('class').count())

data = [[25, 15], [28, 21]]
chi2, p, dof, expected = chi2_contingency(data)
print(f"Chi-square statistic: {chi2}")
print(f"P-value: {p}")

if p < 0.05:
    print("兩客群class分布有顯著差異")
else:
    print("兩客群class分布無顯著差異")

credit_g_m['credit_history'] = np.where(credit_g_m['credit_history'].isin(['no credits/all paid', 'all paid']), 
                                        'normal',
                                        credit_g_m['credit_history'])

# %%
credit_g_m['credit_history'].unique()

# %%
print(len(credit_g_m.columns))
credit_g_m.head(2)
# %%
######################################################### class處理
## 將class 轉換為 0: good ; 1: bad
credit_g_m['class'] = np.where(credit_g_m['class'] == 'good', 0, 1)
# %% 

######################################################### 各因子處理
credit_g_m.select_dtypes(include=['object', 'category']).columns
# %%
###### checking_status
filters = [
   credit_g_m.checking_status == 'no checking',
   credit_g_m.checking_status == '<0',
   credit_g_m.checking_status == '0<=X<200',
   credit_g_m.checking_status == '>=200'
]
values = ['a', 'b', 'c', 'd']
credit_g_m["checking_status"] = np.select(filters, values)
credit_g_m['checking_status'].unique()
# %%
###### credit_history
filters = [
   credit_g_m.credit_history == 'critical/other existing credit',
   credit_g_m.credit_history == 'delayed previously',
   credit_g_m.credit_history == 'existing paid',
   credit_g_m.credit_history == 'normal'
]
values = ['a', 'b', 'c', 'd']
credit_g_m["credit_history"] = np.select(filters, values)
credit_g_m['credit_history'].unique()
# %%

filters = [
   credit_g_m.purpose == 'radio/tv',
   credit_g_m.purpose == 'furniture/equipment',
   credit_g_m.purpose == 'new car',
   credit_g_m.purpose == 'used car',
   credit_g_m.purpose == 'domestic appliance'
]
values = ['radio_tv', 'furniture_equipment', 'new_car', 'used_car', 'domestic_appliance']
credit_g_m["purpose"] = np.select(filters, values, credit_g_m["purpose"])
credit_g_m['purpose'].unique()
# %%
credit_g_m['savings_status'].unique()
filters = [
    credit_g_m.savings_status == 'no known savings',
    credit_g_m.savings_status == '<100',
    credit_g_m.savings_status == '100<=X<500',
    credit_g_m.savings_status == '500<=X<1000',
    credit_g_m.savings_status == '>=1000'
]
values = ['a', 'b', 'c', 'd', 'e']
credit_g_m["savings_status"] = np.select(filters, values)
credit_g_m['savings_status'].unique()
# %%
credit_g_m['employment'].unique()
filters = [
    credit_g_m.employment == 'unemployed',
    credit_g_m.employment == '<1',
    credit_g_m.employment == '1<=X<4',
    credit_g_m.employment == '4<=X<7',
    credit_g_m.employment == '>=7'
]
values = ['a', 'b', 'c', 'd', 'e']
credit_g_m["employment"] = np.select(filters, values)
credit_g_m['employment'].unique()
# %%
credit_g_m['other_parties'] = np.where(credit_g_m['other_parties'] == 'co applicant', 'co_applicant', credit_g_m['other_parties'])
credit_g_m['other_parties'].unique()
# %%
credit_g_m['property_magnitude'] = credit_g_m['property_magnitude'].str.replace(' ', '_', regex=True)
credit_g_m['property_magnitude'].unique()
# %%
credit_g_m['housing'] = credit_g_m['housing'].str.replace(' ', '_', regex=True)
credit_g_m['housing'].unique()
# %%
credit_g_m['job'] = credit_g_m['job'].str.replace(' ', '_', regex=True)
credit_g_m['job'] = credit_g_m['job'].str.replace('/', '_', regex=True)
credit_g_m['job'].unique()
# %%
credit_g_m['sex'].unique()



# %% 
## 將調整後的資料存入mysql 中
bodun.save_data_into_mysql(credit_g_m, 'credit_g_m', 'practice', 'replace')


## 建立暗碼對照表
# %%
col_name = 'checking_status'
definitions = [
    'no checking',
    '<0',
    '0<=X<200',
    '>=200'
]
codes = ['a', 'b', 'c', 'd']

# 創建一個字典，然後轉換成DataFrame
data = {
    'col_name': [col_name] * len(definitions),
    'definition': definitions,
    'code': codes
}
code_table = pd.DataFrame(data)
code_table

# %%
col_name_credit_history = 'credit_history'
definitions_credit_history = [
    'critical/other existing credit',
    'delayed previously',
    'existing paid',
    'normal'
]
codes_credit_history = ['a', 'b', 'c', 'd']

# 創建關於credit_history的對照表資料
data_credit_history = {
    'col_name': [col_name_credit_history] * len(definitions_credit_history),
    'definition': definitions_credit_history,
    'code': codes_credit_history
}
credit_history_table = pd.DataFrame(data_credit_history)

# 將新的對照表資料附加到現有的code_table中
code_table = pd.concat([code_table, credit_history_table], ignore_index=True)

# %%
code_table
# %%
# 新的對照表資料：savings_status
col_name_savings_status = 'savings_status'
definitions_savings_status = [
    'no known savings',
    '<100',
    '100<=X<500',
    '500<=X<1000',
    '>=1000'
]
codes_savings_status = ['a', 'b', 'c', 'd', 'e']

# 創建關於savings_status的對照表資料
data_savings_status = {
    'col_name': [col_name_savings_status] * len(definitions_savings_status),
    'definition': definitions_savings_status,
    'code': codes_savings_status
}
savings_status_table = pd.DataFrame(data_savings_status)

# 將新的對照表資料附加到現有的code_table中
code_table = pd.concat([code_table, savings_status_table], ignore_index=True)

# 顯示更新後的code_table
code_table

# %%
# 新的對照表資料：employment
col_name_employment = 'employment'
definitions_employment = [
    'unemployed',
    '<1',
    '1<=X<4',
    '4<=X<7',
    '>=7'
]
codes_employment = ['a', 'b', 'c', 'd', 'e']

# 創建關於employment的對照表資料
data_employment = {
    'col_name': [col_name_employment] * len(definitions_employment),
    'definition': definitions_employment,
    'code': codes_employment
}
employment_table = pd.DataFrame(data_employment)

# 將新的對照表資料附加到現有的code_table中
code_table = pd.concat([code_table, employment_table], ignore_index=True)

# 顯示更新後的code_table
code_table

# %%
bodun.save_data_into_mysql(code_table, 'credit_g_code_table', 'practice', 'replace')
# %%
code_table
# %%
