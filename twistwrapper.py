import subprocess
import json
from datetime import datetime, timedelta
import logging

def configure_logging():
    logging.basicConfig(filename='dns_twist.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_whois_created_dates(domains, nameserver):
    all_whois_created_dates = {}
    for domain in domains:
        try:
            logging.info(f"Processing domain: {domain}")
            output = subprocess.check_output(['dnstwist', '-f', 'json', '-m', '-w', '-r', '--nameservers', nameserver, domain])
            results = json.loads(output)
            all_whois_created_dates[domain] = results
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running dnstwist for domain {domain}: {e}")
    return all_whois_created_dates

def main(domains, nameserver, days, debug=False):
    logging.info("Job started.")
    whois_created_dates = get_whois_created_dates(domains, nameserver)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    json_file = f'dns_twist_{timestamp}.json'
    with open(json_file, 'w') as f:
        json.dump(whois_created_dates, f, indent=4)
        logging.info(f"JSON output saved to {json_file}")

    if debug:
        for domain, results in whois_created_dates.items():
            for result in results:
                logging.info(f"Domain: {result['domain']}, Whois Created: {result.get('whois_created', 'N/A')}")
                print(f"Domain: {result['domain']}, Whois Created: {result.get('whois_created', 'N/A')}")
    else:
        recent_domains = {domain: results for domain, results in whois_created_dates.items() if any(datetime.now() - datetime.strptime(result['whois_created'], "%Y-%m-%d") < timedelta(days=days) for result in results)}
        for domain, results in recent_domains.items():
            logging.info(f"Domain: {domain}, Results:")
            print(f"Domain: {domain}, Results:")
            for result in results:
                log_message = f"\tWhois Created: {result.get('whois_created', 'N/A')}, Whois Registrar: {result.get('whois_registrar', 'N/A')}, DNS MX: {', '.join(result.get('dns_mx', []))}"
                logging.info(log_message)
                print(log_message)
    logging.info("Job ended.")

if __name__ == "__main__":
    configure_logging()
    domains = ['example.com','sample.com']  # Your list of domains goes here
    nameserver = '8.8.8.8'  # Set your nameserver here
    days = 7  # Set the number of days here
    debug_mode = False  # Set to True to enable debug output
    main(domains, nameserver, days, debug_mode)
