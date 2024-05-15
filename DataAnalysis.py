
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.sandbox.stats.multicomp import multipletests
from scipy.stats import ttest_ind
import  numpy as  np
import os
import matplotlib.pyplot as plt
import matplotlib

import pandas as pd
pd.set_option('display.max_columns', None)


# In this file we are collecting all the data  from the participant folder, read  it in, crop it  to the first  10
# Then, for  each participant we perform a two-way ANOVA to determine whether the speed and FES changed much

def get_participant_data(name, get_first_10 = True):
        data_folder =  f'{os.curdir}/Data/{name}'
        all_trials = []

        for filename in os.listdir(data_folder):
            f = os.path.join(data_folder, filename)
            if os.path.isfile(f):
                with open(f, 'r') as participant_trial:
                    trials = participant_trial.readlines()
                    trials = textToList(trials)
                    if get_first_10:
                        trials = trials[:10]
                    name, speed, fes = get_variables(filename)
                    all_trials.append((name, speed,  fes, trials))
        return all_trials



def get_variables(filename):

    if "FES" in filename:
        FES = "FES"
    else:
        FES = "Control"

    if "Fast" in filename:
        Speed  = "Fast"
    else:
        Speed = "Slow"

    Name = filename.replace(FES, '').replace(Speed, '')
    return Name, Speed, FES

def textToList(line_list):
    times = []
    for line in line_list:
        time = line.split(":")[-1]
        time = time.split("s")[0]
        time = float(time)
        times.append(round(time, 2))
    return times


def plot_all_trials(data, name):
    cmap  =  plt.get_cmap('inferno', 4)
    hex_codes = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
    plt.figure()
    for condition in data:
        if condition[2] == "FES" and condition[1] == "Fast": col = hex_codes[0]
        elif condition[2] == "FES" and condition[1] != "Fast": col = hex_codes[1]
        elif condition[2] != "FES" and condition[1] == "Fast": col = hex_codes[2]
        else:  col = hex_codes[3]
        plt.title(condition[0])
        plt.xlabel("time, s")
        plt.hist(condition[3], bins =  range(0, int(max(condition[3])) + 1), color=col,  label = condition[1] + condition[2])
        plt.legend()
    plt.savefig(name)


def plot_keyword(data, name, keyword, index):
    new_data  =  [x for x in data if x[index]==keyword]
    plot_all_trials(new_data, name)


def plot_all(name):
    plot_all_trials(participant_data_list, f"Data/Plots/{name}")
    plot_keyword(participant_data_list, f"Data/Plots/{name}_Slow", "Slow", 1)
    plot_keyword(participant_data_list, f"Data/Plots/{name}_Fast", "Fast", 1)
    plot_keyword(participant_data_list, f"Data/Plots/{name}_FES", "FES", 2)
    plot_keyword(participant_data_list, f"Data/Plots/{name}_Control", "Control", 2)



if __name__ == '__main__':
    print(np.mean([2, 1, 3, 2]))
    anovas =[]
    for name in ["Amir", "Elizaveta", "Oscar", "Nic"]:
        participant_data_list = get_participant_data(name)
        plot_all(name)


        df_data = {"Speed": [participant_data_list[0][1]]*10 + [participant_data_list[1][1]]*10 + [participant_data_list[2][1]]*10 + [participant_data_list[3][1]]*10,
                   "Stimulation": [participant_data_list[0][2]] * 10 + [participant_data_list[1][2]]*10 + [participant_data_list[2][
                       2]] * 10 + [participant_data_list[3][2]
                                   ]*10,

                   "Reaction_time": participant_data_list[0][3]+participant_data_list[1][3]+participant_data_list[2][3]+participant_data_list[3][3]
                   }

        # Two-way ANOVA


        df_data  = pd.DataFrame(df_data)
        df_data.to_csv(f"{name}_data.csv")

        model = ols("Reaction_time  ~ C(Speed) + C(Stimulation) + C(Speed):C(Stimulation)", data=df_data).fit()
        anova = sm.stats.anova_lm(model, typ = 2)
        anovas.append(anova)
        print("----------------------------------------")
        print(f"Two-way  ANOVA for {name}: {anova}")
        with open(f"Data/{name}_ANOVA", 'w') as file:
            file.write(str(anova))
        print("----------------------------------------")
        print(df_data)


    for name in ["Elizaveta", "Amir"]:
        data = pd.read_csv(f"{name}_data.csv")
        # Filter data and select column
        fast_control_rt = data[(data['Speed'] == 'Fast') & (data['Stimulation'] == 'Control')][
            'Reaction_time']

        fast_fes_rt = data[(data['Speed'] == 'Fast') & (data['Stimulation'] == 'FES')][
            'Reaction_time']

        t_stat, p_value = ttest_ind(fast_control_rt, fast_fes_rt)
        print(f"{name} -  T-test result for FastControl vs FastFES: t-statistic = {t_stat}, p-value = {p_value}")





