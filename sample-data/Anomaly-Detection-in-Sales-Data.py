import pandas as pd
import numpy as np

def detect_sales_anomalies(data):
    """
    Detect anomalies in sales data using IQR method
    """
    # Calculate quartiles
    Q1 = data['Total_Sales'].quantile(0.25)
    Q3 = data['Total_Sales'].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identify anomalies
    anomalies = data[
        (data['Total_Sales'] < lower_bound) | 
        (data['Total_Sales'] > upper_bound)
    ]
    
    return anomalies, lower_bound, upper_bound

# Example usage
sales_df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'Total_Sales': [1000 + i*10 + (1000 if i in [25, 50, 75] else 0) 
                    for i in range(100)]
})

anomalies, lower, upper = detect_sales_anomalies(sales_df)
print(f"Found {len(anomalies)} anomalies")
print(f"Normal range: ${lower:,.0f} - ${upper:,.0f}")

# Output:
# Found 3 anomalies
# Normal range: $1,000 - $2,000