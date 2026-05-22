"""
Fabric Client - Manages authentication and connection to Microsoft Fabric
"""
import os
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FabricClient:
    """Simple Fabric client for managing connections"""
    
    def __init__(self):
        self.credential = None
        self.workspace_name = os.getenv("FABRIC_WORKSPACE_NAME", "My Workspace")
        self.workspace_id = os.getenv("FABRIC_WORKSPACE_ID", "")
        
    def authenticate(self):
        """Authenticate with Azure"""
        try:
            # Try environment variables first, then managed identity
            tenant_id = os.getenv("AZURE_TENANT_ID")
            client_id = os.getenv("AZURE_CLIENT_ID")
            client_secret = os.getenv("AZURE_CLIENT_SECRET")
            
            if all([tenant_id, client_id, client_secret]):
                self.credential = ClientSecretCredential(
                    tenant_id=tenant_id,
                    client_id=client_id,
                    client_secret=client_secret
                )
            else:
                self.credential = DefaultAzureCredential()
            
            return True, "Authentication successful"
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def get_workspace_info(self):
        """Get workspace information"""
        return {
            "name": self.workspace_name,
            "id": self.workspace_id,
            "authenticated": self.credential is not None
        }