# %%
from scipy.io import arff
import pandas as pd
from bodun_package_file import bodun_package as bodun
# %%
def load_arff_to_dataframe(path):
    # 加載ARFF檔案
    data, meta = arff.loadarff(path)
    
    # 轉換為Pandas DataFrame
    df = pd.DataFrame(data)
    
    # 將byte字串類型的屬性轉換為正常的字串（如果有需要的話）
    str_df = df.select_dtypes([object])
    str_df = str_df.stack().str.decode('utf-8').unstack()
    for column in str_df:
        df[column] = str_df[column]
    
    return df
# %%
# 使用示例
df = load_arff_to_dataframe('data\dataset_31_credit-g.arff')
df.head() # 打印DataFrame的前幾行以檢視數據

# %%
## 儲存原始資料至mysql
bodun.save_data_into_mysql(df, 'credit_g', 'practice', 'replace')

# %%
## 儲存字典檔至mysql
dict_ = pd.read_excel('data\credit_g_dict.xlsx')
bodun.save_data_into_mysql(dict_, 'credit_g_dict', 'practice', 'replace')
# %%
