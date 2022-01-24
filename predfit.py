import os
from autogluon.tabular import TabularPredictor
import pandas as pd
import time

def pred_fit(Lname):
    root = os.getcwd()  # 获取当前路径
    if Lname =='NBA':
        path = root + '\\' + 'NBAdata' + '.xlsx'
    elif Lname == 'CBA':
        path = root + '\\' + 'CBAdata' + '.xlsx'
    elif Lname == 'FOOTBOLL':
        path = root + '\\' + 'Fdata' + '.xlsx'

    train_data_all = pd.read_excel(path)
    train_data_all.fillna(0)
    # subsample_size = 10
    # train_data_all = train_data_all.sample(n=subsample_size,random_state=0)
    # train_data_all.head()

    label_n = ['6', '7', '8', '10']
    label_zk = 9
    label_dx = 11
    for i in label_n:
        train_data_all = train_data_all.drop(columns=int(i))
    print(train_data_all)

    train_data = []
    test_data = []
    train_data = pd.DataFrame(train_data_all)
    test_data = pd.DataFrame(train_data_all)
    print(train_data)


    test_data.drop(index=(test_data.loc[(test_data[5] == "完")].index), inplace=True)
    print(test_data)
    train_data.drop(index=(train_data.loc[(train_data[5] != "完")].index), inplace=True)
    print(train_data)

    if Lname == 'NBA':
        time_now = time.strftime("%Y-%m-%d 18:00", time.localtime())
        if (time.strftime("%Y-%m-%d %H:%M", time.localtime()) > time_now):
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M")))
        else:
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M"))) - 86400
        yesterday = now - 86400
        time_yesterday = time.strftime("%Y-%m-%d 18:00", time.localtime(yesterday))
    elif Lname == 'CBA':
        time_now = time.strftime("%Y-%m-%d 23:59", time.localtime())
        if (time.strftime("%Y-%m-%d %H:%M", time.localtime()) > time_now):
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M")))
        else:
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M"))) - 86400
        yesterday = now - 86400
        time_yesterday = time.strftime("%Y-%m-%d 23:59", time.localtime(yesterday))
    elif Lname == 'FOOTBOLL':
        time_now = time.strftime("%Y-%m-%d 12:00", time.localtime())
        if (time.strftime("%Y-%m-%d %H:%M", time.localtime()) > time_now):
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M")))
        else:
            now = int(time.mktime(time.strptime(str(time_now), "%Y-%m-%d %H:%M"))) - 86400
        yesterday = now - 86400
        time_yesterday = time.strftime("%Y-%m-%d 12:00", time.localtime(yesterday))

    yesterday_week = int(time.localtime(yesterday)[7] / 7) + 1
    yesterday_month = (int)(str(time_yesterday)[5:7])
    week = int(time.localtime(now)[7] / 7) + 1
    month = (int)(str(time_now)[5:7])

    train_data['day'] = train_data.apply(lambda x: (int)((time.mktime(
        time.strptime(str(x[1]), "%Y-%m-%d %H:%M")) - time.mktime(
        time.strptime(str(time_now), "%Y-%m-%d %H:%M"))) / 86400), axis=1)

    train_data['week'] = train_data.apply(lambda x: int(time.localtime(int(time.mktime(time.strptime(str(x[1]), "%Y-%m-%d %H:%M"))))[7]/7)+1, axis=1)
    train_data['month'] = train_data.apply(lambda x: (int)(str(x[1])[5:7]), axis=1)
    print(train_data)

    train_data_d = train_data.copy()
    train_data_d = train_data_d.loc[train_data_d['day'] == -1].copy()

    train_data_3d = train_data.copy()
    train_data_3d = train_data_3d.loc[train_data_3d['day'] >= -3].copy()
    train_data_3d.drop(index=(train_data_3d.loc[(train_data_3d['day'] >= 0)].index), inplace=True)

    train_data_w = train_data.loc[train_data['week'] == (week - 1)].copy()

    train_data_m = train_data.loc[train_data['month'] == month].copy()

    train_data_a = train_data.copy()
    train_data_a.drop(index=(train_data_a.loc[(train_data_a['day'] >= 0)].index), inplace=True)

    train_data = train_data.drop(columns='day')
    train_data = train_data.drop(columns='week')
    train_data = train_data.drop(columns='month')
    train_data_zk = train_data.drop(columns=[label_dx])
    train_data_dx = train_data.drop(columns=[label_zk])

    if Lname == 'NBA':
        save_path_zk_D = ['agModels-predictClassNBAzk_D','agModels-predictClassNBAdx_D']
        save_path_zk_3D = ['agModels-predictClassNBAzk_3D', 'agModels-predictClassNBAdx_3D']
        save_path_zk_W = ['agModels-predictClassNBAzk_W','agModels-predictClassNBAdx_W']
        save_path_zk_M = ['agModels-predictClassNBAzk_M','agModels-predictClassNBAdx_M']
        save_path_zk_A = ['agModels-predictClassNBAzk_A', 'agModels-predictClassNBAdx_A']
    elif Lname == 'CBA':
        save_path_zk_D = ['agModels-predictClassCBAzk_D','agModels-predictClassCBAdx_D']
        save_path_zk_3D = ['agModels-predictClassCBAzk_3D', 'agModels-predictClassCBAdx_3D']
        save_path_zk_W = ['agModels-predictClassCBAzk_W','agModels-predictClassCBAdx_W']
        save_path_zk_M = ['agModels-predictClassCBAzk_M','agModels-predictClassCBAdx_M']
        save_path_zk_A = ['agModels-predictClassCBAzk_A', 'agModels-predictClassCBAdx_A']
    elif Lname == 'FOOTBOLL':
        save_path_zk_D = ['agModels-predictClassFzk_D', 'agModels-predictClassFdx_D']
        save_path_zk_3D = ['agModels-predictClassFzk_3D', 'agModels-predictClassFdx_3D']
        save_path_zk_W = ['agModels-predictClassFzk_W', 'agModels-predictClassFdx_W']
        save_path_zk_M = ['agModels-predictClassFzk_M', 'agModels-predictClassFdx_M']
        save_path_zk_A = ['agModels-predictClassFzk_A', 'agModels-predictClassFdx_A']

    save_path_list = [save_path_zk_D, save_path_zk_3D, save_path_zk_W,save_path_zk_M,save_path_zk_A]

    train_data_list = [train_data_d, train_data_3d, train_data_w, train_data_m, train_data_a]

    for i in range(len(save_path_list)):
        same = 0
        train_data_l = []
        train_data_l = pd.DataFrame()
        train_data_l = train_data_list[i].copy()
        if(len(train_data_l)==0):
            continue
        print(train_data_l)

        train_data_l = train_data_l.drop(columns='day')
        train_data_l = train_data_l.drop(columns='week')
        train_data_l = train_data_l.drop(columns='month')
        train_data_zk_l = train_data_l.drop(columns=[label_dx])
        train_data_dx_l = train_data_l.drop(columns=[label_zk])

        save_path_zk = save_path_list[i][0]
        save_path_dx = save_path_list[i][1]
        print(save_path_zk)
        print(save_path_dx)
        # if i == 2:
        #     if yesterday_week == week:
        #         print('same')
        #         same = 0
        #     else:
        #         same =1
        # if i == 3:
        #     if yesterday_month == month:
        #         print('same')
        #         same = 0
        #     else:
        #         same =1
        #
        # if same == 0:
        #     predictor_zk = TabularPredictor(label=label_zk, path=save_path_zk).fit(train_data_zk_l, time_limit=60, presets='best_quality')
        #     predictor_dx = TabularPredictor(label=label_dx, path=save_path_dx).fit(train_data_dx_l, time_limit=60, presets='best_quality')
        # else:
        #     print('same')
        predictor_zk = TabularPredictor(label=label_zk, path=save_path_zk, problem_type='multiclass').fit(
            train_data_zk_l, time_limit=60, presets='best_quality')#
        predictor_dx = TabularPredictor(label=label_dx, path=save_path_dx, problem_type='multiclass').fit(
            train_data_dx_l, time_limit=60, presets='best_quality')

        predictor = TabularPredictor.load(save_path_zk)
        y_pred_zk = predictor.predict(train_data_zk)
        # print(y_pred_zk)
        y_test_zk = train_data[label_zk]
        pref_zk = predictor.evaluate_predictions(y_true=y_test_zk, y_pred=y_pred_zk, auxiliary_metrics=True)
        print(save_path_zk)
        print(pref_zk)
        predictor = TabularPredictor.load(save_path_dx)
        y_pred_dx = predictor.predict(train_data_dx)
        # print(y_pred_dx)
        y_test_dx = train_data[label_dx]
        pref_dx = predictor.evaluate_predictions(y_true=y_test_dx, y_pred=y_pred_dx, auxiliary_metrics=True)
        print(save_path_dx)
        print(pref_dx)
    return


# if __name__ == '__main__':
#     time_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#
#     pred_fit('FOOTBOLL')
#     pred_fit('NBA')
#     pred_fit('CBA')
#     time_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     print(time_start)
#     print(time_end)
