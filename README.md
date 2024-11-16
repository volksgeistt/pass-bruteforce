# UnLockr
A high-performance, multi-threaded password recovery tool for encrypted files. UnLockr supports multiple file formats and provides a user-friendly command-line interface with real-time progress monitoring.
![image](https://github.com/user-attachments/assets/74d34f9b-da30-433e-9cde-28ec090284f4)
# Features
- Multi-threaded password recovery using process pools
- Real-time progress monitoring and speed statistics
- Support for multiple file formats:
   - ZIP archives (.zip)
   - PDF documents (.pdf)
   - Microsoft Office files (.docx, .xlsx, .pptx, .doc, .xls, .ppt)
   - RAR archives (.rar)
   - 7-Zip archives (.7z)
   - OpenDocument files (.odt, .ods, .odp)
# Installation
1. Clone the repository:
```bash
git clone https://github.com/volksgeistt/unlockr.git
cd unlockr
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
*Packages Required:* `PyPDF2, msoffcrypto-tool, rarfile, py7zr, pyfiglet, colorama`<br>
3. Run the script:
```bash
python unlockr.py
```
# Example
```bash
$ python unlockr.py

Enter path to encrypted file: /path/to/encrypted.zip
Enter path to wordlist file: /path/to/wordlist.txt

Starting password recovery for: encrypted.zip
File type: ZIP
Using wordlist: wordlist.txt
Using processes: 7

Progress: 45.2% | Speed: 15234.56 passwords/sec | Attempts: 1,234,567
```
# Disclaimer
This tool is for educational purposes and legitimate password recovery only. The author is not responsible for any misuse or damage caused by this program. Always ensure you have explicit permission to attempt password recovery on any files.



