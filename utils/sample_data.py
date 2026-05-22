"""
Sample Data Generator - Creates test data for development without Fabric access
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SampleDataGenerator:
    """Generates sample data for testing the app"""
    
    @staticmethod
    def generate_sales_data(months=12):
        """Generate sample sales data"""
        np.random.seed(42)
        
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate sales patterns with seasonality and trend
        base_sales = 1000
        trend = np.linspace(0, 500, len(dates))
        seasonal = 200 * np.sin(np.linspace(0, 4*np.pi, len(dates)))
        noise = np.random.normal(0, 100, len(dates))
        
        sales = base_sales + trend + seasonal + noise
        sales = np.maximum(sales, 0)  # No negative sales
        
        # Create DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Sales_Amount': sales.round(2),
            'Units_Sold': (sales / 25).round(0).astype(int),
            'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], len(dates))
        })
        
        return df
    
    @staticmethod
    def generate_customer_data(n_customers=100):
        """Generate sample customer data"""
        np.random.seed(123)
        
        customers = pd.DataFrame({
            'Customer_ID': [f'CUST-{i:04d}' for i in range(1, n_customers + 1)],
            'Name': [f'Customer {i}' for i in range(1, n_customers + 1)],
            'Region': np.random.choice(['North', 'South', 'East', 'West'], n_customers),
            'Segment': np.random.choice(['Enterprise', 'SMB', 'Consumer'], n_customers, p=[0.2, 0.3, 0.5]),
            'Lifetime_Value': np.random.normal(5000, 2000, n_customers).round(2),
            'Signup_Date': [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(n_customers)]
        })
        
        return customers
    
    @staticmethod
    def generate_anomalies(regular_data):
        """Inject some anomalies into the data for testing"""
        anomaly_data = regular_data.copy()
        
        # Add some price spikes
        anomaly_indices = np.random.choice(len(anomaly_data), 5, replace=False)
        anomaly_data.loc[anomaly_indices, 'Sales_Amount'] *= np.random.uniform(3, 5, len(anomaly_indices))
        
        # Add some zero sales days
        zero_indices = np.random.choice(len(anomaly_data), 3, replace=False)
        anomaly_data.loc[zero_indices, 'Sales_Amount'] = 0
        
        return anomaly_data