import os
import platform
import subprocess
import asyncio
import requests
import fireducks.pandas as pd  # Import regular pandas as pd
from icmplib import async_ping


 # Added import

# List of Public DNS Servers
dns_servers = {
    "Google DNS": "8.8.8.8",
    "Google DNS (Backup)": "8.8.4.4",
    "Cloudflare DNS": "1.1.1.1",
    "Cloudflare DNS (Backup)": "1.0.0.1",
    "OpenDNS": "208.67.222.222",
    "OpenDNS (Backup)": "208.67.220.220",
    "Quad9": "9.9.9.9",
    "Quad9 (Backup)": "149.112.112.112",
    "AdGuard DNS": "94.140.14.14",
    "AdGuard DNS (Backup)": "94.140.15.15"
}

# Function to get user's location (for reference)
def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        return f"{data.get('city', 'Unknown City')}, {data.get('country', 'Unknown')}"
    except Exception:
        return "Unknown Location"

# Function to check current DNS settings
def get_current_dns():
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
            dns_list = [line.split(":")[-1].strip() for line in result.stdout.split("\n") if "DNS Servers" in line]
        else:
            with open("/etc/resolv.conf", "r") as file:
                dns_list = [line.split()[1] for line in file.readlines() if line.startswith("nameserver")]
        return dns_list if dns_list else ["Unknown"]
    except Exception:
        return ["Unknown"]

# Function to ping DNS servers
async def ping_dns(name, dns):
    try:
        result = await async_ping(dns, count=2, timeout=0.5)
        return {"DNS_Name": name, "DNS_Server": dns, "Response_Time": result.avg_rtt if result else float("inf")}
    except Exception:
        return {"DNS_Name": name, "DNS_Server": dns, "Response_Time": float("inf")}

# Function to test all DNS servers
async def test_dns_servers():
    tasks = [ping_dns(name, ip) for name, ip in dns_servers.items()]
    results = await asyncio.gather(*tasks)
    
    # Sort results by response time
    results.sort(key=lambda x: x["Response_Time"])

    # Convert to pandas DataFrame for better formatting
    df = pd.DataFrame(results)
    print("\nTest Results:\n", df.to_string(index=False))

    # Select the best DNS
    best_dns = results[0] if results else None
    return best_dns

# Function to apply the best DNS server
def apply_dns_settings(dns_server):
    if not dns_server:
        print("No valid DNS to apply.")
        return

    print(f"Applying new DNS: {dns_server}...")

    if platform.system() == "Windows":
        interface_name = "Wi-Fi"  # Adjust this if needed
        command = f'netsh interface ip set dns name="{interface_name}" static {dns_server}'
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif platform.system() == "Linux":
        try:
            with open("/etc/resolv.conf", "w") as file:
                file.write(f"nameserver {dns_server}\n")
            print(f"DNS changed to {dns_server}")
        except PermissionError:
            print("Permission Denied: Run with sudo to change DNS settings.")

# Main function
async def main():
    print("\n🚀 DNS Optimizer Started!")
    print(f"📍 Location: {get_user_location()}")
    print(f"🌐 Current DNS: {', '.join(get_current_dns())}\n")

    # Run DNS tests
    best_dns = await test_dns_servers()

    if best_dns:
        print(f"\n🏆 Best DNS: {best_dns['DNS_Name']} ({best_dns['DNS_Server']})")
        apply_choice = input("Do you want to apply this DNS? (y/n): ").strip().lower()
        if apply_choice == "y":
            apply_dns_settings(best_dns["DNS_Server"])
        else:
            print("No changes made.")
    else:
        print("\nNo valid DNS found.")

# Run the script
if __name__ == "__main__":  # Corrected condition
    asyncio.run(main())