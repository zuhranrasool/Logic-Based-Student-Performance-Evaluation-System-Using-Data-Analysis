
from core.data_loader import load_data
from core.data_processing import process_data

df = load_data("dataset/student_data.csv")

if df is not None:
    df = process_data(df)
    print(df)
    df.to_csv("output/categorized_students.csv", index=False)
    print("Categorized file saved in output folder!")