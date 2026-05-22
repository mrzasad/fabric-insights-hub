# Analyze customer segments
customer_query = """
EVALUATE 
SUMMARIZECOLUMNS(
    'Customer'[Segment],
    'Customer'[Region],
    "Customer_Count", DISTINCTCOUNT('Customer'[ID]),
    "Avg_LTV", AVERAGE('Customer'[LifetimeValue]),
    "Total_Revenue", SUM('Sales'[Amount])
)
"""

customers = fabric.evaluate_dax(
    workspace="workspace-id",
    dataset="Customer Analytics",
    dax_string=customer_query
)

# Perform segmentation analysis
segment_analysis = customers.groupby('Segment').agg({
    'Customer_Count': 'sum',
    'Avg_LTV': 'mean',
    'Total_Revenue': 'sum'
}).round(2)

print(segment_analysis)
"""
            Customer_Count  Avg_LTV  Total_Revenue
Segment                                           
Enterprise             150   25,000      3,750,000
SMB                    450   12,500      5,625,000
Consumer              1200    5,000      6,000,000
"""