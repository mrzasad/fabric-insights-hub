from datetime import datetime, timedelta

def monitor_refresh_status():
    """Monitor and manage semantic model refreshes"""
    
    # Get refresh history
    refresh_history = fabric.list_refresh_history(
        dataset="Sales Analytics",
        workspace="workspace-id"
    )
    
    # Analyze performance
    avg_duration = refresh_history['Duration'].mean()
    success_rate = (
        refresh_history['Status'] == 'Success'
    ).mean() * 100
    
    # Check for failures
    recent_failures = refresh_history[
        (refresh_history['Status'] == 'Failed') &
        (refresh_history['End Time'] > datetime.now() - timedelta(hours=24))
    ]
    
    # Trigger refresh if needed
    if len(recent_failures) > 0:
        fabric.refresh_dataset(
            dataset="Sales Analytics",
            workspace="workspace-id"
        )
        print("Triggered refresh due to recent failures")
    
    return {
        'average_duration': avg_duration,
        'success_rate': success_rate,
        'recent_failures': len(recent_failures)
    }

# Example output:
# {
#     'average_duration': '4.5 minutes',
#     'success_rate': 98.5,
#     'recent_failures': 1
# }