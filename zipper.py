import os
import zipfile
import shutil

def zip_folder(folder_path, output_path):
    if not os.path.exists(folder_path):
        print(f"[zipper] Folder not found: {folder_path}")
        return

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        print(f"[zipper] Successfully zipped '{folder_path}' to '{output_path}'")
    except Exception as e:
        print(f"[zipper] Failed to zip: {e}")

def unzip_file(zip_path, extract_to):
    if not os.path.exists(zip_path):
        print(f"[zipper] ZIP file not found: {zip_path}")
        return

    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_to)
        print(f"[zipper] Successfully unzipped to '{extract_to}'")
    except Exception as e:
        print(f"[zipper] Failed to unzip: {e}")

def run(args, commands):
    if len(args) < 1:
        print("Usage:")
        print("  zipper zip <folder_path> <output.zip>")
        print("  zipper unzip <file.zip> <destination>")
        return

    mode = args[0]

    if mode == "zip":
        if len(args) != 3:
            print("[zipper] Usage: zipper zip <folder_path> <output.zip>")
            return
        folder_path = args[1]
        output_path = args[2]
        zip_folder(folder_path, output_path)

    elif mode == "unzip":
        if len(args) != 3:
            print("[zipper] Usage: zipper unzip <file.zip> <destination_folder>")
            return
        zip_path = args[1]
        extract_to = args[2]
        unzip_file(zip_path, extract_to)

    else:
        print(f"[zipper] Unknown subcommand: {mode}")
        print("[zipper] Use 'zipper zip' or 'zipper unzip' for operations.")