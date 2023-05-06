# PHP Obfuscator

## Overview

PHP Obfuscator is a command-line tool build with Python to obfuscate PHP source code files using [YAK Pro]((https://github.com/pk-fr/yakpro-po)) and [PHP-Parser](https://github.com/nikic/PHP-Parser/tree/4.x/) php libraries. 

The tool aims to protect the intellectual property of your PHP project by making it more difficult for others to understand or reverse-engineer your code. 

The tool can be used to obfuscate **single files**, **multiple files**, or an **entire project directory**.

## Requirements

- Python 3.6+
- PHP-Parser (PHP library)
- YAK Pro - Php Obfuscator (PHP library)

## Installation

1. Clone the repository

```
git clone https://github.com/your-github-repo/php-obfuscator.git
```

2. Change to the project directory

```
cd php-obfuscator
```

3. Install YAK Pro - Php Obfuscator

You need to install this in to the project directory **_php-obfuscator_**

```
git clone https://github.com/pk-fr/yakpro-po.git
```

After that, you need to configure the package from `yakpro-po.cnf` in to the **_php-obfuscator > yakpro-po_** folder.

**Recommended settings for the YAK Pro configuration:**

```php
// Allowed modes are: 'PREFER_PHP7', 'PREFER_PHP5', 'ONLY_PHP7', 'ONLY_PHP5'
$conf->parser_mode = 'PREFER_PHP7'; 

$conf->obfuscate_constant_name = false;         
$conf->obfuscate_variable_name = false;        
$conf->obfuscate_function_name = false;        
$conf->obfuscate_class_name = false;         
$conf->obfuscate_interface_name = false;         
$conf->obfuscate_trait_name = false;         
$conf->obfuscate_class_constant_name = false;        
$conf->obfuscate_property_name = false;        
$conf->obfuscate_method_name = false;         
$conf->obfuscate_namespace_name = false;         
$conf->obfuscate_label_name = false;    

// User comment to insert inside each obfuscated file
$conf->user_comment = false;         
```     

4. Install PHP-Parser

You need to install this in to the **yakpro-po** directory in to the project directory **_php-obfuscator > yakpro-po_**

```
git clone https://github.com/nikic/PHP-Parser.git
```
5. Install the required Python packages

**From the project directory, you need to run this command:**

```
pip install -r requirements.txt
```

## Usage

1. Ensure you are in the project directory.
2. Run the script

```
python main.py
```

or

```
bash start.sh
```

**Note:** Don't forget to change the path to the script in to the `start.sh` bash file.

3. Follow the prompts to configure the obfuscation settings, including:
    - Mode (single file, multiple files, or entire project directory)
    - Output directory path
    - File or directory paths to exclude
    - Whether to create backups of original PHP files

4. After the obfuscation process is completed, you can find the obfuscated files in the specified output directory.

## Used Libraries

### Python

- **os**, **sys**, **shutil**, and **re** - standard Python libraries for working with the file system and regular expressions
- **logging** - standard Python library for logging
- **concurrent.futures** - standard Python library for parallel processing
- **tqdm** - external library for progress bars

### PHP

- [YAK Pro - a PHP library for obfuscating PHP code](https://github.com/pk-fr/yakpro-po)
- [PHP-Parser - a PHP library to parse and traverse PHP code](https://github.com/nikic/PHP-Parser/tree/4.x/)

## Troubleshooting

If you encounter issues after obfuscating your PHP project, you may need to revert your files to the original (non-obfuscated) versions and reevaluate your obfuscation strategy. Always keep backups of your original code before applying obfuscation, as it can be difficult or impossible to reverse the process and recover the original code.

## License

This project is released under the MIT License.