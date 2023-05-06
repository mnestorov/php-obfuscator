import sys
import base64
import os
import re
import logging
import shutil
from zlib import compress
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import (log_filename, YELLOW, BLUE, GREEN, RED, RESET)

# Configure logging
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def obfuscate_php(input_file, obfuscation_level, create_backup, output_directory):
    if create_backup:
        backup_file = f"{os.path.splitext(input_file)[0]}_backup.php"
        shutil.copy2(input_file, backup_file)
        logging.info(f"Created backup: {backup_file}")

    try:
        logging.info(f"Obfuscating {input_file} with level: {obfuscation_level}")

        with open(input_file, "r") as f:
            php_code = f.read()

        if obfuscation_level == 'low':
            encoded_php_code = base64.b64encode(php_code.encode()).decode()
            obfuscated_code = f"<?php eval(base64_decode('{encoded_php_code}')); ?>"
        elif obfuscation_level == 'medium':
            compressed_php_code = compress(php_code.encode())
            encoded_php_code = base64.b64encode(compressed_php_code).decode()
            obfuscated_code = f"<?php eval(gzinflate(base64_decode('{encoded_php_code}'))); ?>"
        elif obfuscation_level == 'high':
            compressed_php_code = compress(php_code.encode())
            encoded_php_code = base64.b64encode(compressed_php_code).decode()
            obfuscated_code = f"<?php eval(gzinflate(base64_decode('{encoded_php_code}'))); ?>"

            var_pattern = re.compile(r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*')
            var_names = set(var_pattern.findall(obfuscated_code))
            for var_name in var_names:
                new_var_name = f"${obfuscation_level}_{var_name[1:]}"
                obfuscated_code = obfuscated_code.replace(var_name, new_var_name)

        # Save the obfuscated code to the output directory
        output_file = os.path.join(output_directory, f"obfuscated_{os.path.basename(input_file)}")
        with open(output_file, "w") as f:
            f.write(obfuscated_code)

        print(f"{GREEN}Obfuscated file saved as {output_file}{RESET}")
        logging.info(f"Obfuscated {input_file} successfully")

    except Exception as e:
        logging.error(f"Error while obfuscating {input_file}: {e}")
        print(f"{RED}Error while obfuscating {input_file}: {e}{RESET}")

def obfuscate_file(args):
    input_file, obfuscation_level, create_backup, output_directory = args
    obfuscate_php(input_file, obfuscation_level, create_backup, output_directory)

def process_directory(directory, obfuscation_level, exclude_list, create_backup, output_directory, max_workers=4):
    total_files = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".php"):
                total_files += 1

    progress_bar = tqdm(total=total_files, desc="Obfuscating", unit="file")

    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".php"):
                input_file = os.path.join(root, file)

                if any(os.path.commonpath([input_file, exclude]) == os.path.abspath(exclude) for exclude in exclude_list):
                    logging.info(f"Skipping {input_file}: excluded")
                    continue

                file_list.append((input_file, obfuscation_level, create_backup, output_directory))

    progress_bar = tqdm(total=len(file_list), desc="Obfuscating", unit="file")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(obfuscate_file, file_list):
            progress_bar.update()

    progress_bar.close()

def interactive_mode():
    print(f"{GREEN}Welcome to the PHP Obfuscator Interactive Mode!{RESET}")
    print(f"{GREEN}Follow the prompts to obfuscate your PHP files.\n{RESET}")

    print(f"{GREEN}Choose the mode for obfuscating your PHP files:{RESET}")
    print(f"{BLUE}1: Single file{RESET}")
    print(f"{BLUE}2: Multiple files{RESET}")
    print(f"{BLUE}3: Entire project directory{RESET}")
    mode = input(f"{GREEN}Enter the mode number (1/2/3): {RESET}")

    print(f"{GREEN}\nChoose the obfuscation level:{RESET}")
    print(f"{BLUE}1: Low (Base64 encoding){RESET}")
    print(f"{BLUE}2: Medium (zlib compression + Base64 encoding){RESET}")
    print(f"{BLUE}3: High (zlib compression + Base64 encoding + simple variable renaming){RESET}")
    obfuscation_level = input(f"{GREEN}Enter the obfuscation level number (1/2/3): {RESET}")

    exclude_input = input(f"{GREEN}\nEnter a comma-separated list of files or directories to exclude (leave empty if none): {RESET}")
    exclude_list = [path.strip() for path in exclude_input.split(',') if path.strip()]

    backup_input = input(f"{GREEN}\nCreate backups of original PHP files? (y/n): {RESET}")
    create_backup = backup_input.lower() == 'y'

    output_directory = input(f"{GREEN}\nEnter the output directory path: {RESET}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if mode == '1':
        input_file = input(f"{GREEN}\nEnter the PHP file path: {RESET}")
        obfuscate_php(input_file, obfuscation_level, create_backup, output_directory)
    elif mode == '2':
        input_files = input(f"{GREEN}\nEnter a comma-separated list of PHP files to obfuscate: {RESET}")
        files = [file.strip() for file in input_files.split(',') if file.strip()]
        for file in files:
            obfuscate_php(file, obfuscation_level, create_backup, output_directory)
    elif mode == '3':
        input_directory = input(f"{GREEN}\nEnter the directory path containing PHP files: {RESET}")
        process_directory(input_directory, obfuscation_level, exclude_list, create_backup, output_directory)
    else:
        print(f"{RED}Invalid mode. Exiting...{RESET}")
        sys.exit(1)
        
def main():
    interactive = input(f"{YELLOW}Do you want to run the script in interactive mode? (y/n): {RESET}").lower()
    if interactive == 'y':
        interactive_mode()
    else:
        print(f"{GREEN}Choose the mode for obfuscating your PHP files: {RESET}")
        print(f"{BLUE}1: Single file{RESET}")
        print(f"{BLUE}2: Multiple files{RESET}")
        print(f"{BLUE}3: Entire project directory{RESET}")
        mode = input(f"{GREEN}Enter the mode number (1/2/3): {RESET}")

        print(f"{GREEN}\nSelect obfuscation level: {RESET}")
        print(f"{BLUE}1: Low (Base64 encoding){RESET}")
        print(f"{BLUE}2: Medium (zlib compression + Base64 encoding){RESET}")
        print(f"{BLUE}3: High (zlib compression + Base64 encoding + simple variable renaming){RESET}")
        obfuscation_level = input(f"{GREEN}Enter the obfuscation level number (1/2/3): {RESET}")

        output_directory = input(f"{GREEN}Enter the output directory path: {RESET}")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        level_mapping = {'1': 'low', '2': 'medium', '3': 'high'}
        if obfuscation_level not in level_mapping:
            logging.warning("Invalid obfuscation level. Choose from: 1, 2, or 3")
            print(f"{RED}Invalid obfuscation level. Choose from: 1, 2, or 3{RESET}")
            sys.exit(1)
        obfuscation_level = level_mapping[obfuscation_level]

        exclude_input = input(f"{GREEN}Enter file or directory paths to exclude (separated by a space): {RESET}")
        exclude_list = [os.path.abspath(exclude.strip()) for exclude in exclude_input.split()]

        backup_input = input(f"{GREEN}Create backups of original PHP files? (y/n): {RESET}").lower()
        create_backup = backup_input == 'y'

        if mode == '1':
            input_file = input(f"{GREEN}Enter the PHP file path: {RESET}")
            if not input_file.lower().endswith(".php") or not os.path.isfile(input_file):
                logging.warning("Invalid PHP file path")
                print(f"{RED}Invalid PHP file path{RESET}")
                sys.exit(1)
            if any(os.path.commonpath([input_file, exclude]) == os.path.abspath(exclude) for exclude in exclude_list):
                logging.info(f"Skipping {input_file}: excluded")
            else:
                obfuscate_php(input_file, obfuscation_level, create_backup)
        elif mode == '2':
            file_paths = input(f"{GREEN}Enter the PHP file paths separated by a space: {RESET}")
            files = file_paths.split()

            for input_file in files:
                if not input_file.lower().endswith(".php") or not os.path.isfile(input_file):
                    logging.warning(f"Skipping {input_file}: not a valid PHP file")
                    print(f"{RED}Skipping {input_file}: not a valid PHP file{RESET}")
                    continue
                obfuscate_php(input_file, obfuscation_level, create_backup)
        elif mode == '3':
            input_directory = input(f"{GREEN}Enter the project directory path: {RESET}")
            if not os.path.isdir(input_directory):
                logging.warning("Invalid directory path")
                print(f"{RED}Invalid directory path{RESET}")
                sys.exit(1)
            process_directory(input_directory, obfuscation_level, exclude_list, create_backup)
        else:
            logging.warning("Invalid mode. Choose from: 1, 2, or 3")
            print(f"{RED}Invalid mode. Choose from: 1, 2, or 3{RESET}")
            sys.exit(1)

if __name__ == "__main__":
    main()
