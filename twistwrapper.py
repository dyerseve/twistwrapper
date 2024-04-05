import subprocess
import json
from datetime import datetime, timedelta

def get_whois_created_dates(domains, nameserver):
    all_whois_created_dates = {}
    for domain in domains:
        try:
            output = subprocess.check_output(['dnstwist', '-f', 'json', '-m', '-w', '-r', '--nameservers', nameserver, domain])
            results = json.loads(output)
            for result in results:
                if 'whois_created' in result and result['whois_created']:
                    all_whois_created_dates[result['domain']] = {
                        'whois_created': datetime.strptime(result['whois_created'], "%Y-%m-%d"),
                        'whois_registrar': result.get('whois_registrar', 'N/A'),
                        'dns_mx': result.get('dns_mx', [])
                    }
        except subprocess.CalledProcessError as e:
            print(f"Error running dnstwist for domain {domain}: {e}")
    return all_whois_created_dates

def main(domains, nameserver, days, debug=False):
    whois_created_dates = get_whois_created_dates(domains, nameserver)
    if debug:
        for domain, info in whois_created_dates.items():
            print(f"Domain: {domain}, Whois Created: {info['whois_created']}")
    else:
        recent_domains = [(domain, info) for domain, info in whois_created_dates.items() if datetime.now() - info['whois_created'] < timedelta(days=days)]
        if recent_domains:
            for domain, info in recent_domains:
                print(f"Domain: {domain}, Whois Created: {info['whois_created']}, Whois Registrar: {info['whois_registrar']}, DNS MX: {', '.join(info['dns_mx'])}")

if __name__ == "__main__":
    domains = ['exmaple1.com', 'sample2.com']  # Your list of domains goes here
    nameserver = '8.8.8.8'  # Set your nameserver here
    days = 7  # Set the number of days here
    debug_mode = False  # Set to True to enable debug output
    main(domains, nameserver, days, debug_mode)
