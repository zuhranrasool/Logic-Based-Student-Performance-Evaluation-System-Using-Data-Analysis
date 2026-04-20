# core/logic_rules.py

def apply_dld_logic(df):
    """
    Logic-Based Evaluation System.
    This function maps directly to the logic gates in your project.
    """
    
    def classify(row):
        # DLD Summer Circuit (Adding all inputs)
        total = row["Attendance"] + row["Quiz"] + row["Mid"] + row["Final"]

        # DLD Threshold Logic (Comparators)
        if total < 50:
            return "Fail"
        elif 50 <= total <= 55:
            return "At Risk"
        else:
            return "Safe"

    # Apply the logic to the entire table
    df['Category'] = df.apply(classify, axis=1)
    
    return df