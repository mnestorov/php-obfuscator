import sys
import os
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import log_filename, YELLOW, BLUE, GREEN, RED, RESET, YAKPRO
from subprocess import call

# Configure logging
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Configuration for YakPro-Po obfuscation options
OB_OPTIONS = {
    "variables": "--obfuscate-variables",
    "functions": "--obfuscate-functions",
    "classes": "--obfuscate-classes"
}

def get_obfuscation_options():
    """Prompt user for obfuscation preferences."""
    print(f"{GREEN}Choose the obfuscation options:{RESET}")
    options = []

    for key, desc in OB_OPTIONS.items():
        choice = input(f"{GREEN}Obfuscate {key}? (y/n): {RESET}").lower()
        if choice == 'y':
            options.append(desc)

    return options

def obfuscate_php(input_file, obfuscation_options, create_backup, output_directory):
    if create_backup:
        backup_file = f"{os.path.splitext(input_file)[0]}_backup.php"
        shutil.copy2(input_file, backup_file)
        logging.info(f"Created backup: {backup_file}")

    try:
        # Create the directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        output_file = os.path.join(output_directory, f"obfuscated_{os.path.basename(input_file)}")
        logging.info(f"Obfuscating {input_file}")

        command = [YAKPRO] + obfuscation_options + [output_file, input_file]
        call(command)

        print(f"{GREEN}Obfuscated file saved as {output_file}{RESET}")
        logging.info(f"Obfuscated {input_file} successfully")

    except Exception as e:
        logging.error(f"Error while obfuscating {input_file}: {e}")
        print(f"{RED}Error while obfuscating {input_file}: {e}{RESET}")

def obfuscate_file(args):
    input_file, obfuscation_options, create_backup, output_directory = args
    obfuscate_php(input_file, obfuscation_options, create_backup, output_directory)

def process_directory(directory, obfuscation_options, exclude_list, create_backup, output_directory, max_workers=4):
    total_files = sum(len(files) for _, _, files in os.walk(directory) if any(f.lower().endswith(".php") for f in files))

    progress_bar = tqdm(total=total_files, desc="Obfuscating", unit="file")

    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".php"):
                input_file = os.path.join(root, file)

                if any(os.path.commonpath([input_file, exclude]) == os.path.abspath(exclude) for exclude in exclude_list):
                    logging.info(f"Skipping {input_file}: excluded")
                    continue

                # Calculate the target directory in the output structure
                relative_path = os.path.relpath(root, directory)
                target_directory = os.path.join(output_directory, relative_path)

                file_list.append((input_file, obfuscation_options, create_backup, target_directory))

    progress_bar = tqdm(total=len(file_list), desc="Obfuscating", unit="file")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in executor.map(obfuscate_file, file_list):
            progress_bar.update()

    progress_bar.close()

def validate_mode_input(mode):
    try:
        mode = int(mode)
        if mode not in [1, 2, 3]:
            raise ValueError
        return mode
    except ValueError:
        logging.error("Invalid mode input. Please enter 1, 2, or 3.")
        print(f"{RED}Invalid mode. Choose from: 1, 2, or 3{RESET}")
        sys.exit(1)

def validate_directory_input(directory_path):
    if not os.path.isdir(directory_path):
        logging.error(f"Invalid directory path: {directory_path}")
        print(f"{RED}Invalid directory path{RESET}")
        sys.exit(1)

def main():
    print(f"{YELLOW}Welcome to the PHP Obfuscator!{RESET}")
    print(f"{YELLOW}Follow the prompts to obfuscate your PHP files.\n{RESET}")

    print(f"{GREEN}Choose the mode for obfuscating your PHP files:{RESET}")
    print(f"{BLUE}1: Single file{RESET}")
    print(f"{BLUE}2: Multiple files{RESET}")
    print(f"{BLUE}3: Entire project directory{RESET}")
    mode = validate_mode_input(input(f"{GREEN}Enter the mode number (1/2/3): {RESET}"))

    output_directory = input(f"{GREEN}Enter the output directory path: {RESET}")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    exclude_input = input(f"{GREEN}Enter file or directory paths to exclude (separated by a space) (you can skip this step): {RESET}")
    exclude_list = [os.path.abspath(exclude.strip()) for exclude in exclude_input.split()]

    create_backup = input(f"{GREEN}Create backups of original PHP files? (y/n): {RESET}").lower() == 'y'

    obfuscation_options = get_obfuscation_options()

    if mode == 1:
        input_file = input(f"{GREEN}Enter the PHP file path: {RESET}")
        if not input_file.lower().endswith(".php") or not os.path.isfile(input_file):
            logging.warning("Invalid PHP file path")
            print(f"{RED}Invalid PHP file path{RESET}")
            sys.exit(1)
        if any(os.path.commonpath([input_file, exclude]) == os.path.abspath(exclude) for exclude in exclude_list):
            logging.info(f"Skipping {input_file}: excluded")
        else:
            obfuscate_php(input_file, obfuscation_options, create_backup, output_directory)
    elif mode == 2:
        file_paths = input(f"{GREEN}Enter the PHP file paths separated by a space: {RESET}")
        files = file_paths.split()

        for input_file in files:
            if not input_file.lower().endswith(".php") or not os.path.isfile(input_file):
                logging.warning(f"Skipping {input_file}: not a valid PHP file")
                print(f"{RED}Skipping {input_file}: not a valid PHP file{RESET}")
                continue
            obfuscate_php(input_file, obfuscation_options, create_backup, output_directory)
    elif mode == 3:
        input_directory = input(f"{GREEN}Enter the project directory path: {RESET}")
        validate_directory_input(input_directory)
        process_directory(input_directory, obfuscation_options, exclude_list, create_backup, output_directory)
    else:
        logging.warning("Invalid mode. Choose from: 1, 2, or 3")
        print(f"{RED}Invalid mode. Choose from: 1, 2, or 3{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
