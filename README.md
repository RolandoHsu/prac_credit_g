## 資料源資訊
* 資料來源 : [網址](https://www.openml.org/search?type=data&status=active&id=31)
* 資料簡述 : 依據顧客資料評估顧客風險(class = bad/ good)

## EDA

### NULL 值確認
* 確認所有欄位皆無 Null 值

### 數值型因子summary

|                    | duration | credit_amount | installment_commitment | residence_since | age  | existing_credits | num_dependents |
|:-------------------|---------:|--------------:|-----------------------:|----------------:|-----:|-----------------:|---------------:|
| count              |  1000.00 |      1000.00  |               1000.00  |         1000.00 |1000.0|          1000.00 |        1000.00 |
| mean               |    20.90 |      3271.26  |                  2.97  |            2.85 | 35.55|             1.41 |           1.16 |
| std                |    12.06 |      2822.74  |                  1.12  |            1.10 | 11.38|             0.58 |           0.36 |
| min                |     4.00 |       250.00  |                  1.00  |            1.00 | 19.00|             1.00 |           1.00 |
| 25%                |    12.00 |      1365.50  |                  2.00  |            2.00 | 27.00|             1.00 |           1.00 |
| 50%                |    18.00 |      2319.50  |                  3.00  |            3.00 | 33.00|             1.00 |           1.00 |
| 75%                |    24.00 |      3972.25  |                  4.00  |            4.00 | 42.00|             2.00 |           1.00 |
| max                |    72.00 |     18424.00  |                  4.00  |            4.00 | 75.00|             4.00 |           2.00 |


### 資料確認- 單因子概況確認
##### 數值型變數(數量: 7)
###### 因子探討
* duration : 存續期間(月份)，可能是貸款月份或剩餘多少月份
  * 由資料可以看出特定月份有較高的頻次，判斷應是銀行貸款給顧客時，會設定特定幾個期間(EX: 貸款3年、5年、7年等完整年份。)
  * 與class同步分析
    * bad 的duration中位數較高(24; good為18)
* credit_amount : 貸款額度/ 信用額度..等
  * 資料分佈右偏，符合預期樣態。
  * 需確認建模時是否要排除離群值。
  * 與class同步分析
    * **猜測**若額度越高，判斷應是質較好的顧客，因此bad的可能性可能越低。--> bad中位數較高，判斷應是指貸款額度，而非如信用卡額度。
* installment_commitment : 分期付款率 佔可支配所得的比率
  * 僅有1~4%的整數值，判斷應是銀行在設定分期付款率時，會依照其他風險因子給予顧客分期付款利率
  * 與class同步分析
    * **猜測**若此因子越高，則bad的可能性越高。 --> bad中位數=4 (good為3)
* resience_since : 現居住地自X年起。(不太確定定義是什麼)
  * 僅有1~4四種數值，分佈上2、4較多，1、3較少。
* age : 年齡
  * 年齡層分佈較為年輕，40歲以下顧客佔比為70.1%
  * 與class同步分析
    * bad 中位數較低(31; good為34)，代表年輕人為風險戶的可能性較高 
* existing_credits : 在此家銀行現有的信用數目 
  * 僅有1~4四個數值，其中持有1項信用產品的為63.3%，2項信用產品的為33.3%。
* num_dependents : 需要扶養的人數
  * 僅有1或2個人，其中需撫養1人的佔84.5%
  * 與class同步分析
    * **猜測**扶養兩人以上的顧客bad的可能性越高 --> 沒看到此現象。

###### 與class變數之T檢定結果(p-value 0.05)

| col_name                | T-statistic    | P-value         | 檢定結果                                 |
|-------------------------|----------------|-----------------|------------------------------------------|
| duration                | -6.952         | 6.49e-12        | 因子平均值存在顯著差異       |
| credit_amount           | -4.948         | 8.80e-07        | 因子平均值存在顯著差異 |
| installment_commitment | -2.293         | 0.0220          | 因子平均值存在顯著差異 |
| residence_since         | -0.094         | 0.925           | **沒有足夠的證據證明兩類別之residence_since 平均值存在顯著差異** |
| age                     | 2.891          | 0.00393         | 因子平均值存在顯著差異           |
| existing_credits        | 1.446          | 0.148           | **沒有足夠的證據證明兩類別之existing_credits 平均值存在顯著差異** |
| num_dependents          | 0.095          | 0.924           | **沒有足夠的證據證明兩類別之num_dependents 平均值存在顯著差異** |

###### 相關係數探討
僅credit_amount 與 duration 具高度相關(62%)，若貸款金額越高，則需要較長的借貸期間，評估合理。

|                         | duration | credit_amount | installment_commitment | residence_since | age     | existing_credits | num_dependents |
|-------------------------|----------|---------------|------------------------|-----------------|---------|------------------|----------------|
| **duration**            | 1.000    | 0.625         | 0.075                  | 0.034           | -0.036  | -0.011           | -0.024         |
| **credit_amount**       | 0.625    | 1.000         | -0.271                 | 0.029           | 0.033   | 0.021            | 0.017          |
| **installment_commitment** | 0.075    | -0.271        | 1.000                  | 0.049           | 0.058   | 0.022            | -0.071         |
| **residence_since**     | 0.034    | 0.029         | 0.049                  | 1.000           | 0.266   | 0.090            | 0.043          |
| **age**                 | -0.036   | 0.033         | 0.058                  | 0.266           | 1.000   | 0.149            | 0.118          |
| **existing_credits**    | -0.011   | 0.021         | 0.022                  | 0.090           | 0.149   | 1.000            | 0.110          |
| **num_dependents**      | -0.024   | 0.017         | -0.071                 | 0.043           | 0.118   | 0.110            | 1.000          |

###### 離群值探討

| 評估指標                 | 離群值下界   | 離群值上界   | 離群值樣本數 |
|----------------------|----------|----------|---------|
| duration            | -6.0     | 42.0     | 70      |
| credit_amount       | -2544.6  | 7882.4   | 72      |
| installment_commitment | -1.0     | 7.0      | 0       |
| residence_since     | -1.0     | 7.0      | 0       |
| age                 | 4.5      | 64.5     | 23      |
| existing_credits    | -0.5     | 3.5      | 6       |
| num_dependents      | 1.0      | 1.0      | 155     |


##### 類別型變數(數量: 14)
###### 因子探討
* class : 目標變數(bad/good)
  * bad : good = 30% : 70% 
* checking_status : 現有支票帳戶的狀態，以德國馬克計算。
  * 以no_checking的人最多(39.4%)，但沒有很顯著的分佈差異。
* credit_history : 信用歷史
  * 共有五個類別
  
  | 原文                            | 繁體中文           |
  |--------------------------------|-------------------|
  | critical/other existing credit | 風險帳戶 |
  | existing paid                  | 已還款    |
  | delayed previously             | 延遲          |
  | no credits/all paid            | 無信貸/全部支付   |
  | all paid                       | 全部支付          |

  *  no credits/all paid(4%)、all paid(4.9%) 單看定義有點接近，將細部去看跟class的關係，決定是否合併。
    * 篩選no credits/all paid、all paid兩種類別，計算bad/good佔比差異後，依卡方檢定結果，兩客群的class分布無顯著差異(p-value= 0.768)，且依描述，no credits/all paid與all paid可能都是all paid，因此將兩種客群整合為normal顧客。
      
    | credit_history | bad | good |
    |----------------|-----|------|
    | no credits/all paid|  25 |   15 |
    | all paid       |  28 |   21 |

* purpose : 貸款目的
  * 以radio/tv(28%)、new car(23.4%)、furniture/equipment(18.1%) 為最大宗。
* savings_status : 儲蓄帳戶/債券的狀態(馬克)
  * <100 的佔比為60.3%。
* employment : 工作年數
* personal_status : 個人狀態(婚姻狀況、性別...等)
  * 底下為原資料表呈現的四種分類，以婚姻狀況來說，女性無區分，男性又將已婚/鰥夫放在一起，資料定義較為混亂。
    * **調整**將擷取female/male，作為sex變數，婚姻狀態則放棄不取用。

  | 值                   | 中文說明             |
  |----------------------|----------------------|
  | male single          | 男性 單身            |
  | female div/dep/mar   | 女性 離婚/分居/已婚  |
  | male div/sep         | 男性 離婚/分居       |
  | male mar/wid         | 男性 已婚/鰥夫       |

* sex : 性別
  * 男 : 女 = 69 : 31
 
* other_parties : 其他債務人/保證人
  * 共有三種值，分別為 none(90.7%)/ guarantor(保證人 5.2%)/ co applicant(共同申請人 4.1%)
  * 超過90%集中在none，可考慮排除此變數不使用。(需確認與class的關係)

* property_magnitude : 其他資產持有狀態
  * 持有車、不動產、壽險或未知是否持有其他資產
  * 可與purpose比較，確認資料是否正確 --> purpose = new car/ used car 但沒有car
    * purpose 為new car / used car的顧客但沒有實體資產car，代表幾種可能
      * purpose 可能失準(EX: 顧客亂填)
      * property_magnitude 可能失準(EX: 僅標示一種資產or 無法查證)，但因其他資產持有狀態可能是查詢顧客繳稅等資訊，想像上失準的可能性較低。
      * 可能因時間差，導致如下結果(EX: 顧客貸款買車，但可能因意外導致車子損壞，或車子是為了家人購買..等)

    | property_magnitude   | num |
    |----------------------|---------|
    | car                  | 110     |
    | life insurance       | 72      |
    | no known property    | 70      |
    | real estate          | 85      |
    ||(上表客群為purpose 為new car / used car)|


* other_payment_plans : 其他分期付款計劃（銀行、商店）
  * 分為 none(81.4%)、bank(13.9%)、stores(4.7%)
  * **猜測**不確定bank、stores是否需要付利息，假設需要，預想會做此種交易代表現金可能不足，bad機會較高?
  * 可以確認bank+stores是否有較多的bad

* housing : 房屋持有狀態(自有/租賃..)
  * own(71.3%)、rent(17.9%)、for free(10.8%)
* job : 工作

| 值                            | 中文說明                     | 佔比   |
|-------------------------------|------------------------------|-------|
| skilled                       | 技術熟練工                   | 63%   |
| unskilled resident            | 未熟練工（本地居民）         | 20%   |
| high qualif/self emp/mgmt     | 高資質/自僱/管理職           | 14.8% |
| unemp/unskilled non res       | 失業/未熟練工（非本地居民）   | 2.2%  |

* own_telephone : yes/no
  * 不太確定此欄位本身定義，yes佔比為40.4%(none: 59.6%)，可再觀察與class交集狀況。
 
* foreign_worker : 外籍工作者(yes/no)
  * yes: 96.3% 近乎全部為外籍。 

###### 與class變數之卡方檢定結果(p-value 0.05)

| col_name             | Chi-squared | P-value   | 檢定結果                  |
|----------------------|-------------|-----------|--------------------------|
| checking_status      | 123.721     | 1.22e-26  | 兩變數存在顯著關聯        |
| credit_history       | 61.691      | 1.28e-12  | 兩變數存在顯著關聯        |
| purpose              | 33.356      | 1.16e-04  | 兩變數存在顯著關聯        |
| savings_status       | 36.099      | 2.76e-07  | 兩變數存在顯著關聯        |
| employment           | 18.368      | 0.00105   | 兩變數存在顯著關聯        |
| personal_status      | 9.605       | 0.0222    | 兩變數存在顯著關聯        |
| other_parties        | 6.645       | 0.0361    | 兩變數存在顯著關聯        |
| property_magnitude   | 23.720      | 2.86e-05  | 兩變數存在顯著關聯        |
| other_payment_plans  | 12.839      | 0.00163   | 兩變數存在顯著關聯        |
| housing              | 18.200      | 1.12e-04  | 兩變數存在顯著關聯        |
| job                  | 1.885       | 0.597     | 沒有足夠的證據證明兩變數存在顯著關聯 |
| own_telephone        | 1.173       | 0.279     | 沒有足夠的證據證明兩變數存在顯著關聯 |
| foreign_worker       | 5.822       | 0.0158    | 兩變數存在顯著關聯        |
| age_adj              | 22.989      | 0.0177    | 兩變數存在顯著關聯        |
| sex                  | 5.349       | 0.0207    | 兩變數存在顯著關聯        |

## 建模資料調整
#### 應變數:
* class : bad/ good

#### 自變數
resience_since : 不確定因子定義，且與class 進行T檢定後沒有足夠的證據證明class兩類別因子平均值存在顯著差異，因此排除此因子。















