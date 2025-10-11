import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model import ScratchLinearRegression

# Set page configuration
st.set_page_config(
    page_title="Academic Performance and Career Outcomes Analysis",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .prediction-result {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #3498db;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">Academic Performance and Career Outcomes Analysis</h1>', unsafe_allow_html=True)
st.markdown("""
This analytical tool examines the relationship between academic performance metrics and career outcomes 
using statistical modeling techniques. The system provides insights into how academic achievements 
correlate with professional opportunities.
""")

# Load and prepare data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('placement_extended.csv')
        return df
    except FileNotFoundError:
        st.error("Required data file not found. Please ensure the dataset is available in the specified location.")
        return None

# Load data
df = load_data()

if df is not None:
    # Sidebar for analysis parameters
    with st.sidebar:
        st.header("Analysis Parameters")
        st.markdown("Configure the analysis parameters below:")
        
        cgpa_input = st.number_input(
            "Academic Performance Score", 
            min_value=0.0, 
            max_value=10.0, 
            value=7.5, 
            step=0.1,
            help="Enter academic performance score for analysis"
        )
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Single Prediction", "Comparative Analysis"],
            help="Choose the type of analysis to perform"
        )

    # Train model
    @st.cache_resource
    def train_model():
        lr = ScratchLinearRegression()
        X = df['cgpa'].values
        y = df['package'].values
        lr.fit(X, y)
        return lr

    # Train the model
    try:
        model = train_model()
        
        # Key Metrics Section
        st.subheader("Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Observations", f"{len(df):,}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Mean Academic Score", f"{df['cgpa'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Mean Career Outcome", f"{df['package'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Correlation Coefficient", f"{df['cgpa'].corr(df['package']):.3f}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Model Information
        st.subheader("Statistical Model")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            The analytical model employs linear regression to quantify the relationship between 
            academic performance and career outcomes. This statistical approach provides a 
            mathematical framework for understanding how variations in academic achievement 
            correspond to differences in professional opportunities.
            """)
            
            st.markdown(f"""
            **Regression Equation:**  
            Career Outcome = {model.m:.4f} × Academic Score + {model.b:.4f}
            """)
            
        with col2:
            st.markdown("**Model Parameters**")
            st.write(f"Slope Coefficient: {model.m:.4f}")
            st.write(f"Intercept Term: {model.b:.4f}")

        # Prediction Section
        if st.sidebar.button("Generate Analysis", type="primary"):
            prediction = model.predict(cgpa_input)
            
            st.subheader("Analysis Results")
            st.markdown('<div class="prediction-result">', unsafe_allow_html=True)
            st.markdown(f"### Projected Career Outcome: **{prediction:.2f}**")
            st.markdown(f"""
            Based on an academic performance score of **{cgpa_input}**, 
            the statistical model projects a career outcome of **{prediction:.2f}**.
            This projection represents the expected value derived from the established 
            relationship between academic performance and career outcomes in the dataset.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        # Visualization Section
        st.subheader("Statistical Visualization")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Scatter plot with regression line
        ax1.scatter(df['cgpa'], df['package'], alpha=0.7, color='#3498db', s=50, label='Observations')
        
        x_range = np.linspace(df['cgpa'].min(), df['cgpa'].max(), 100)
        y_pred_line = model.predict(x_range)
        ax1.plot(x_range, y_pred_line, color='#e74c3c', linewidth=2.5, label='Regression Line')

        if cgpa_input is not None:
            pred_value = model.predict(cgpa_input)
            ax1.scatter([cgpa_input], [pred_value], color='#2ecc71', s=150, 
                      label=f'Analysis Point (Score={cgpa_input})', zorder=5, edgecolors='black')

        ax1.set_xlabel('Academic Performance Score', fontsize=12)
        ax1.set_ylabel('Career Outcome Metric', fontsize=12)
        ax1.set_title('Relationship Analysis: Academic Performance vs Career Outcomes', fontsize=14, pad=20)
        ax1.legend()
        ax1.grid(True, alpha=0.2)

        # Distribution analysis
        ax2.hist(df['package'], bins=25, alpha=0.8, color='#9b59b6', edgecolor='white', linewidth=0.5)
        ax2.axvline(df['package'].mean(), color='#e74c3c', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["package"].mean():.2f}')
        ax2.set_xlabel('Career Outcome Metric', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Distribution of Career Outcomes', fontsize=14, pad=20)
        ax2.legend()
        ax2.grid(True, alpha=0.2)

        plt.tight_layout()
        st.pyplot(fig)

        # Model Performance Metrics
        st.subheader("Model Performance Assessment")
        
        X_all = df['cgpa'].values.astype(float)
        y_all = df['package'].values.astype(float)
        y_pred_all = model.predict(X_all)

        # Calculate performance metrics
        mse = np.mean((y_all - y_pred_all) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_all - y_pred_all))
        
        ss_res = np.sum((y_all - y_pred_all) ** 2)
        ss_tot = np.sum((y_all - np.mean(y_all)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        with perf_col1:
            st.metric("Mean Squared Error", f"{mse:.4f}")
        with perf_col2:
            st.metric("Root Mean Squared Error", f"{rmse:.4f}")
        with perf_col3:
            st.metric("Mean Absolute Error", f"{mae:.4f}")
        with perf_col4:
            st.metric("R-squared", f"{r_squared:.4f}")

        # Interpretation Guide
        st.subheader("Interpretation Guidelines")
        st.markdown("""
        - **R-squared Value**: Indicates the proportion of variance in career outcomes that can be explained by academic performance scores
        - **Regression Slope**: Represents the expected change in career outcome for each unit increase in academic performance
        - **Error Metrics**: Provide insight into the average magnitude of prediction errors
        - **Analysis Point**: Shows how a specific academic performance score relates to the overall trend
        """)

        # Methodology
        with st.expander("Methodology Details"):
            st.markdown("""
            ### Analytical Methodology
            
            This analysis employs ordinary least squares (OLS) linear regression, a widely accepted 
            statistical method for modeling relationships between variables. The approach includes:
            
            1. **Data Preparation**: Ensuring data quality and appropriate formatting
            2. **Model Training**: Calculating optimal parameters to minimize prediction errors
            3. **Validation**: Assessing model performance using multiple statistical metrics
            4. **Interpretation**: Providing context and meaning to the statistical results
            
            The model assumes a linear relationship between academic performance and career outcomes, 
            which provides a foundational understanding while acknowledging that real-world 
            relationships may involve additional complex factors.
            """)

    except Exception as e:
        st.error(f"Analysis encountered an issue: {str(e)}")
        st.info("Please verify data integrity and model configuration.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d;'>"
    "Academic and Career Analytics Platform | Designed for Educational Insight and Research Purposes"
    "</div>", 
    unsafe_allow_html=True
)