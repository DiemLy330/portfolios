#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Clean raw data
def data_cleaning():
    df = pd.read_csv('src/transactions.csv', sep=';', index_col=0, header=1, encoding='latin-1')

    # Drop empty rows and columns
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    # Fill empty cells in online_order column
    df.online_order.fillna(method='ffill',inplace=True)

    # Change data type in list_price and standard_cost columns from string to integer
    df.list_price = df.list_price.str.replace(",",'.')
    df.standard_cost = df.standard_cost.str.replace(',','.').str.replace(' ','').str.lstrip('$')
    df.list_price = pd.to_numeric(df['list_price'],errors='coerce')
    df.standard_cost = pd.to_numeric(df['standard_cost'], errors='ignore')

    # Create margin and profit columns
    df['margin'] = (df.list_price - df.standard_cost)/df.list_price*100
    df['profit'] = (df.list_price - df.standard_cost)

    # Create product column indicates brand name, product line and product class
    df['product'] = df['brand'] + ': ' + df['product_line'] + ' (class: ' + df['product_class'] + ')'

    # Change data type of transaction_date to date time type
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df['transaction_month'] = df['transaction_date'].dt.month

    # Drop unnecessary column
    df = df.drop('order_status', axis=1)
    return df

# Identify customers by age range
def age_group(x):
    age_mean = x.groupby(['customer_id']).age.mean()
    start = np.empty([0, 7])
    ranges = [range(0, 20), range(20, 30), range(30, 40), range(40, 50), range(50, 60), range(60, 70), range(70, 80)]
    for age in age_mean:
        feature = np.zeros(7)
        for order, span in enumerate(ranges):
            for i in span:
                if i == age:
                    feature[order] += 1
        result = np.vstack((start, feature))
        start = result
    total = sum(result)
    return total

def main():
    x = data_cleaning()
    x = x[x.brand.isna()==False]

    # Concatenate relevant tables into one
    y = pd.read_csv('src/customer_info.csv', sep=',')
    x = x.merge(y, left_on='customer_id', right_on='customer_id')

    # Plot graph of female customer by age
    cols = ['< 20', '20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69', '70 - 79']
    female = x.where(x.gender == 'Female')
    female = age_group(female)
    plt.barh(cols, female, color='pink')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.title('Female')
    plt.show()

    # Plot graph of female customer by age
    male = x.where(x.gender == 'Male')
    male = age_group(male)
    plt.barh(cols, male, color='blue')
    plt.gca().invert_xaxis()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.title('Male')
    plt.show()

    # x.to_csv(r'/Users/diemly/Documents/Python Projects/src/customer_value.csv',index=False)

if __name__ == "__main__":
    main()
