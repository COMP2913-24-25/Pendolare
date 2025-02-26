"""
Direct diagnostic tool for Message Service
Run this locally to check on your service's status without needing to access the service directly
"""
import argparse
import http.client
import json
import sys
import ssl
import urllib.parse

def get_diagnostic_data(host, path="/diagnostics", ssl_enabled=True, verify_ssl=True, verbose=False):
    """Connect directly to the diagnostic endpoint and retrieve data"""
    try:
        # Set up SSL context if needed
        context = None
        if ssl_enabled and not verify_ssl:
            context = ssl._create_unverified_context()
        
        # Create the appropriate connection
        if ssl_enabled:
            conn = http.client.HTTPSConnection(host, context=context)
        else:
            conn = http.client.HTTPConnection(host)
        
        # Make the request
        if verbose:
            print(f"Connecting to {host}{path}...")
        
        # Add a unique query parameter to bypass caching
        if "?" in path:
            path = f"{path}&_t={hash(str(host))}"
        else:
            path = f"{path}?_t={hash(str(host))}"
            
        conn.request("GET", path)
        
        # Get and process the response
        response = conn.getresponse()
        status = response.status
        
        if verbose:
            print(f"Response status: {status}")
            print(f"Response headers: {response.getheaders()}")
        
        if status == 200:
            content = response.read().decode('utf-8')
            return True, status, content
        else:
            return False, status, response.read().decode('utf-8')
            
    except Exception as e:
        return False, 0, str(e)
    finally:
        if 'conn' in locals():
            conn.close()

def check_endpoints(host, ssl_enabled=True, verify_ssl=True, verbose=False):
    """Check multiple diagnostic endpoints"""
    results = {}
    
    # List of paths to check
    paths = [
        "/health",
        "/diagnostics",
        "/diagnostics/status",
        "/diagnostics/logs"
    ]
    
    # Try Kong Gateway path if it might be accessed through Kong
    if not host.startswith("message-service"):
        paths.append("/message/health")
        paths.append("/message/diagnostics")
    
    for path in paths:
        print(f"Checking {path}...")
        success, status, content = get_diagnostic_data(host, path, ssl_enabled, verify_ssl, verbose)
        
        results[path] = {
            "success": success,
            "status": status,
            "content": content[:500] + "..." if len(content) > 500 else content
        }
        
        print(f"  Status: {'✅ Success' if success else '❌ Failed'} ({status})")
        
        # If successful and returning JSON, pretty print a summary
        if success and content.strip().startswith('{'):
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    # Show a summary based on the endpoint
                    if path == "/diagnostics/status":
                        if "status" in data:
                            print("  Service Status:")
                            for key, value in data["status"].items():
                                print(f"    {key}: {value}")
                    elif path == "/diagnostics/logs":
                        if "logs" in data and isinstance(data["logs"], list):
                            print(f"  Recent Logs: (showing last {min(3, len(data['logs']))})")
                            for log in data["logs"][-3:]:
                                print(f"    [{log.get('level', 'INFO')}] {log.get('message', '')}")
                    elif path == "/health":
                        print(f"  Health: {content.strip()}")
            except json.JSONDecodeError:
                if verbose:
                    print("  Response is not valid JSON")
        
        print()
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Check diagnostic endpoints for Message Service')
    parser.add_argument('--host', type=str, help='Host to connect to (e.g., example.azurecontainerapps.io)')
    parser.add_argument('--no-ssl', action='store_true', help='Disable SSL (use HTTP instead of HTTPS)')
    parser.add_argument('--no-verify', action='store_true', help='Disable SSL certificate verification')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Get host from arguments or prompt
    host = args.host
    if not host:
        host = input("Enter host (e.g., example.azurecontainerapps.io): ")
    
    # Remove protocol if included
    if "://" in host:
        host = host.split("://")[1]
    
    # Remove path if included
    if "/" in host:
        host = host.split("/")[0]
    
    print(f"\nChecking diagnostic endpoints on {host}\n")
    results = check_endpoints(host, not args.no_ssl, not args.no_verify, args.verbose)
    
    print("\nSummary:")
    for path, result in results.items():
        status_symbol = "✅" if result["success"] else "❌"
        print(f"{status_symbol} {path}: HTTP {result['status']}")
    
    # Provide troubleshooting guidance
    working_endpoints = sum(1 for r in results.values() if r["success"])
    if working_endpoints == 0:
        print("\n❌ No endpoints are accessible. Possible problems:")
        print("  - The service might not be running")
        print("  - There could be network restrictions in place")
        print("  - The endpoints may not be exposed externally")
        print("  - CORS might be blocking the requests")
        print("\nTroubleshooting:")
        print("  1. Check if the service is deployed and running")
        print("  2. Verify the ingress settings in your Container App")
        print("  3. Check if Kong Gateway is properly routing to the service")
        print("  4. Try accessing directly or through Kong Gateway")
    elif working_endpoints < len(results):
        print("\n⚠️ Some endpoints are accessible, but not all.")
        print("This suggests the service is running but there might be:")
        print("  - Routing issues for specific paths")
        print("  - Authorization requirements on some endpoints")
    else:
        print("\n✅ All diagnostic endpoints are accessible!")

if __name__ == "__main__":
    main()
