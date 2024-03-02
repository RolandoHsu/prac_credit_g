# %%
from bodun_package_file import bodun_package as bodun
import pandas as pd
import numpy as np

## 繪圖
import matplotlib.pyplot as plt
import seaborn as sns

## 統計檢定
from scipy.stats import chi2_contingency
from scipy import stats
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
credit_g_dict[credit_g_dict['col_name'] == 'foreign_worker']['definition'].values[0]
# %%
######################################################### null值確認
check_null = credit_g.isnull().mean().to_frame().reset_index()
check_null.columns = ['col_name', 'null_rate']
check_null[check_null['null_rate'] != 0]

# %%
######################################################### 數值型變數
credit_g.describe()
# %% 
def get_hist_plot_n(df, col_name):
    # 繪製直方圖並獲取條形的信息
    n, bins, patches = plt.hist(df[col_name], bins=30, alpha=0.5, color='g', edgecolor='black')

    # 在每個條形上方顯示頻率值
    for patch in patches:
        height = patch.get_height()
        plt.text(patch.get_x() + patch.get_width() / 2, height + 3, f'{int(height)}', ha='center', va='bottom')

    plt.title(col_name)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()
# %%
for i in credit_g.select_dtypes(include=[np.number]).columns:
    get_hist_plot_n(credit_g, i)

# %%
############### 相關係數
corr_col = credit_g.select_dtypes(include=[np.number]).columns
correlation_matrix = credit_g[corr_col].corr()
correlation_matrix

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()
# %%
correlation_matrix
# %%
############### 尋找離群值
def find_outliers_by_iqr(df, feature):
    # 计算IQR
    q1 = df[feature].quantile(0.25)
    q3 = df[feature].quantile(0.75)
    iqr = q3 - q1
    print('評估指標: '+feature)
    # 计算离群值的边界
    lower_bound = q1 - 1.5 * iqr
    print('離群值下界: ', lower_bound)
    upper_bound = q3 + 1.5 * iqr
    print('離群值下界: ', upper_bound)
    # 确定数据中哪些是离群值
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    print('離群值樣本數: ', len(outliers))
    return outliers


for i in credit_g.select_dtypes(include=[np.number]).columns:
    find_outliers_by_iqr(credit_g, i)
    print('')

# %%
######################################################### 類別型變數
# %%
############################## 欄位值調整
### 年齡
filters = [
   credit_g.age < 20,
   (credit_g.age >=20) & (credit_g.age < 25),
   (credit_g.age >=25) & (credit_g.age < 30),
   (credit_g.age >=30) & (credit_g.age < 35),
   (credit_g.age >=35) & (credit_g.age < 40),
   (credit_g.age >=40) & (credit_g.age < 45),
   (credit_g.age >=45) & (credit_g.age < 50),
   (credit_g.age >=50) & (credit_g.age < 55),
   (credit_g.age >=55) & (credit_g.age < 60),
   (credit_g.age >=60) & (credit_g.age < 65),
   (credit_g.age >=65) & (credit_g.age < 70),
   credit_g.age >=70
]
values = ['01_<20', '02_<25', '03_<30', '04_<35', '05_<40', '06_<45', '07_<50',
          '08_<55', '09_<60', '10_<65', '11_<70', '12_<75'
          ]
credit_g["age_adj"] = np.select(filters, values)
credit_g.head(2)

#### 性別
credit_g['sex'] = np.where(credit_g['personal_status'].str.contains('female'), 'female', 'male')

# %%
# 繪製類別型變數的分佈圖
def get_hist_plot_c(data, col_name, order_method = 'b'):
    """
    參數定義:
        * order_method 
            * a : 依照類別名稱排序
            * b : 依照各類別佔比排序
            * 其他 : 可輸入自定義的排序list
    """
    if order_method == 'a':
        # 繪製計數直方圖
        ax = sns.countplot(x=col_name, data=data.sort_values(col_name))
    elif order_method == 'b':
        # 計算每個類別的計數並按計數降冪排序
        order = data[col_name].value_counts().index
        # 繪製計數直方圖，並按計數降冪排序
        ax = sns.countplot(x=col_name, data=data, order=order)
    else: ## 自定義排序
        ax = sns.countplot(x=col_name, data=data, order = order_method)
    
    plt.title(col_name)
    plt.xlabel('Category')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)

    # 計算總數以便計算百分比
    total = len(data)
    
    # 在每個柱子上方添加百分比
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        x = p.get_x() + p.get_width() / 2
        y = p.get_height()
        ax.annotate(percentage, (x, y), ha='center', va='bottom')

    plt.show()

# %%
i = 'checking_status'
order = ['no checking', '<0', '0<=X<200', '>=200']
get_hist_plot_c(credit_g, i, order_method = order)

# %%
for i in credit_g.select_dtypes(include=['object', 'category']).columns:
    if i == 'age_adj':
        get_hist_plot_c(credit_g, i, order_method = 'a')
    elif i == 'checking_status':
        order = ['no checking', '<0', '0<=X<200', '>=200']
        get_hist_plot_c(credit_g, i, order_method = order)
    elif i == 'savings_status':
        order = ['no known savings', '<100', '100<=X<500', '500<=X<1000', '>=1000']
        get_hist_plot_c(credit_g, i, order_method = order)
    elif i == 'employment':
        order = ['unemployed', '<1', '1<=X<4', '4<=X<7', '>=7']
        get_hist_plot_c(credit_g, i, order_method = order)
    else:
        get_hist_plot_c(credit_g, i)
# %%

# %%
######################################################### 探討各變數與class的關係
######################## 連續型變數
def get_vilinplot(data, col_name):
    sns.violinplot(x='class', y=col_name, data=data, color='g')
    plt.title(f'Relationship between {col_name} and Class')

    for i, group in enumerate(data['class'].unique()):
        median = data[data['class'] == group][col_name].median()
        plt.text(i, median, f'{median}', size='x-small', color='white')

    plt.show()

# %%
for i in credit_g.select_dtypes(include=[np.number]).columns:
    get_vilinplot(credit_g, i)
# %%

def perform_ttest(df, group_column, value_column):

    group_A = df[df[group_column] == df[group_column].unique()[0]][value_column]
    group_B = df[df[group_column] == df[group_column].unique()[1]][value_column]

    t_stat, p_value = stats.ttest_ind(group_A, group_B)
    print(f'{value_column}與class T檢定')
    print(f"T-statistic: {t_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print(f"兩類別之{value_column} 平均數存在顯著差異")
    else:
        print(f"沒有足夠的證據證明兩類別之{value_column} 平均數存在顯著差異")
    print('')
    return t_stat, p_value

for i in credit_g.select_dtypes(include=[np.number]).columns:
    perform_ttest(credit_g, 'class', i)

# %%
######################## 類別型變數
def chi_square_test(df, class_variable, variable1):

    contingency_table = pd.crosstab(df[variable1], df[class_variable])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    print(f'{variable1}與class 卡方檢定')
    print(f"Chi-squared: {chi2}")
    print(f"P-value: {p}")
    if p < 0.05:
        print(f"兩變數存在顯著關聯")
    else:
        print(f"沒有足夠的證據證明兩變數存在顯著關聯")
    print('')

for i in credit_g.select_dtypes(include=['object', 'category']).columns:
    if i == 'class':
        pass
    else:
        chi_square_test(credit_g, 'class', i)


# %%
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='checking_status', hue='class', data=credit_g)
plt.title(f"{'credit_history'} Distribution with Class Proportions")
plt.xlabel('credit_history')
plt.ylabel('Frequency')
plt.legend(title='Class')
# 计算每个category_variable值下的class总数
category_counts = credit_g.groupby('checking_status')['class'].value_counts().unstack().fillna(0)

# 在每个条形上添加占比标签
for p in ax.patches:
    category = p.get_x()  # 获取category_variable的位置索引，用于从category_counts中找到对应的计数
    value = p.get_height()  # 条形的高度，即当前class在特定category_variable值下的计数
    total = category_counts.iloc[int(category)].sum()  # 获取当前category_variable值的总计数
    percentage = f'{100 * value/total:.1f}%'  # 计算占比并格式化为百分比
    
    # 设置标签位置和文本
    x = p.get_x() + p.get_width() / 2
    y = value
    if value > 0:  # 只有当值大于0时才显示标签
        ax.text(x, y, percentage, ha='center', va='bottom')
plt.show()
# %%
# category = p.get_x() + p.get_width() / 2.0
# category_name = [t.get_text() for t in ax.get_xticklabels()][int(category)]
# percentage = 100 * height / total
# percentage
category_counts.iloc[int(category)]
category_counts.iloc[int(category)]

# %%
def plot_class_distribution(data, category_variable, order=None):
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x=category_variable, hue='class', data=data, order=order)
    plt.title(f"{category_variable} Distribution with Class Proportions")
    plt.xlabel(category_variable)
    plt.ylabel('Frequency')
    plt.legend(title='Class')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.show()

# Example usage
order = credit_g['purpose'].value_counts().index
plot_class_distribution(credit_g, 'purpose', order = order)
# %%
order = credit_g['credit_history'].value_counts().index
plot_class_distribution(credit_g, 'credit_history', order = order)
# %%

order = credit_g['personal_status'].value_counts().index
plot_class_distribution(credit_g, 'personal_status', order = order)

# %%
# 创建列联表
ct = pd.crosstab(credit_g['class'], credit_g['checking_status'])

# 创建热力图
plt.figure(figsize=(10, 8))
sns.heatmap(ct, annot=True, cmap='coolwarm', fmt='d')
plt.title('Heatmap of Variable1 vs Variable2')
plt.xlabel('Variable2')
plt.ylabel('Variable1')
plt.show()

# %%
credit_g.select_dtypes(include=['object', 'category']).columns
# %%
len(credit_g.columns)
# %%
credit_g.columns
# %%
test = credit_g.drop_duplicates()
# %%
len(test)
# %%

## 資料異常值確認
purpose_check = credit_g[credit_g['purpose'].isin(['new car', 'used car'])]
purpose_check[['purpose', 'property_magnitude']].groupby('property_magnitude').count().reset_index()
# %%
purpose_credit_amount = credit_g[['purpose', 'credit_amount']].groupby('purpose').mean().reset_index().sort_values('credit_amount', ascending = False).reset_index(drop = True)
purpose_credit_amount
# %%
credit_g[['purpose', 'credit_amount']].groupby('purpose').agg({'credit_amount': 'median'}).reset_index().sort_values('credit_amount', ascending = False).reset_index(drop = True)
# %%
credit_g[['purpose', 'duration', 'credit_amount']].groupby('purpose').agg({'credit_amount': 'median', 'duration': 'median'}).reset_index().sort_values('credit_amount', ascending = False).reset_index(drop = True)
# %%
