import pandas

totalData = pandas.read_csv("data.csv", delimiter="\t", on_bad_lines="skip")

totalData.show()