import concurrent.futures
import csv
import json
import subprocess
import time


def generate_addresses():
    try:
        # Call the 'hdwallet generate' command using the subprocess module
        output = subprocess.run(['hdwallet', 'generate'], check=True, text=True, capture_output=True)
        # Assuming the output is in json format
        output_dict = json.loads(output.stdout)
        return output_dict
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while generating addresses: {e.stderr}")
        # Handle any errors that might occur during the address generation process
        return None


def write_output(output_dict):
    with open(output_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Flatten the addresses dictionary
        output_dict["addresses"] = ", ".join([f"{k}: {v}" for k, v in output_dict.get("addresses", {}).items()])
        writer.writerow(output_dict)


if __name__ == "__main__":
    output_file = "generated_output.csv"
    fieldnames = ["cryptocurrency", "symbol", "network", "strength", "entropy", "mnemonic", "language", "passphrase", "seed",
                "root_xprivate_key", "root_xpublic_key", "xprivate_key", "xpublic_key", "uncompressed", "compressed",
                "chain_code", "private_key", "public_key", "wif", "finger_print", "semantic", "path", "hash", "addresses"]
    with open(output_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Check if the file is empty and write headers if needed
        if file.tell() == 0:
            writer.writeheader()
    count = 0
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            future = executor.submit(generate_addresses)
            output_dict = future.result()
            if output_dict:
                write_output(output_dict)
                count += 1
            if count % 100 == 0:
                elapsed_time = time.time() - start_time
                addresses_per_sec = count / elapsed_time
                addresses_per_min = addresses_per_sec * 60
                addresses_per_day = addresses_per_min * 1440
                print(f"Generated {count} addresses in {elapsed_time:.2f} seconds. Speed: {addresses_per_sec:.2f} addresses/sec, {addresses_per_min:.2f} addresses/min, {addresses_per_day:.2f} addresses/day")