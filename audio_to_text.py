"""
FILE 1: audio_to_text.py
Chức năng: Đọc nội dung âm thanh từ file MP4 và lưu vào file text.txt
Cài đặt: pip install moviepy speechrecognition pydub
"""

import speech_recognition as sr
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import sys

class AudioToTextConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def extract_audio_from_video(self, video_path, audio_path="temp_audio.wav"):
        """Trích xuất âm thanh từ video MP4 thành file WAV"""
        try:
            print(f"📹 Đang đọc video: {video_path}")
            video = VideoFileClip(video_path)
            
            print("🎵 Đang trích xuất âm thanh...")
            audio = video.audio
            
            # Sửa lỗi verbose - bỏ tham số verbose và logger
            audio.write_audiofile(audio_path, codec='pcm_s16le', fps=16000)
            
            audio.close()
            video.close()
            
            print(f"✅ Đã trích xuất âm thanh thành công: {audio_path}")
            return audio_path
        except Exception as e:
            print(f"❌ Lỗi khi trích xuất âm thanh: {e}")
            return None
    
    def transcribe_audio(self, audio_path, language="vi-VN"):
        """Nhận dạng giọng nói từ file âm thanh"""
        try:
            print(f"🎤 Đang nhận dạng giọng nói (ngôn ngữ: {language})...")
            
            with sr.AudioFile(audio_path) as source:
                # Điều chỉnh nhiễu môi trường
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Ghi âm toàn bộ file
                audio_data = self.recognizer.record(source)
                
                # Nhận dạng bằng Google Speech Recognition
                text = self.recognizer.recognize_google(audio_data, language=language)
                
                print("✅ Nhận dạng thành công!")
                return text
                
        except sr.UnknownValueError:
            return "❌ Không thể nhận dạng giọng nói. Vui lòng kiểm tra chất lượng âm thanh."
        except sr.RequestError as e:
            return f"❌ Lỗi kết nối đến dịch vụ nhận dạng: {e}"
        except Exception as e:
            return f"❌ Lỗi: {e}"
    
    def save_to_text_file(self, text, output_file="text.txt"):
        """Lưu nội dung text vào file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text.upper())  # Chuyển thành chữ hoa
            print(f"✅ Đã lưu nội dung vào file: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi lưu file: {e}")
            return False
    
    def process_video(self, video_path, output_text="text.txt", language="vi-VN"):
        """Xử lý toàn bộ quá trình"""
        print("\n" + "="*60)
        print("🎬 CHUYỂN ĐỔI ÂM THANH TỪ VIDEO MP4 SANG TEXT")
        print("="*60)
        
        # Kiểm tra file video tồn tại
        if not os.path.exists(video_path):
            print(f"❌ Không tìm thấy file video: {video_path}")
            return False
        
        # Trích xuất âm thanh
        audio_file = self.extract_audio_from_video(video_path)
        if not audio_file:
            return False
        
        # Nhận dạng giọng nói
        text = self.transcribe_audio(audio_file, language)
        
        # Lưu vào file text
        success = self.save_to_text_file(text, output_text)
        
        # Xóa file âm thanh tạm
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"🗑️ Đã xóa file tạm: {audio_file}")
        
        # Hiển thị kết quả
        if success:
            print("\n" + "="*60)
            print("📝 NỘI DUNG TEXT ĐÃ LƯU:")
            print("="*60)
            print(text[:500] + "..." if len(text) > 500 else text)
            print("="*60)
            print(f"\n✨ Hoàn thành! Nội dung đã được lưu vào {output_text}")
        
        return success

def main():
    converter = AudioToTextConverter()
    
    # Nhập thông tin
    video_file = input("\n📹 Nhập đường dẫn đến file MP4: ").strip()
    
    output_file = input("📄 Nhập tên file output text (mặc định: text.txt): ").strip()
    if not output_file:
        output_file = "text.txt"
    
    print("\n🌐 Chọn ngôn ngữ:")
    print("1. Tiếng Việt (vi-VN)")
    print("2. Tiếng Anh (en-US)")
    print("3. Tiếng Trung (zh-CN)")
    
    lang_choice = input("Chọn (1/2/3): ").strip()
    language_map = {
        "1": "vi-VN",
        "2": "en-US", 
        "3": "zh-CN"
    }
    language = language_map.get(lang_choice, "vi-VN")
    
    # Xử lý
    converter.process_video(video_file, output_file, language)

if __name__ == "__main__":
    # Kiểm tra thư viện
    try:
        import moviepy
        import speech_recognition
    except ImportError as e:
        print("❌ Thiếu thư viện! Vui lòng cài đặt:")
        print("pip install moviepy speechrecognition pydub")
        sys.exit(1)
    
    main()