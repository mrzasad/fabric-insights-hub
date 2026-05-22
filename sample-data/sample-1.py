# Connect to Fabric and analyze sales data
from utils.fabric_client import FabricClient

# Initialize client
client = FabricClient()
client.authenticate()

# Query semantic model
dax_query = """
EVALUATE 
SUMMARIZECOLUMNS(
    'Date'[Month],
    'Product'[Category],
    "Total_Sales", SUM('Sales'[Amount]),
    "Profit_Margin", [Profit Margin %],
    "YoY_Growth", [YoY Growth]
)
ORDER BY 'Date'[Month] ASC
"""

# Execute query
sales_data = fabric.evaluate_dax(
    workspace="workspace-id",
    dataset="Sales Analytics",
    dax_string=dax_query
)

# Output example
"""
        Month  Category  Total_Sales  Profit_Margin  YoY_Growth
0  2024-01   Electronics    125,000          23.5%       12.3%
1  2024-01   Clothing       89,000           31.2%        8.7%
2  2024-01   Food           156,000          19.8%       15.2%
3  2024-02   Electronics    142,000          24.1%       11.8%
4  2024-02   Clothing       95,000           30.5%        9.2%
"""