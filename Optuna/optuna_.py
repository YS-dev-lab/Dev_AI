import os
import optuna
import lightgbm as lgb
import sklearn.datasets
import sklearn.metrics
from sklearn.model_selection import train_test_split
import pandas as pd
from pathlib import Path


# 목적 함수가 추가적인 인자를 가질 수 있음.
# (https://optuna.readthedocs.io/en/stable/faq.html#objective-func-addtional-args)
# 

save_file = Path(__file__).parent.joinpath('breast_cancer_data')
file_path = save_file / 'breast_cancer_data.csv'

if not os.path.exists(file_path):
    
    print(" 데이터셋 없음")
    print("데이터셋 다운로드 시작 . . .")
    x,y = sklearn.datasets.load_breast_cancer(return_X_y=True)
    feature_names = sklearn.datasets.load_breast_cancer().feature_names
    df = pd.DataFrame(x, columns=feature_names)
    df['target'] = y
    save_file = Path(__file__).parent.joinpath('breast_cancer_data')
    os.makedirs(save_file, exist_ok=True)
    df.to_csv(save_file / "breast_cancer_data.csv", index=False)
    print("데이터셋 다운로드 완료.!")

def objective(trial):

    df = pd.read_csv(# kaggle data를 가져옴
                    save_file / "breast_cancer_data.csv"
    )
    x=  df[['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness']]
    y = df['target']
    
    train_x, valid_x,train_y,valid_y = train_test_split(x,y,test_size=0.3,random_state=42)
    dtrain = lgb.Dataset(train_x,label= train_y)
    
    
    # 파라미터 공간 정의 (파라미터공간은 학습 모델이 사용하는 하이퍼파라미터를 지정하는것)
    param = {
        "objective": "binary",
        "metric": "binary_logloss",
        "verbosity": -1,
        "boosting_type" : "gbdt",
        "lambda_l1" : trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2" : trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves" : trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction" : trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction" : trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq" : trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples" : trial.suggest_int("min_child_samples", 5, 100),
    }
    
    import numpy as np
    gbm = lgb.train(param,dtrain) # 모델 학습
    preds = gbm.predict(valid_x) # 모델 예측
    pred_labels = np.rint(preds) # 예측 라벨중 real 값만 가져옴
    accuracy = sklearn.metrics.accuracy_score(valid_y, pred_labels)
    return accuracy

if __name__ =="__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100) # return accuracy 값이 가장 높은 trial을 찾음
    
    print("Best trial:")
    
    # Objective function (study.optimize()로 전달된 함수)에서 반환된 값이 가장 높은 trial을 가져옴.
    trial = study.best_trial
    
    print(f"  Value: {trial.value}")
    
    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")