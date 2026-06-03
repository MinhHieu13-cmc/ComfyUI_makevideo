import os
import sys
import urllib.request

def download_file(url, dest_path):
    print(f"Starting download: {url} -> {dest_path}")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    if os.path.exists(dest_path):
        print(f"File already exists at {dest_path}. Skipping.")
        return

    temp_dest = dest_path + ".tmp"
    
    try:
        def report_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = downloaded * 100 / total_size
                sys.stdout.write(f"\rDownloading... {percent:.2f}% ({downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB)")
                sys.stdout.flush()
            else:
                sys.stdout.write(f"\rDownloading... {downloaded / (1024*1024):.1f} MB")
                sys.stdout.flush()
                
        urllib.request.urlretrieve(url, temp_dest, reporthook=report_hook)
        print("\nDownload finished.")
        os.rename(temp_dest, dest_path)
        print(f"Successfully saved to {dest_path}\n")
    except Exception as e:
        print(f"\nError downloading {url}: {e}")
        if os.path.exists(temp_dest):
            os.remove(temp_dest)
        sys.exit(1)

def main():
    models_to_download = [
        {
            "url": "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/vae/wan2.2_vae.safetensors",
            "dest": os.path.join("models", "vae", "wan2.2_vae.safetensors")
        },
        {
            "url": "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors",
            "dest": os.path.join("models", "diffusion_models", "wan2.2_ti2v_5B_fp16.safetensors")
        }
    ]
    
    print("Starting download of Wan 2.2 5B models for ComfyUI...")
    for item in models_to_download:
        download_file(item["url"], item["dest"])
    print("All downloads completed successfully!")

if __name__ == "__main__":
    main()
