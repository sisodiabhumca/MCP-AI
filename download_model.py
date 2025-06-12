from huggingface_hub import hf_hub_download
import os

def download_model(model_name="llama-2-7b-chat.Q4_K_M.gguf"):
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Download the model
    model_path = hf_hub_download(
        repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
        filename=model_name,
        local_dir="models",
        # Temporarily disable SSL verification for troubleshooting
        # WARNING: Not recommended for production environments
        force_download=True, # Force download to ensure it retries
        resume_download=False, # Start fresh
        # Add 'config_kwargs': {'trust_remote_code': True} if `allow_unsafe_deserialization` or similar is needed
        # For SSL issues, direct SSL parameter is usually in requests/urllib3
        # For hf_hub_download, a common workaround for persistent SSL is to set environment var
        # or use a custom http_client/session, but given the error, force_download + resume_download
        # combined with previous cert steps is the way. If still fails, manual download is option.
    )
    print(f"Model downloaded to: {model_path}")
    return model_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="llama-2-7b-chat.Q4_K_M.gguf", help="Name of the GGUF model file to download")
    args = parser.parse_args()
    download_model(args.model_name) 