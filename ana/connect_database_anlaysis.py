import pymysql as ms
import uproot
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

plt.style.use("mystyle.txt")
# Establish connection parameters
host = "localhost"  # Usually 'localhost' for local development
user = "root"
password = "@Min08240707"
database = "test"


def connect_db(sql_query, i):
    # Create a connection object
    result = []
    connection = ms.connect(
        host=host,
        user=user,
        password=password,
        db=database,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor,
    )
    # Create a cursor object
    cursor = connection.cursor()
    # SQL query for SELECT

    print("channel ========================" + str(i))

    try:
        # Execute the SQL command
        cursor.execute(sql_query)
        # Fetch all the rows
        rows = cursor.fetchall()
        # Display the rows
        for row in rows:
            # print(row)
            for key, values in row.items():
                # print(key, values)  # Or perform operations on each row as needed
                result.append(values)
        return result
    except Exception as e:
        print(f"Error: {e}")
    # Close the cursor and connection
    cursor.close()
    connection.close()


# Check if this module is the main module being run
if __name__ == "__main__":
    ROB = 4
    final_result = []
    for i in range(64):
        sql_query = (
            "SELECT Q1 , sigma1 FROM tt_tele_fit_result where ROB = 4 and channel = "
            + str(i)
            + ";"
        )
        Q1 = connect_db(
            sql_query, i
        )  # Call the main function if this script is executed directly
        print(Q1)
        sql_query = (
            "SELECT a1 FROM web_tt_tele_calibration where FEB_ID = 9 and CH = "
            + str(i)
            + ";"
        )
        a1 = connect_db(
            sql_query, i
        )  # Call the main function if this script is executed directly

        a1.extend(Q1)
        # merged_list = a1
        final_result.append(a1)
        df = pd.DataFrame(
            final_result,
            columns=[
                "a1",
                "test1",
                "t1_er",
                "test2",
                "t2_er",
                "test3",
                "t3_er",
                "test4",
                "t4_er",
            ],
        )
    print(df)

    x = np.arange(64)
    print(x)
    ax = plt.axes(
        xlim=[0, 63], ylim=[0, 20], xlabel="Channel", ylabel=r"Q$_{1}$"
    )  # r"$\\frac{{\\chi^2}}{{\\text{{NDF}}}}"
    plt.scatter(
        x, df["a1"] * 0.16, marker="o", label="a1 * 0.16"
    )  # Plotting the histogram
    plt.errorbar(
        x, df["test1"], yerr=df["t1_er"], marker="*", label="test1"
    )  # Plotting the histogram
    plt.errorbar(
        x, df["test1"], yerr=df["t2_er"], marker="^", label="test3"
    )  # Plotting the histogram
    plt.errorbar(
        x, df["test1"], yerr=df["t3_er"], marker="v", label="test5"
    )  # Plotting the histogram
    plt.errorbar(
        x, df["test1"], yerr=df["t4_er"], marker="+", label="test6"
    )  # Plotting the histogram
    plt.title("ROB " + str(ROB))
    plt.legend()
    plt.savefig("Final_Result_test/ROB_" + str(ROB) + "_compare_Q1a1.pdf")
    plt.show()
