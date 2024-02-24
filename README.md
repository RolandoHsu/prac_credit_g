## 資料源資訊
* 資料來源 : [網址](https://www.openml.org/search?type=data&status=active&id=31)
* 資料簡述 : 依據顧客資料評估顧客風險(class = bad/ good)

## ETL

### NULL 值確認
* 確認所有欄位皆無 Null 值

### 資料確認- 單因子概況確認
##### 數值型變數(數量: 7)
* duration : 存續期間(月份)，可能是貸款月份或剩餘多少月份
  * 由資料可以看出特定月份有較高的頻次，判斷應是銀行貸款給顧客時，會設定特定幾個期間(EX: 貸款3年、5年、7年等完整年份。)
* credit_amount : 貸款額度/ 信用額度..等
  * 資料分佈右偏，符合預期樣態。
  * 需確認建模時是否要排除離群值。
  * **猜測**若額度越高，判斷應是質較好的顧客，因此bad的可能性可能越低。
* installment_commitment : 分期付款率 佔可支配所得的比率
  * 僅有1~4%的整數值，判斷應是銀行在設定分期付款率時，會依照其他風險因子給予顧客分期付款利率
  * **猜測**若此因子越高，則bad的可能性越高。
* resience_since : 現居住地自X年起。(不太確定定義是什麼)
  * 僅有1~4四種數值，分佈上2、4較多，1、3較少。
* age : 年齡
  * 年齡層分佈較為年輕，40歲以下顧客佔比為70.1%
* existing_credits : 在此家銀行現有的信用數目 
  * 僅有1~4四個數值，其中持有1項信用產品的為63.3%，2項信用產品的為33.3%。
* num_dependents : 需要扶養的人數
  * 僅有1或2個人，其中需撫養1人的佔84.5%
  * **猜測**扶養兩人以上的顧客bad的可能性越高
##### 類別型變數
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



### 資料確認- 與class交集概況確認

