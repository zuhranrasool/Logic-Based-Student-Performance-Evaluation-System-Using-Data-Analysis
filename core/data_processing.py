# core/data_processing.py

def calculate_totals(df):
    """
    DLD Mapping: This acts as a Summer Circuit.
    It adds Attendance, Quiz, Mid, and Final marks to create a Total.
    """
    # Ensure all columns are treated as numbers
    df['Total'] = df['Attendance'] + df['Quiz'] + df['Mid'] + df['Final']
    return df