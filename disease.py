
from gettext import find
import re
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm 
import enum 


### Focus: Using the generator to not store any data in memory from the dataset.
### Using Composition to make single responsibility functions
### Calculate the fitness of people in the dataset based on their MET score without storing any of the read data in memory.


def main():
    try:
        # parse the input file. error check for not-.csv files or other input
        parser = argparse.ArgumentParser(
                        prog='read_generator',
                        description='Reads files too large for ram',
                        epilog='end of program')
        parser.add_argument('input', type =csvname)
        args = parser.parse_args()
        file = args.input
    except argparse.ArgumentTypeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

        # TO TEST AGAINST (file size wise and file typewise)
    # create_huge_file()
    # open_no_generator(file)  # This will take a long time to open

    fit, unfit = generate_fitness_scores_men(file)
    x_fit, y_fit, x_unfit, y_unfit = calculate_mean_std(fit, unfit)
    plot_heights_fit_vs_unfit(x_fit, y_fit, x_unfit, y_unfit, plot_label_men())

    fit, unfit = generate_fitness_scores_women(file)
    x_fit, y_fit, x_unfit, y_unfit = calculate_mean_std(fit, unfit)
    plot_heights_fit_vs_unfit(x_fit, y_fit, x_unfit, y_unfit,plot_label_women())

    df = pd.read_csv(file, sep=';')

    ##### DOESNT WORK AFTER REFACTOR, but it had a bug anyway
    # insert score for fit people in the dataframe
    # df['Fitscore'] = 0
    # df.loc[fit, 'Fitscore'] = 1 # this is a pandas version of map function
    # df.drop(indices_to_drop, inplace=True) # pandas filter out rows 
    # scatterplot the fit men vs unfit men against their respective heights to see if there is a correlation between calories burned and height
    # plt.scatter(df[df['Fitscore'] == 1]['Fitscore'], df[df['Fitscore'] == 1]['height'], color='green', label='Fit', alpha=0.7)  # included a filtering of fitscore by: df[df['Fitscore'] == 1]['Fitscore']
    # plt.scatter(df[df['Fitscore'] == 0]['Fitscore'], df[df['Fitscore'] == 0]['height'], color='red', label='Unfit', alpha=0.7)
    # plt.xlabel("Fit")
    # plt.ylabel("Height in cm")
    # plt.title("Fit vs unfit people")
    # plt.legend()
    # plt.grid()
    # plt.show()

    # scatterplot the age vs height
    df['age_years'] = (df['age'] / 365).round()
    plt.scatter(df['age_years'],df['height'],color='skyblue')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

    # plot the distribution of height using a normal distribution (showing mean height and std deviation of population))
    std = df['height'].std()
    mean = df['height'].mean()
    x = np.linspace(mean -std, mean+std)
    y = norm.pdf(x, mean, std)
    plt.title("mean height for the population")
    plt.plot(x,y)
    plt.show()

    
    # compare the mean and std of height for each age-group
    age_height_compare = df.groupby('age_years')['height'].agg('mean','std').reset_index()
    print(age_height_compare)
  
    # try to map. (couldnt fin use for it in this program, since using a generator, but it works)
    res = mapping([1,2,3,4,5,6,7,8,9,10]) # convert list of any to list of float
    # print(list(res))
    
    # filter function testing (coulnt find use for it in this program, since using a generator, but it works)
    res = filtering([1,2,3,4,5,6,7,8,9,10]) # filters list of any to filter out all but 2
    # print(res)

    



# only use men in the dataset
def check_gender_is_men(gender):
    if gender.isdigit() and int(gender) == 2:
        return True
    return False

def check_gender_is_women(gender):
    if gender.isdigit() and int(gender) == 1:
        return True
    return False

# filter out height mistakes in the dataset
def filter_out_height_mistakes(height): # the dataset has some mistakes in the height column like height = 50
    if height.isdigit() and int(height) > 150:
       return height

# calculate the MET score of a person based on their weight, time and calories burned
def calculate_MET(weight, time, calories_burned):
    if weight:
        resting_calories_pr_min = (float(weight) * 0.0175)
        resting_calories_over_time = time * resting_calories_pr_min
        MET = calories_burned / resting_calories_over_time
        return MET
    return None

# make sure that input file is a .csv file
def csvname(inn):
    if not inn.endswith('.csv'):
        raise argparse.ArgumentTypeError("File must be a .csv file")
    return inn


# open file generator
def open_file_generator(file):
    with open(file, "r") as f: # opens and auto closes file
        for line in f:  
            yield line.split(";") # saves loop state and returns to it when called again to save memory

# try mapping function
def mapping(e):
    res = map(int,e)
    return list(res)

# try filter function 
def filtering(e):
    res = filter(lambda x: x==2, e) # filters list of any to filter out all but 2
    return list(res)

# Calculate the mean and std of the fit
def calculate_mean_std(fit, unfit):
    if fit and unfit:
        fit_mapped = mapping(fit)
        mean_fit = np.mean(fit_mapped)
        std_fit = np.std(fit_mapped)
        x_fit = np.linspace(mean_fit - 3*std_fit, mean_fit + 3*std_fit, 100)
        y_fit = norm.pdf(x_fit, mean_fit, std_fit)

        # Calculate the mean and std of the unfit
        unfit_mapped = mapping(unfit)
        mean_unfit = np.mean(unfit_mapped)
        std_unfit = np.std(unfit_mapped)
        x_unfit = np.linspace(mean_unfit - 3*std_unfit, mean_unfit + 3*std_unfit, 100)
        y_unfit = norm.pdf(x_unfit, mean_unfit, std_unfit)
        return x_fit, y_fit, x_unfit, y_unfit

def plot_heights_fit_vs_unfit(x_fit, y_fit, x_unfit, y_unfit, label_gender):
    # plot the heights vs the fit and unfit distributions
        plt.plot(x_fit, y_fit, color='green', label='Fit')
        plt.plot(x_unfit, y_unfit, color='red', label='Unfit ')
        plt.xlabel("Standard deviation of height of fit and unfit males")
        plt.ylabel("Height")
        label_gender
        plt.legend()
        plt.grid()
        plt.show()

def plot_label_men():
    return plt.title("fitness score based on height MEN")

def plot_label_women():
    return plt.title("fitness score based on height WOMEN")
   

### Evaluate fitness of people in the dataset based on their MET score
### when performing a 30 minute exercise that burns 245 calories
def generate_fitness_scores_men(file):
    fit = []
    unfit = []
    for index,x in enumerate(open_file_generator(file)):
        if filter_out_height_mistakes(x[3]):
                # Check for men
                if check_gender_is_men(x[2]):
                    MET = calculate_MET(float(x[4]), time=30,calories_burned=245)
                    if MET and MET <6:
                            fit.append(x[3])
                    else:
                        unfit.append(x[3])
    return fit, unfit   

### Evaluate fitness of people in the dataset based on their MET score
### when performing a 30 minute exercise that burns 245 calories
def generate_fitness_scores_women(file):
    fit = []
    unfit = []
    for index,x in enumerate(open_file_generator(file)):
        if filter_out_height_mistakes(x[3]):
                # Check for women
                if check_gender_is_women(x[2]):
                    MET = calculate_MET(float(x[4]), time=30,calories_burned=245)
                    if MET and MET <6:
                            fit.append(x[3])
                    else:
                        unfit.append(x[3])
    return fit, unfit 

# def create_huge_file():
#     with open("large_file.txt", "w") as f:
#         for i in range(500000000):  # Adjust the number for a larger file
#             f.write(f"This is line {i}\n")



# def open_no_generator(file):
#     lines =[]
#     with open(file, "r") as f:
#         for i in open_file(file):
#             lines+=i
#     return lines

if __name__ == "__main__":
    main()
