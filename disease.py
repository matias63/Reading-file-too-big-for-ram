
import re
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm 
import enum 


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

        # TO TEST AGAINST
    # create_huge_file()
    # open_no_generator(file)  # This will take a long time to open

  

    
    ### Evaluate fitness of people in the dataset based on their MET score
    ### when performing a 30 minute exercise that burns 245 calories
    cholesterol_fit = []
    indices_to_drop = []
    time = 30
    calories_burned = 245
    # counter = 0
    for index,x in enumerate(open_file(file)):
        if filter_out_hright_mistakes(x[3]):
                # Check for men
                check_gender_is_men(x[2])
                MET = calculate_MET(float(x[4]), time=30,calories_burned=245)
                if MET and MET <6:
                        cholesterol_fit.append(index)

    
    # inserr score for fit people in the dataframe
    df = pd.read_csv(file, sep=';')
    df['Fitscore'] = 0
    df.loc[cholesterol_fit, 'Fitscore'] = 1 # this is a pandas version of map function
    df.drop(indices_to_drop, inplace=True) # pandas filter out rows 

    

    # scatterplot the fit men vs unfit men against their respective heights to see if there is a correlation between calories burned and height
    plt.scatter(df[df['Fitscore'] == 1]['Fitscore'], df[df['Fitscore'] == 1]['height'], color='green', label='Fit', alpha=0.7)  # included a filtering of fitscore by: df[df['Fitscore'] == 1]['Fitscore']
    plt.scatter(df[df['Fitscore'] == 0]['Fitscore'], df[df['Fitscore'] == 0]['height'], color='red', label='Unfit', alpha=0.7)
    plt.xlabel("Fit")
    plt.ylabel("Height in cm")
    plt.title("Fit vs unfit people")

    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()

    plt.grid()
    plt.show()


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
    plt.plot(x,y)
    plt.show()

    
    # compare the mean and std of height for each age-group
    age_height_compare = df.groupby('age_years')['height'].agg('mean','std').reset_index()
    print(age_height_compare)
   


    # try to map. (couldnt fin use for it in this program, since using a generator, but it works)
    res = mapping([1,2,3,4,5,6,7,8,9,10]) # convert list of any to list of float
    print(list(res))
    
    # filter function testing (coulnt find use for it in this program, since using a generator, but it works)
    res = filtering([1,2,3,4,5,6,7,8,9,10]) # filters list of any to filter out all but 2
    print(res)

def check_gender_is_men(gender):
    if gender.isdigit() and int(gender) == 2:
        return gender
    return None

def filter_out_hright_mistakes(height):
    if height.isdigit() and int(height) > 150:
       return height

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
def open_file(file):
    with open(file, "r") as f: # opens and auto closes file
        for line in f:  
            yield line.split(";") # saves loop state and returns to it when called again to save memory

# try mapping function
def mapping(e):
    res = map(float,e)
    return res

# try filter function 
def filtering(e):
    res = filter(lambda x: x==2, e) # filters list of any to filter out all but 2
    return list(res)



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
