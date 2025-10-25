"""
Terminal AI - AI Chat Assistant using Google Gemini
Author: Aidomx
Version: 1.0
"""

import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def setup_environment():
    """Setup environment and API key"""
    load_dotenv()  # Load from .env file 
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Masukkan Google Gemini API Key Anda: ").strip()
        if not api_key:
            print("❌ API Key diperlukan!")
            sys.exit(1)
    return api_key

def initialize_client(api_key):
    """Initialize Gemini client"""
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"❌ Gagal menginisialisasi client: {e}")
        sys.exit(1)

def print_welcome():
    """Print welcome message"""
    print("🤖 Terminal AI - AI Assistant")
    print("=" * 40)
    print("Ketik 'quit' untuk keluar")
    print("Ketik 'clear' untuk menghapus history")
    print("Ketik 'help' untuk bantuan")
    print("=" * 40)

def print_help():
    """Print help message"""
    print("\n📖 **Bantuan:**")
    print("  • Ketik pesan biasa untuk chat dengan AI")
    print("  • 'quit' - Keluar dari aplikasi")
    print("  • 'clear' - Hapus history percakapan")
    print("  • 'help' - Tampilkan bantuan ini")
    print("  • 'model' - Ganti model AI")
    print()

def get_available_models():
    """Return available Gemini models"""
    return {
        "1": "gemini-2.5-flash",
        "2": "gemini-2.0-flash",
        "3": "gemini-1.5-flash",
        "4": "gemini-1.5-pro",
        "5": "gemini-2.0-flash-exp"
    }

def change_model(current_model):
    """Change AI model"""
    models = get_available_models()
    print("\n🤖 **Pilih Model AI:**")
    for key, model in models.items():
        status = " ✅" if model == current_model else ""
        print(f"  {key}. {model}{status}")
    choice = input("\nPilih model (1-5) atau 'cancel': ").strip()
    if choice in models:
        new_model = models[choice]
        print(f"🔄 Model diubah ke: {new_model}")
        return new_model
    elif choice.lower() == 'cancel':
        print("❌ Pembatalan perubahan model")
        return current_model
    else:
        print("❌ Pilihan tidak valid!")
        return current_model

def chat_loop(client):
    """Main chat loop"""
    history = []
    current_model = "gemini-2.5-flash"
    print_welcome()
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            # Handle commands
            if user_input.lower() == 'quit':
                print("👋 Sampai jumpa!")
                break
            elif user_input.lower() == 'clear':
                history.clear()
                print("🗑️ History percakapan dihapus!")
                continue
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'model':
                current_model = change_model(current_model)
                continue
            elif not user_input:
                continue
            # Process AI response
            print("🤖 AI: ", end="", flush=True)
            full_response = ""
            # Prepare contents with history
            contents = history + [user_input]
            # Generate response
            for chunk in client.models.generate_content_stream(
                model=current_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            print()  # New line
            # Update history (keep last 10 exchanges to prevent too long context)
            history.append(user_input)
            history.append(full_response)
            history = history[-20:]  # Keep last 10 exchanges
        except KeyboardInterrupt:
            print("\n\n👋 Dihentikan oleh user. Sampai jumpa!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("🔄 Silakan coba lagi...")

def main():
    """Main function"""
    try:
        print("🚀 Memulai Terminal AI...")
        # Setup
        api_key = setup_environment()
        client = initialize_client(api_key)
        # Test connection
        print("🔗 Menguji koneksi ke Gemini API...")
        test_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Hello"
        )
        print("✅ Koneksi berhasil!")
        # Start chat
        chat_loop(client)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
