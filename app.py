"""
Microsoft Fabric Sample Application
A simple, functional demo of MS Fabric integration with Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Import utilities
from utils.fabric_client import FabricClient
from utils.sample_data import SampleDataGenerator

# Page configuration
st.set_page_config(
    page_title="Fabric Analytics Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .success-metric {
        color: #28a745;
        font-size: 24px;
        font-weight: bold;
    }
    .warning-metric {
        color: #ffc107;
        font-size: 24px;
        font-weight: bold;
    }
    .danger-metric {
        color: #dc3545;
        font-size: 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'fabric_client' not in st.session_state:
    st.session_state.fabric_client = FabricClient()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = None
if 'customer_data' not in st.session_state:
    st.session_state.customer_data = None

# Title
st.title("📊 Microsoft Fabric Analytics Demo")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Connection Mode
    connection_mode = st.radio(
        "Data Source Mode",
        ["📦 Sample Data (No Fabric Required)", "☁️ Connect to Live Fabric"],
        help="Choose between sample data or live Fabric connection"
    )
    
    st.markdown("---")
    
    if connection_mode == "☁️ Connect to Live Fabric":
        st.subheader("Fabric Connection")
        
        # Authentication
        if st.button("🔐 Authenticate", use_container_width=True):
            with st.spinner("Authenticating..."):
                success, message = st.session_state.fabric_client.authenticate()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        # Workspace configuration
        workspace_id = st.text_input(
            "Workspace ID",
            value=st.session_state.fabric_client.workspace_id,
            help="Enter your Fabric workspace ID"
        )
        
        dataset_name = st.text_input(
            "Dataset Name",
            value="Sales Analytics",
            help="Enter the dataset name to query"
        )
    
    st.markdown("---")
    st.subheader("📈 Dashboard Filters")
    
    # Date range filter
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=90), datetime.now()),
        max_value=datetime.now()
    )
    
    # Category filter (will be populated dynamically)
    if st.session_state.sales_data is not None:
        categories = st.session_state.sales_data['Category'].unique().tolist()
        selected_categories = st.multiselect(
            "Product Categories",
            categories,
            default=categories[:2]
        )

# Main content
if connection_mode == "📦 Sample Data (No Fabric Required)":
    # Load sample data
    if st.button("🎲 Generate Sample Data", type="primary", use_container_width=True):
        with st.spinner("Generating sample data..."):
            generator = SampleDataGenerator()
            
            # Generate regular and anomaly data
            regular_sales = generator.generate_sales_data(months=6)
            st.session_state.sales_data = generator.generate_anomalies(regular_sales)
            st.session_state.customer_data = generator.generate_customer_data(100)
            st.session_state.data_loaded = True
            
            st.success("Sample data generated successfully!")
            st.rerun()

# Display dashboard when data is loaded
if st.session_state.data_loaded:
    sales_df = st.session_state.sales_data
    customer_df = st.session_state.customer_data
    
    # Filter data by date range if specified
    if len(date_range) == 2:
        start_date, end_date = date_range
        sales_df = sales_df[
            (sales_df['Date'].dt.date >= start_date) & 
            (sales_df['Date'].dt.date <= end_date)
        ]
    
    # Filter by category if selected
    if 'selected_categories' in locals() and selected_categories:
        sales_df = sales_df[sales_df['Category'].isin(selected_categories)]
    
    # Top-level metrics
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = sales_df['Sales_Amount'].sum()
        avg_sales = sales_df['Sales_Amount'].mean()
        st.metric(
            "Total Sales",
            f"${total_sales:,.0f}",
            delta=f"Avg: ${avg_sales:,.0f}/day"
        )
    
    with col2:
        total_units = sales_df['Units_Sold'].sum()
        st.metric(
            "Total Units Sold",
            f"{total_units:,}",
            delta=f"{len(sales_df)} days"
        )
    
    with col3:
        # Detect anomalies using IQR method
        q1 = sales_df['Sales_Amount'].quantile(0.25)
        q3 = sales_df['Sales_Amount'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        anomalies = sales_df[
            (sales_df['Sales_Amount'] < lower_bound) | 
            (sales_df['Sales_Amount'] > upper_bound)
        ]
        
        st.metric(
            "Anomalies Detected",
            len(anomalies),
            delta=f"Threshold: ${upper_bound:,.0f}",
            delta_color="inverse"
        )
    
    with col4:
        total_customers = len(customer_df)
        st.metric(
            "Total Customers",
            f"{total_customers:,}",
            delta=f"Avg LTV: ${customer_df['Lifetime_Value'].mean():,.0f}"
        )
    
    st.markdown("---")
    
    # Charts section
    tab1, tab2, tab3 = st.tabs([
        "📈 Sales Trends", 
        "👥 Customer Analytics", 
        "⚠️ Anomaly Detection"
    ])
    
    # Tab 1: Sales Trends
    with tab1:
        st.subheader("Daily Sales Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Line chart of daily sales
            fig_line = px.line(
                sales_df,
                x='Date',
                y='Sales_Amount',
                title='Daily Sales Trend',
                labels={'Sales_Amount': 'Sales ($)', 'Date': 'Date'}
            )
            fig_line.update_layout(height=400)
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            # Sales by category
            category_sales = sales_df.groupby('Category')['Sales_Amount'].sum().reset_index()
            fig_pie = px.pie(
                category_sales,
                values='Sales_Amount',
                names='Category',
                title='Sales by Category'
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Moving average
        st.subheader("7-Day Moving Average")
        sales_df['MA7'] = sales_df['Sales_Amount'].rolling(window=7).mean()
        
        fig_ma = go.Figure()
        fig_ma.add_trace(go.Scatter(
            x=sales_df['Date'],
            y=sales_df['Sales_Amount'],
            mode='lines',
            name='Daily Sales',
            line=dict(color='lightblue')
        ))
        fig_ma.add_trace(go.Scatter(
            x=sales_df['Date'],
            y=sales_df['MA7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color='darkblue', width=3)
        ))
        fig_ma.update_layout(
            title='Sales with 7-Day Moving Average',
            height=400
        )
        st.plotly_chart(fig_ma, use_container_width=True)
    
    # Tab 2: Customer Analytics
    with tab2:
        st.subheader("Customer Segmentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer distribution by region
            region_dist = customer_df['Region'].value_counts().reset_index()
            region_dist.columns = ['Region', 'Count']
            
            fig_region = px.bar(
                region_dist,
                x='Region',
                y='Count',
                title='Customers by Region',
                color='Region'
            )
            st.plotly_chart(fig_region, use_container_width=True)
        
        with col2:
            # Customer lifetime value distribution
            fig_ltv = px.histogram(
                customer_df,
                x='Lifetime_Value',
                title='Customer Lifetime Value Distribution',
                nbins=20
            )
            fig_ltv.add_vline(
                x=customer_df['Lifetime_Value'].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text="Average LTV"
            )
            st.plotly_chart(fig_ltv, use_container_width=True)
        
        # Segment analysis
        st.subheader("Segment Performance")
        
        segment_metrics = customer_df.groupby('Segment').agg({
            'Customer_ID': 'count',
            'Lifetime_Value': ['mean', 'sum']
        }).round(2)
        segment_metrics.columns = ['Customer Count', 'Avg LTV', 'Total LTV']
        segment_metrics = segment_metrics.reset_index()
        
        st.dataframe(
            segment_metrics,
            use_container_width=True,
            hide_index=True
        )
    
    # Tab 3: Anomaly Detection
    with tab3:
        st.subheader("Statistical Anomaly Detection")
        
        # Anomaly visualization
        sales_df['Anomaly'] = 'Normal'
        sales_df.loc[sales_df.index.isin(anomalies.index), 'Anomaly'] = 'Anomaly'
        
        fig_anomaly = px.scatter(
            sales_df,
            x='Date',
            y='Sales_Amount',
            color='Anomaly',
            color_discrete_map={'Normal': '#636EFA', 'Anomaly': '#EF553B'},
            title='Anomaly Detection Visualization',
            size_max=10
        )
        
        # Add threshold lines
        fig_anomaly.add_hline(
            y=upper_bound,
            line_dash="dash",
            line_color="red",
            annotation_text="Upper Threshold"
        )
        fig_anomaly.add_hline(
            y=lower_bound,
            line_dash="dash",
            line_color="red",
            annotation_text="Lower Threshold"
        )
        
        st.plotly_chart(fig_anomaly, use_container_width=True)
        
        # Anomaly details
        if len(anomalies) > 0:
            st.subheader("🔍 Anomalous Records")
            st.dataframe(
                anomalies[['Date', 'Sales_Amount', 'Units_Sold', 'Category']].sort_values(
                    'Sales_Amount', ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Highest Anomaly", f"${anomalies['Sales_Amount'].max():,.0f}")
            with col2:
                st.metric("Lowest Anomaly", f"${anomalies['Sales_Amount'].min():,.0f}")
            with col3:
                anomaly_rate = (len(anomalies) / len(sales_df)) * 100
                st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
        else:
            st.info("No anomalies detected in the current data range.")
    
    # Data export section
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export sales data
        csv_sales = sales_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Sales Data (CSV)",
            data=csv_sales,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export customer data
        csv_customers = customer_df.to_csv(index=False)
        st.download_button(
            label="👥 Download Customer Data (CSV)",
            data=csv_customers,
            file_name=f"customer_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif connection_mode == "☁️ Connect to Live Fabric":
    st.info("""
    ### 🔌 Live Fabric Connection
    
    To connect to Microsoft Fabric:
    
    1. **Enter your Azure credentials** in the `.env` file
    2. **Click "Authenticate"** in the sidebar
    3. **Enter your Workspace ID** and Dataset Name
    4. The app will connect to Fabric and display your real data
    
    **Prerequisites:**
    - Azure subscription with Fabric capacity
    - Service principal with appropriate permissions
    - Semantic model configured in Fabric
    
    For now, you can use the **Sample Data mode** to explore the app's features.
    """)
    
    # Placeholder for Fabric connection
    if st.session_state.fabric_client.credential:
        st.success("✅ Connected to Azure")
        
        # This would be replaced with actual Fabric API calls
        st.subheader("Fabric Data Preview")
        
        # Example Fabric query (commented out for safety)
        """
        import sempy.fabric as fabric
        
        try:
            datasets = fabric.list_datasets(workspace=workspace_id)
            st.dataframe(datasets)
        except Exception as e:
            st.error(f"Error querying Fabric: {e}")
        """

else:
    # Welcome screen when no data is loaded
    st.info("""
    ### 👋 Welcome to the Fabric Analytics Demo!
    
    This application demonstrates key Microsoft Fabric capabilities:
    
    - **📊 Data Exploration**: Interactive dashboards and visualizations
    - **🧠 Anomaly Detection**: Statistical outlier detection
    - **📈 Trend Analysis**: Moving averages and pattern recognition
    - **👥 Customer Analytics**: Segmentation and lifetime value analysis
    
    **Get Started:**
    1. Choose **"Sample Data"** mode in the sidebar
    2. Click **"Generate Sample Data"** to see the demo
    3. Explore the different tabs and visualizations
    
    Or connect to a **live Fabric workspace** if you have one configured.
    """)
    
    # Display sample layout
    st.markdown("### 📱 App Preview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Total Sales</h4>
            <p class="success-metric">$XXX,XXX</p>
            <small>Average: $X,XXX/day</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>⚠️ Anomalies</h4>
            <p class="warning-metric">XX</p>
            <small>Detection Active</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>👥 Customers</h4>
            <p class="success-metric">XXX</p>
            <small>Across segments</small>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Microsoft Fabric Analytics Demo | Built with Streamlit and Plotly</p>
        <p style='font-size: 12px;'>This is a sample application for demonstration purposes</p>
    </div>
    """,
    unsafe_allow_html=True
)