# %%
from bodun_package_file import bodun_package as bodun
import pandas as pd
import numpy as np
from datetime import datetime

## 切分訓練 測試資料
from sklearn.model_selection import train_test_split

## 建模
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
# %%
############################################## 導入資料源
sql = f""" select * from practice.credit_g_m """
credit_g_m = bodun.pull_data_from_mysql(sql, 'practice')
print('總欄位個數: ', len(credit_g_m.columns))
credit_g_m.head(2)
# %%
############################################## 調整因子，確認效果是否較好
## 原始模型

def create_model(data):

    X = data.drop('class', axis=1)
    y = data['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    rfc = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],  
        'max_depth': [None, 10, 20, 30]
    }
    grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best AUC score:", grid_search.best_score_)
    # 使用最佳參數的模型進行預測
    best_model = grid_search.best_estimator_
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_pred_proba)
    print("Test AUC score:", test_auc)
    feature_importances = best_model.feature_importances_
    features = X_train.columns
    feature_importance_dict = dict(zip(features, feature_importances))

    # 對特徵及其重要性進行排序
    sorted_feature_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 列出貢獻度排序前十的因子
    top_10_features = sorted_feature_importances[:10]
    print('')
    print("Top 10 contributing factors and their importances:")
    for feature, importance in top_10_features:
        print(f"{feature}: {importance}")

# %%
## 原始資料
create_model(credit_g_m)
# %%
## 排除顯著性較低的變數
col_to_drop = ['residence_since', 'existing_credits', 'num_dependents', 'job', 'own_telephone'] 
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('欄位個數: ', len(credit_g_m_2.columns)-1)
create_model(credit_g_m_2)
# %%
## 排除顯著性較低的變數: existing_credits num_dependents job own_telephone	
col_to_drop = ['existing_credits', 'num_dependents', 'job', 'own_telephone'] 
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('欄位個數: ', len(credit_g_m_2.columns)-1)
create_model(credit_g_m_2)

# %%
# 刪除 personal_status, foreign_worker, residence_since, existing_credits, num_dependents, job, own_telephone
col_to_drop = ['personal_status', 'foreign_worker', 'existing_credits', 'num_dependents', 'job', 'own_telephone']
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('欄位個數: ', len(credit_g_m_2.columns)-1)
create_model(credit_g_m_2)


# %%

############################################## 調整模型(皆採用GridSearchCV cv=5 測試)
## 隨機森林
def create_model(data):

    X = data.drop('class', axis=1)
    y = data['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    rfc = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],  
        'max_depth': [None, 10, 20, 30]
    }
    grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best AUC score:", grid_search.best_score_)
    # 使用最佳參數的模型進行預測
    best_model = grid_search.best_estimator_
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_pred_proba)
    print("Test AUC score:", test_auc)
    feature_importances = best_model.feature_importances_
    features = X_train.columns
    feature_importance_dict = dict(zip(features, feature_importances))

    # 對特徵及其重要性進行排序
    sorted_feature_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 列出貢獻度排序前十的因子
    top_10_features = sorted_feature_importances[:10]
    print('')
    print("Top 10 contributing factors and their importances:")
    for feature, importance in top_10_features:
        print(f"{feature}: {importance}")

col_to_drop = ['personal_status', 'foreign_worker', 'existing_credits', 'num_dependents', 'job', 'own_telephone']
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('模型: 隨機森林')
print('欄位個數: ', len(credit_g_m_2.columns)-1)
start = datetime.now()
create_model(credit_g_m_2)
end = datetime.now()
print('執行時間: ', end - start)

# %%
## 決策樹
def create_model(data):

    X = data.drop('class', axis=1)
    y = data['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    dtc = DecisionTreeClassifier(random_state=42)
    param_grid = {
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 10, 20],
        'min_samples_leaf': [1, 5, 10]
    }
    grid_search = GridSearchCV(estimator=dtc, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best AUC score:", grid_search.best_score_)
    # 使用最佳參數的模型進行預測
    best_model = grid_search.best_estimator_
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_pred_proba)
    print("Test AUC score:", test_auc)
    feature_importances = best_model.feature_importances_
    features = X_train.columns
    feature_importance_dict = dict(zip(features, feature_importances))

    # 對特徵及其重要性進行排序
    sorted_feature_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 列出貢獻度排序前十的因子
    top_10_features = sorted_feature_importances[:10]
    print('')
    print("Top 10 contributing factors and their importances:")
    for feature, importance in top_10_features:
        print(f"{feature}: {importance}")

col_to_drop = ['personal_status', 'foreign_worker', 'existing_credits', 'num_dependents', 'job', 'own_telephone']
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('模型: 決策樹')
print('欄位個數: ', len(credit_g_m_2.columns)-1)
start = datetime.now()
create_model(credit_g_m_2)
end = datetime.now()
print('執行時間: ', end - start)

# %%
## XGBOOST
def create_model(data):

    X = data.drop('class', axis=1)
    y = data['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    xgb = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss')
    param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 4, 5],
    'learning_rate': [0.01, 0.05, 0.1]
    }
    grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best AUC score:", grid_search.best_score_)
    # 使用最佳參數的模型進行預測
    best_model = grid_search.best_estimator_
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_pred_proba)
    print("Test AUC score:", test_auc)
    feature_importances = best_model.feature_importances_
    features = X_train.columns
    feature_importance_dict = dict(zip(features, feature_importances))

    # 對特徵及其重要性進行排序
    sorted_feature_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 列出貢獻度排序前十的因子
    top_10_features = sorted_feature_importances[:10]
    print('')
    print("Top 10 contributing factors and their importances:")
    for feature, importance in top_10_features:
        print(f"{feature}: {importance}")

col_to_drop =  ['personal_status', 'foreign_worker', 'existing_credits', 'num_dependents', 'job', 'own_telephone']
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('模型: XGBOOST')
print('欄位個數: ', len(credit_g_m_2.columns)-1)
start = datetime.now()
create_model(credit_g_m_2)
end = datetime.now()
print('執行時間: ', end - start)
# %%
## lightbgm
def create_model(data):

    X = data.drop('class', axis=1)
    y = data['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    lgbm = LGBMClassifier(random_state=42, force_col_wise=True)
    param_grid = {
    'n_estimators': [100, 200, 300, 500, 800],
    'max_depth': [3, 4, 5],  
    'learning_rate': [0.01, 0.05, 0.08, 0.1],
    'num_leaves': [5, 6, 7, 12, 13, 14, 15, 28, 29, 30, 31],  # 根據max_depth調整合適的範圍
    'subsample':[0.8, 0.9, 1.0],
    'colsample_bytree' : [0.8, 0.9, 1.0]
    }
    grid_search = GridSearchCV(estimator=lgbm, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best AUC score:", grid_search.best_score_)
    # 使用最佳參數的模型進行預測
    best_model = grid_search.best_estimator_
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_pred_proba)
    print("Test AUC score:", test_auc)
    feature_importances = best_model.feature_importances_
    features = X_train.columns
    feature_importance_dict = dict(zip(features, feature_importances))

    # 對特徵及其重要性進行排序
    sorted_feature_importances = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 列出貢獻度排序前十的因子
    top_10_features = sorted_feature_importances[:10]
    print('')
    print("Top 10 contributing factors and their importances:")
    for feature, importance in top_10_features:
        print(f"{feature}: {importance}")

col_to_drop = ['personal_status', 'foreign_worker', 'existing_credits', 'num_dependents', 'job', 'own_telephone']
credit_g_m_2 = credit_g_m.drop(columns=col_to_drop)
print('模型: LIGHTGBM')
print('欄位個數: ', len(credit_g_m_2.columns)-1)
start = datetime.now()
create_model(credit_g_m_2)
end = datetime.now()
print('執行時間: ', end - start)


# %%
############################################## 模型測試

clf = DecisionTreeClassifier(random_state=0)
# 使用訓練集訓練模型
clf.fit(X_train, y_train)
# 使用測試集進行預測
y_pred = clf.predict(X_test)
# 計算準確率
accuracy = accuracy_score(y_test, y_pred)
print(classification_report(y_test,y_pred))
print(f'模型準確率: {accuracy:.2f}')

print(confusion_matrix(y_test,y_pred))
# %%
# 計算AUC值
auc_score = roc_auc_score(y_test, y_pred)
print(f"AUC: {auc_score:.2f}")
# %%
# 獲得畫ROC曲線所需的數據
fpr, tpr, thresholds = roc_curve(y_test, y_pred)

# 畫ROC曲線
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auc_score:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
# %%
#n_estimator代表要使用多少CART樹（CART樹為使用GINI算法的決策樹）
rfc = RandomForestClassifier(n_estimators=100, random_state=0)
#從訓練組資料中建立隨機森林模型
rfc.fit(X_train,y_train)
#預測測試組的駝背是否發生
rfc_pred = rfc.predict(X_test)
#利用confusion matrix來看實際及預測的差異
print(confusion_matrix(y_test,rfc_pred))
#利用classification report來看precision、recall、f1-score、support
print(classification_report(y_test,rfc_pred))
auc_score = roc_auc_score(y_test, rfc_pred)
print(f"AUC: {auc_score:.2f}")
# %%
rfc = RandomForestClassifier(n_estimators=100, random_state=0)

# 設定K折交叉驗證的參數，這裡K=5
kf = KFold(n_splits=5, shuffle=True, random_state=0)

# 使用cross_val_score函數進行交叉驗證，這裡以AUC為評分標準
scores = cross_val_score(rfc, X_train, y_train, cv=kf, scoring='roc_auc')

# 輸出每一折的AUC分數以及平均AUC分數
print(f"每一折的AUC分數: {scores}")
print(f"平均AUC分數: {np.mean(scores):.2f}")
# %%

# %%
# 创建随机森林分类器实例
rfc = RandomForestClassifier(random_state=42)
# 定义要搜索的超参数空间
param_grid = {
    'n_estimators': [100, 200, 300],  # 树的数量
    'max_depth': [None, 10, 20, 30],  # 树的最大深度
}
# 创建GridSearchCV对象，使用AUC作为评分标准
grid_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
# 在训练集上执行网格搜索
grid_search.fit(X_train, y_train)
# 打印找到的最佳参数和对应的AUC分数
print("Best parameters:", grid_search.best_params_)
print("Best AUC score:", grid_search.best_score_)
# %%
# 使用最佳参数的模型进行预测
best_model = grid_search.best_estimator_
y_pred_proba = best_model.predict_proba(X_test)[:, 1]  # 获取正类别的概率
# %%
y_pred_proba
# %%
test_auc = roc_auc_score(y_test, y_pred_proba)
print("Test AUC score:", test_auc)
# %%
# 獲得畫ROC曲線所需的數據
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
# 畫ROC曲線
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {test_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
# %%

## 調整因子，確認效果有沒有比較好


## 調整模型
