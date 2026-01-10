
import os
from huggingface_hub import HfApi, create_repo
from dotenv import load_dotenv

load_dotenv()

def deploy():
    print("🚀 Deploying to Hugging Face Spaces...")
    
    # 1. Get Token
    token = os.getenv("HUGGINGFACE_API_KEY")
    if not token:
        print("❌ Error: HUGGINGFACE_API_KEY not found in environment.")
        print("Please set it in your .env file or environment variables.")
        return

    api = HfApi(token=token)
    
    # 2. Define Space Name
    # Extract user name from token usually, but here we ask or generate
    user = api.whoami()["name"]
    repo_name = "ai-call-analyzer-gradio"
    repo_id = f"{user}/{repo_name}"
    
    print(f"Target Space: {repo_id}")
    
    # 3. Create Repo (if not exists)
    try:
        url = create_repo(
            repo_id=repo_id,
            token=token,
            repo_type="space",
            space_sdk="gradio",
            exist_ok=True,
            private=False 
        )
        print(f"✅ Repo exists/created at: {url}")
    except Exception as e:
        print(f"❌ Error creating repo: {e}")
        return

    # 4. Upload Files
    # We upload only necessary files
    files_to_upload = [
        "app_gradio.py",
        "requirements.txt",
        "packages.txt",
        "README.md",
        ".env" # CAUTION: Usually we don't upload .env, but for this specific "deploy for me" request, 
               # we might need to set secrets. BUT uploading .env to public space is BAD.
               # Better approach: Set secret programmatically.
    ]
    
    print("📤 Uploading files...")
    try:
        for file in files_to_upload:
            if file == ".env":
                continue # Skip .env file upload for security
                
            if os.path.exists(file):
                print(f"  - Uploading {file}...")
                api.upload_file(
                    path_or_fileobj=file,
                    path_in_repo=file,
                    repo_id=repo_id,
                    repo_type="space"
                )
    except Exception as e:
         print(f"❌ Error uploading files: {e}")
         
    # 5. Set Secret
    print("🔑 Setting Secrets...")
    try:
        api.add_space_secret(
            repo_id=repo_id,
            key="HUGGINGFACE_API_KEY",
            value=token
        )
        print("✅ Secret HUGGINGFACE_API_KEY set.")
    except Exception as e:
        print(f"⚠️ Could not set secret (might already exist or permission issue): {e}")

    print("\n🎉 Deployment Triggered!")
    print(f"👉 View your app here: https://huggingface.co/spaces/{repo_id}")

if __name__ == "__main__":
    deploy()
