import os
import time

from data_collector import collect, collect_predict, collect_training, combine_classifications, get_password, \
    training_to_df, transform_data
from data_generator import generate_synthetic_data
from get_user import curr_account, new_account
import pandas as pd

from model import initialize_model, make_prediction


def main():

    hasAccount = input("Do you have an account? (Enter Y/N) ").upper()
    while hasAccount != "Y" and hasAccount != "N":
        hasAccount = input("Please enter Y or N").upper()
    if hasAccount == "Y":
        userName = input("Enter Username: ")
        userName += ".csv"
        if not os.path.exists(userName):
            userNameNew = curr_account()

        else:
            df = pd.read_csv(userName)
            rf_model = initialize_model(df)

            print("Enter Password: ")
            # Collects and transforms the data to predict a classification of
            predict_transformed = collect_predict()
            try:
                prediction = make_prediction(rf_model, predict_transformed)
                print("Prediction: ", prediction)
                print("1: True User")
                print("0: Incorrect User")
            except:
                print(ValueError, "Incorrect Password")


    else:
        userNameNew = new_account()
        print("Choose a password. Press shift to submit it.")
        time.sleep(1)
        password = get_password(collect(1))
        time.sleep(1)
        print("Password: ", password)

        print("Re-Enter your password: ")
        training_data_true = collect_training(1)
        print("Re-type your password irregularly: ")
        training_data_false = collect_training(0)

        training_data_transformed_false = transform_data(training_data_false)
        df1 = generate_synthetic_data(password, training_data_transformed_false)

        training_data_transformed_true = transform_data(training_data_true)
        df2 = generate_synthetic_data(password, training_data_transformed_true)

        combined_df = pd.concat([df1, df2], ignore_index=True)
        # Get equal number of each class
        class_0 = combined_df[combined_df['target'] == 0]
        class_1 = combined_df[combined_df['target'] == 1]

        # Take min count to balance
        min_count = min(len(class_0), len(class_1))

        # Sample equally from both classes
        balanced_df = pd.concat([
            class_0.sample(min_count, random_state=42),
            class_1.sample(min_count, random_state=42)
        ], ignore_index=True)

        # Shuffle the final dataset
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        # training_data = combine_classifications(training_data_transformed_false, training_data_transformed_true)
        # print("FINAL TRAINING: ", training_data)
        # generate_synthetic_data(password, training_data)
        #df = training_to_df(training_data, password)

        balanced_df.to_csv(userNameNew, index=False)





main()