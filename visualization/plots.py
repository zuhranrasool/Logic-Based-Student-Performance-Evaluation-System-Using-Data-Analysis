import matplotlib.pyplot as plt
import seaborn as sns

def create_distribution_plot(df):
    fig, ax = plt.subplots()
    sns.countplot(x='Category', data=df, palette='Set2', ax=ax)
    ax.set_title("Student Distribution by Category")
    return fig

def create_scatter_plot(df):
    fig, ax = plt.subplots()
    sns.scatterplot(x='Attendance', y='Final', hue='Category', data=df, ax=ax)
    ax.axvline(7.5, color='r', linestyle='--') # Logic Threshold
    ax.axhline(20, color='r', linestyle='--')  # Logic Threshold
    ax.set_title("Attendance vs Final Marks")
    return fig