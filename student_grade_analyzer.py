import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Student Grade Analyzer")

# Input method selection
input_method = st.radio("Choose input method:", ("Upload CSV", "Manual Input"))

df = None

if input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with columns: Student Name, Math Grade, Science Grade, English Grade", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Strip column names to handle any extra spaces
            df.columns = df.columns.str.strip()
            required_columns = ["Student Name", "Math Grade", "Science Grade", "English Grade"]
            # Check if all required columns are present (case-insensitive)
            df_columns_lower = [col.lower() for col in df.columns]
            required_lower = [col.lower() for col in required_columns]
            if set(required_lower).issubset(set(df_columns_lower)):
                # Rename columns to standard names
                column_mapping = {}
                for req in required_columns:
                    for col in df.columns:
                        if col.lower() == req.lower():
                            column_mapping[col] = req
                            break
                df = df.rename(columns=column_mapping)
            else:
                st.error("The CSV file must contain the following columns: Student Name, Math Grade, Science Grade, English Grade")
                df = None
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            df = None
else:
    st.subheader("Manual Input")
    num_students = st.number_input("Number of students", min_value=1, value=4, step=1)
    data = []
    for i in range(num_students):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name = st.text_input(f"Student {i+1} Name", key=f"name_{i}")
        with col2:
            math = st.number_input(f"Math Grade", min_value=0, max_value=100, value=85, key=f"math_{i}")
        with col3:
            science = st.number_input(f"Science Grade", min_value=0, max_value=100, value=90, key=f"science_{i}")
        with col4:
            english = st.number_input(f"English Grade", min_value=0, max_value=100, value=88, key=f"english_{i}")
        if name:
            data.append([name, math, science, english])
    if data:
        df = pd.DataFrame(data, columns=["Student Name", "Math Grade", "Science Grade", "English Grade"])

if df is not None and not df.empty:
    # Calculate average grades for each student
    df['Average Grade'] = df[['Math Grade', 'Science Grade', 'English Grade']].mean(axis=1)

    # Calculate overall statistics
    overall_average = np.mean(df['Average Grade'])
    overall_std = np.std(df['Average Grade'])

    st.subheader("Grade Data")
    st.dataframe(df)

    st.subheader("Overall Statistics")
    st.write(f"Overall Average Grade: {overall_average:.2f}")
    st.write(f"Overall Standard Deviation: {overall_std:.2f}")

    # Plot the average grades
    st.subheader("Average Grades per Student")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(df['Student Name'], df['Average Grade'], color='skyblue')
    ax1.set_title('Average Grades per Student')
    ax1.set_xlabel('Student Name')
    ax1.set_ylabel('Average Grade')
    ax1.set_ylim(0, 100)
    st.pyplot(fig1)

    # Plot histogram of grades
    st.subheader("Distribution of Average Grades")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.hist(df['Average Grade'], bins=5, color='lightgreen', edgecolor='black')
    ax2.set_title('Distribution of Average Grades')
    ax2.set_xlabel('Average Grade')
    ax2.set_ylabel('Frequency')
    st.pyplot(fig2)
else:
    st.write("Please provide grade data using one of the input methods above.")
