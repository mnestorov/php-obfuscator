# Changelog

### 1.0 (2023.05.07)
- Initial release.

### 1.1 (2024.09.04)
- Added `shlex.quote()` in the `obfuscate_php()` function when constructing the command to ensure that paths with spaces or special characters are handled properly. 
- Updated the YAKPRO command in `config.py` to use `os.path.expanduser` to make it dynamic and compatible with user home directories