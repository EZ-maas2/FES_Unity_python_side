import statistics

import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import kruskal, wilcoxon

import os
import matplotlib.pyplot as plt

import seaborn as sns

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


def name_encode(name):
    if name == "Amir":
        return "Participant 1"
    elif name == "Elizaveta" or name == "Eliza":

        return "Participant 2"
    elif name == "Oscar":
        return "Participant 3"
    elif name == "Nic":
        return "Participant 4"
    else: return None

def plot_all_trials(data, name):
    #cmap  =  plt.get_cmap('turbo', 4)
    #hex_codes = [matplotlib.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
    plt.figure()
    for condition in data:
        if condition[2] == "FES" and condition[1] == "Fast": col = '#FF0000' #hex_codes[0]
        elif condition[2] == "FES" and condition[1] != "Fast": col = '#FD9D00' #hex_codes[1]
        elif condition[2] != "FES" and condition[1] == "Fast": col = "#B5FA33" #hex_codes[2]
        else:  col = "#32342E" # hex_codes[3]
        plt.title(name_encode(condition[0]))
        plt.xlabel("time, s")
        sns.histplot(condition[3],   label = condition[1] + condition[2], color=col, binwidth=1)  #bins =  range(0, int(max(condition[3])) + 1),
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

def try_z(res):
    try:
            z  = res.zstatistic

    except:
            z =  None
    finally:
        return z


def get_specific_group(data, speed, stim):
    return data[(data['Speed'] == speed) & (data['Stimulation'] == stim)][
        'Reaction_time']


if __name__ == '__main__':
    ANOVA = False
    KRUSKAL = True
    TTEST  = False
    WILCOXON = True
    CreateAllData = False
    names = ["Amir", "Elizaveta", "Oscar", "Nic"]


    for name in names:
        participant_data_list = get_participant_data(name)
        #plot_all(name)


        df_data = {"Speed": [participant_data_list[0][1]]*10 + [participant_data_list[1][1]]*10 + [participant_data_list[2][1]]*10 + [participant_data_list[3][1]]*10,
                   "Stimulation": [participant_data_list[0][2]] * 10 + [participant_data_list[1][2]]*10 + [participant_data_list[2][
                       2]] * 10 + [participant_data_list[3][2]
                                   ]*10,

                   "Reaction_time": participant_data_list[0][3]+participant_data_list[1][3]+participant_data_list[2][3]+participant_data_list[3][3]
                   }




        df_data  = pd.DataFrame(df_data)
        df_data.to_csv(f"{name}_data.csv")

        if KRUSKAL:
            h, p = kruskal(participant_data_list[0][3], participant_data_list[1][3], participant_data_list[2][3], participant_data_list[3][3])
            print(f"For {name}, kruskal-wallis H test shows {h} statistic, p-value  is {p}")


    print("--------------------------------------------------------------------------------")
    if CreateAllData:
        all_data = pd.concat([pd.read_csv("Elizaveta_data.csv"), pd.read_csv("Oscar_data.csv"),
                             pd.read_csv("Amir_data.csv"), pd.read_csv("Nic_data.csv")])

        all_data.sort_values(by = ["Speed", "Stimulation"])
        all_data.to_csv("Data/all_data.csv")

    all_data = pd.read_csv("Data/all_data.csv")
    all_fastFES = get_specific_group(all_data, speed="Fast", stim="FES")
    all_slowFES = get_specific_group(all_data, speed="Slow", stim="FES")
    all_fastControl  = get_specific_group(all_data, speed="Fast", stim="Control")
    all_slowControl  = get_specific_group(all_data, speed="Slow", stim="Control")



    # Do kruskal  on all data
    h, p = kruskal(all_slowControl, all_fastControl, all_slowFES, all_fastFES)
    print(f"For ALL DATA, kruskal-wallis H test shows {h} statistic, p-value  is {p}")
    res = wilcoxon(all_fastControl, all_fastFES)

    print(f"ALL DATA =  Wilcoxon result for FastControl vs FastFES: statistic = {res.statistic}, p-value = {res.pvalue}, "
          f"median  FastControl =  {statistics.median(all_fastControl)}, "
          f"median FastFES = {statistics.median(all_fastFES)}")

    res = wilcoxon(all_slowControl, all_slowFES)
    print(f"ALL DATA = Wilcoxon result for  SlowControl vs SlowFES: statistic = {res.statistic}, p-value = {res.pvalue}"
          f"median SlowControl = {statistics.median(all_slowControl)},"
          f" median SlowFES = {statistics.median(all_slowFES)}")

    res = wilcoxon(all_slowControl, all_fastControl)
    print(
        f"ALL DATA =  Wilcoxon result for  SlowControl vs FastControl: statistic = {res.statistic}, p-value = {res.pvalue}, "
        f"median SlowControl = {statistics.median(all_slowControl)},"
        f" median FastControl = {statistics.median(all_fastControl)}")



    # Plot all data as a boxplot
    plt.figure()
    plt.title("Game-dependent reaction time")
    sns.boxplot(data ={'Slow Control': all_slowControl, 'Slow  FES': all_slowFES, 'Fast Control': all_fastControl, 'Fast FES': all_fastFES}, palette="hot")
    plt.ylabel("Reaction time, s")
    plt.savefig("Data/Plots/all_data")

    print("--------------------------------------------------------------------------------")



# post-hoc  testing for groups that showed significance in ANOVA
    def participantLvlPost(names):
        for name in names:
            data = pd.read_csv(f"{name}_data.csv")
            # Filter data and select column
            fast_control_rt = data[(data['Speed'] == 'Fast') & (data['Stimulation'] == 'Control')][
                'Reaction_time']

            fast_fes_rt = data[(data['Speed'] == 'Fast') & (data['Stimulation'] == 'FES')][
                'Reaction_time']


            slow_control_rt = data[(data['Speed'] == 'Slow') & (data['Stimulation'] == 'Control')][
                'Reaction_time']

            slow_fes_rt = data[(data['Speed'] == 'Slow') & (data['Stimulation'] == 'FES')][
                'Reaction_time']


            if WILCOXON:
                res  = wilcoxon(fast_control_rt, fast_fes_rt)

                print(f"{name} -  Wilcoxon result for FastControl vs FastFES: statistic = {res.statistic}, p-value = {res.pvalue}, "
                      f"median  FastControl =  {statistics.median(fast_control_rt)}, "
                      f"median FastFES = {statistics.median(fast_fes_rt)}")

                res = wilcoxon(slow_control_rt, slow_fes_rt)
                print(f"{name} -  Wilcoxon result for  SlowControl vs SlowFES: statistic = {res.statistic}, p-value = {res.pvalue}"
                      f"median SlowControl = {statistics.median(slow_control_rt)}, median SlowFES = {statistics.median(slow_fes_rt)}")

                res = wilcoxon(slow_control_rt, fast_control_rt)
                print(f"{name} -  Wilcoxon result for  SlowControl vs FastControl: statistic = {res.statistic}, p-value = {res.pvalue}, "
                      f"median SlowControl = {statistics.median(slow_control_rt)}, median FastControl = {statistics.median(fast_control_rt)}")










