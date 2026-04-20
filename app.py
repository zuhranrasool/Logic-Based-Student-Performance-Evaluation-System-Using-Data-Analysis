import streamlit as st
import pandas as pd
from core.data_loader import load_csv
from core.data_processing import calculate_totals
from core.logic_rules import apply_dld_logic
from visualization.plots import create_distribution_plot, create_scatter_plot

st.set_page_config(page_title="Student Performance Logic System", layout="wide")
st.title("🧠 Logic-Based Student Performance System")
st.markdown("---")
# --- Project Team Info in Colored Boxes ---
st.markdown(
    """
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <div style="background-color:#4CAF50; color:white; padding:15px; border-radius:8px; flex:1; text-align:center;">
            <b>Project Leader</b><br>Zuhran Rasool
        </div>
        <div style="background-color:#2196F3; color:white; padding:15px; border-radius:8px; flex:1; text-align:center;">
            <b>Team Member</b><br>Yousuf Sarfraz
        </div>
        <div style="background-color:#FF5722; color:white; padding:15px; border-radius:8px; flex:1; text-align:center;">
            <b>Team Member</b><br>Muhammad Rayan
        </div>
    </div>
    """, unsafe_allow_html=True
)
# --- Header Section ---

st.markdown("---")

# --- Data Pipeline ---
df = load_csv('dataset/student_data.csv')

if df is not None:
    # Process Data
    df = calculate_totals(df)
    df = apply_dld_logic(df)

    id_col = next((c for c in df.columns if any(word in c.lower() for word in ['roll', 'no', 'id', 'reg'])), None)

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Search & Filter")
    
    # 1. Search by Name or Roll Number
    search_query = st.sidebar.text_input("Search Student (Name/Roll#):")
    
    # 2. Filter by Subject (if column exists)
    if 'Subject' in df.columns:
        subjects = ["All"] + list(df['Subject'].unique())
        selected_subject = st.sidebar.selectbox("Select Subject:", subjects)
    else:
        selected_subject = "All"

    # --- Apply Filters to Data ---
  # --- 1. Identify Columns ---
    id_col = next((c for c in df.columns if any(word in c.lower() for word in ['roll', 'no', 'id', 'reg'])), None)
    
    # --- 2. Apply Filters (Name/Roll AND Subject) ---
    filtered_df = df.copy()
    
    # Apply Subject Filter First
    if selected_subject != "All":
        filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]
    
    # Apply Search Filter Second
    if search_query:
        name_match = filtered_df['Name'].str.contains(search_query, case=False, na=False)
        if id_col:
            roll_match = filtered_df[id_col].astype(str).str.contains(search_query, na=False)
            filtered_df = filtered_df[name_match | roll_match]
        else:
            filtered_df = filtered_df[name_match]

    # --- 3. Display Logic ---
    if search_query:
        if not filtered_df.empty:
            st.success(f"🔍 Showing {len(filtered_df)} result(s) for '{search_query}' in {selected_subject}")
            
            for i in range(len(filtered_df)):
                student = filtered_df.iloc[i]
                
                with st.container():
                    st.subheader(f"👤 Student: {student['Name']} ({student.get('Subject', 'N/A')})")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Roll Number", student[id_col] if id_col else "N/A")
                    c2.metric("Total Score", f"{student['Total']:.2f}")
                    
                    status = student['Category']
                    c3.metric("System Status", status)
                    
                    if status == "Safe":
                        st.info("✅ Logic Result: PASS")
                    elif status == "At Risk":
                        st.warning("⚠️ Logic Result: MARGINAL")
                    else:
                        st.error("❌ Logic Result: FAIL")
                    
                    st.dataframe(filtered_df.iloc[[i]], use_container_width=True)
                    st.markdown("---")
        else:
            st.error(f"No results found for '{search_query}' in {selected_subject}")
    else:
        st.info("👋 Welcome! Please enter a Name or Roll Number and select a Subject to see specific results.")
        
        # Show mini-stats of the selected subject when not searching
        subject_data = df[df['Subject'] == selected_subject] if selected_subject != "All" else df
        st.write(f"### 📊 {selected_subject} Overview")
        st.write(f"Total Records in this Category: **{len(subject_data)}**")