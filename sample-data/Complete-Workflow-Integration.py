# Complete analytics workflow example
class AnalyticsWorkflow:
    """End-to-end analytics workflow"""
    
    def __init__(self):
        self.client = FabricClient()
        self.client.authenticate()
        
    def run_daily_analysis(self):
        """Execute complete daily analysis pipeline"""
        
        # 1. Refresh data
        print("Step 1: Refreshing semantic models...")
        fabric.refresh_dataset(
            dataset="Daily Sales",
            workspace="workspace-id"
        )
        
        # 2. Extract metrics
        print("Step 2: Extracting KPIs...")
        kpi_query = """
        EVALUATE 
        ROW(
            "Total_Revenue", [Total Revenue],
            "Total_Orders", [Total Orders],
            "Avg_Order_Value", [AOV],
            "Active_Customers", [Active Customers]
        )
        """
        kpis = fabric.evaluate_dax(
            workspace="workspace-id",
            dataset="Daily Sales",
            dax_string=kpi_query
        )
        
        # 3. Detect anomalies
        print("Step 3: Running anomaly detection...")
        sales_data = fabric.evaluate_dax(
            workspace="workspace-id",
            dataset="Daily Sales",
            dax_string="""
            EVALUATE 
            SUMMARIZECOLUMNS(
                'Date'[Date],
                "Revenue", [Total Revenue]
            )
            """
        )
        
        anomalies = detect_anomalies(sales_data)
        
        # 4. Generate alerts
        if len(anomalies) > 0:
            send_alert(f"Found {len(anomalies)} anomalies in today's data")
        
        # 5. Export report
        report = {
            'date': datetime.now().isoformat(),
            'kpis': kpis.to_dict(),
            'anomalies': anomalies.to_dict(),
            'status': 'Success'
        }
        
        return report

# Example output:
# {
#     'date': '2024-01-15T10:30:00',
#     'kpis': {
#         'Total_Revenue': 1250000,
#         'Total_Orders': 4500,
#         'Avg_Order_Value': 278,
#         'Active_Customers': 2300
#     },
#     'anomalies': {
#         'count': 3,
#         'dates': ['2024-01-05', '2024-01-12', '2024-01-15']
#     },
#     'status': 'Success'
# }