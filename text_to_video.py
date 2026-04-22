"""
FILE 2: text_to_video.py
Chức năng: Tạo video từ file text.txt với hiển thị từng câu (nền đen, chữ trắng)
"""

import os
import re
import sys

# ========== CẤU HÌNH IMAGEMAGICK CHO WINDOWS ==========
from moviepy.config import change_settings

# ĐƯỜNG DẪN ĐẾN IMAGEMAGICK - ĐÃ CẬP NHẬT THEO ĐƯỜNG DẪN CỦA BẠN
imagemagick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

# Kiểm tra và cấu hình
if os.path.exists(imagemagick_path):
    change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})
    print(f"✅ Đã cấu hình ImageMagick thành công!")
    print(f"   Đường dẫn: {imagemagick_path}")
else:
    print(f"❌ Không tìm thấy ImageMagick tại: {imagemagick_path}")
    print("📌 Vui lòng kiểm tra lại đường dẫn!")
    print("📌 Hoặc cài đặt ImageMagick từ: https://imagemagick.org/script/download.php")
# =====================================================

# Import moviepy sau khi đã cấu hình
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips

class TextToVideoCreator:
    def __init__(self, text_file="text.txt", video_size=(1920, 1080)):
        self.text_file = text_file
        self.video_size = video_size
        self.sentences = []
        
    def read_and_split_sentences(self):
        """Đọc file text và tách thành các câu"""
        try:
            print(f"\n📖 Đang đọc file: {self.text_file}")
            
            with open(self.text_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            if not content:
                print("❌ File text rỗng!")
                return False
            
            # Tách câu dựa trên dấu câu
            sentences = re.split(r'([.!?;:]+)', content)
            
            self.sentences = []
            for i in range(0, len(sentences) - 1, 2):
                if i + 1 < len(sentences):
                    sentence = sentences[i] + sentences[i + 1]
                    if sentence.strip():
                        self.sentences.append(sentence.strip())
            
            if len(sentences) % 2 == 1 and sentences[-1].strip():
                self.sentences.append(sentences[-1].strip())
            
            if not self.sentences:
                temp_sentences = re.split(r'[.!?]+', content)
                self.sentences = [s.strip() + '.' for s in temp_sentences if s.strip()]
            
            print(f"✅ Đã đọc {len(self.sentences)} câu")
            
            for i, sent in enumerate(self.sentences[:5]):
                preview = sent[:80] + "..." if len(sent) > 80 else sent
                print(f"   Câu {i+1}: {preview}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file: {self.text_file}")
            return False
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return False
    
    def calculate_sentence_duration(self, sentence, base_duration=2.0, words_per_second=2.5):
        """Tính thời gian hiển thị cho mỗi câu"""
        word_count = len(sentence.split())
        duration = base_duration + (word_count / words_per_second)
        duration = max(2.0, min(15.0, duration))
        return duration
    
    def wrap_text(self, text, max_width=35):
        """Wrap text để hiển thị nhiều dòng"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def create_video_basic(self, output_video="output_sentences.mp4", fontsize=80, font="Arial"):
        """Chế độ 1: Hiển thị toàn bộ câu"""
        if not self.sentences:
            print("❌ Không có câu nào để hiển thị!")
            return False
        
        print("\n🎬 Chế độ 1: Hiển thị toàn bộ câu")
        print("-" * 40)
        
        # Tính thời gian
        sentence_durations = []
        total_duration = 0
        
        for i, sentence in enumerate(self.sentences):
            duration = self.calculate_sentence_duration(sentence)
            sentence_durations.append(duration)
            total_duration += duration
            word_count = len(sentence.split())
            print(f"Câu {i+1}: {word_count} từ - {duration:.2f} giây")
        
        print(f"\n📊 Tổng thời lượng: {total_duration:.2f} giây")
        
        # Tạo nền đen
        print("🎨 Đang tạo nền video...")
        background = ColorClip(size=self.video_size, color=(0, 0, 0), duration=total_duration)
        
        # Tạo clip cho từng câu
        clips = []
        current_time = 0
        
        for i, (sentence, duration) in enumerate(zip(self.sentences, sentence_durations)):
            display_text = self.wrap_text(sentence, max_width=35)
            
            # Tạo TextClip
            txt_clip = TextClip(display_text, 
                               fontsize=fontsize, 
                               color='white',
                               font=font,
                               stroke_color='black',
                               stroke_width=2,
                               method='caption',
                               align='center',
                               size=self.video_size)
            
            txt_clip = txt_clip.set_position('center')
            txt_clip = txt_clip.set_start(current_time).set_duration(duration)
            
            # Thêm hiệu ứng mờ dần
            try:
                txt_clip = txt_clip.crossfadein(0.3).crossfadeout(0.5)
            except:
                pass
            
            clips.append(txt_clip)
            current_time += duration
            
            progress = (i + 1) / len(self.sentences) * 100
            print(f"🔄 Đã xử lý: {progress:.1f}% - Câu {i+1}/{len(self.sentences)}")
        
        # Ghép video
        print("🎬 Đang render video...")
        final_video = CompositeVideoClip([background] + clips)
        
        # Xuất video
        try:
            final_video.write_videofile(output_video, 
                                       fps=24,
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile='temp-audio.m4a',
                                       remove_temp=True)
            
            print(f"\n✅ Video đã được tạo thành công!")
            print(f"📁 File: {output_video}")
            print(f"⏱️ Thời lượng: {total_duration:.2f} giây")
            print(f"🎯 Số câu: {len(self.sentences)}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo video: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            final_video.close()
            for clip in clips:
                clip.close()
            background.close()
    
    def create_video_with_typing_effect(self, output_video="output_typing.mp4", 
                                        fontsize=80, font="Arial"):
        """Chế độ 2: Hiệu ứng gõ chữ"""
        if not self.sentences:
            print("❌ Không có câu nào để hiển thị!")
            return False
        
        print("\n🎬 Chế độ 2: Hiệu ứng gõ chữ")
        print("-" * 40)
        
        all_clips = []
        
        for i, sentence in enumerate(self.sentences):
            words = sentence.split()
            total_duration = self.calculate_sentence_duration(sentence)
            word_duration = total_duration / len(words) if words else 0.2
            
            print(f"Câu {i+1}: {len(words)} từ - {total_duration:.2f} giây")
            
            sentence_clips = []
            current_text = ""
            
            for j, word in enumerate(words):
                if j == 0:
                    current_text = word
                else:
                    current_text += " " + word
                
                display_text = self.wrap_text(current_text, max_width=35)
                
                txt_clip = TextClip(display_text,
                                   fontsize=fontsize,
                                   color='white',
                                   font=font,
                                   stroke_color='black',
                                   stroke_width=2,
                                   method='caption',
                                   align='center',
                                   size=self.video_size)
                
                txt_clip = txt_clip.set_position('center')
                txt_clip = txt_clip.set_duration(word_duration)
                sentence_clips.append(txt_clip)
            
            sentence_sequence = concatenate_videoclips(sentence_clips, method="compose")
            sentence_sequence = sentence_sequence.set_duration(total_duration)
            all_clips.append(sentence_sequence)
            
            progress = (i + 1) / len(self.sentences) * 100
            print(f"🔄 Tiến độ: {progress:.1f}%")
        
        print("🎬 Đang render video với hiệu ứng gõ chữ...")
        final_sequence = concatenate_videoclips(all_clips, method="compose")
        
        background = ColorClip(size=self.video_size, color=(0, 0, 0), 
                              duration=final_sequence.duration)
        
        final_video = CompositeVideoClip([background, final_sequence.set_position('center')])
        
        try:
            final_video.write_videofile(output_video,
                                       fps=24,
                                       codec='libx264',
                                       audio_codec='aac',
                                       temp_audiofile='temp-audio.m4a',
                                       remove_temp=True)
            
            print(f"\n✅ Video với hiệu ứng gõ chữ đã được tạo!")
            print(f"📁 File: {output_video}")
            print(f"⏱️ Thời lượng: {final_sequence.duration:.2f} giây")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False
        finally:
            final_video.close()
            background.close()

def main():
    print("\n" + "="*60)
    print("🎬 TẠO VIDEO TỪ TEXT VỚI HIỂN THỊ TỪNG CÂU")
    print("="*60)
    
    text_file = input("\n📄 Nhập tên file text (mặc định: text.txt): ").strip()
    if not text_file:
        text_file = "text.txt"
    
    if not os.path.exists(text_file):
        print(f"❌ Không tìm thấy file {text_file}")
        return
    
    output_file = input("🎥 Nhập tên file output (mặc định: output_video.mp4): ").strip()
    if not output_file:
        output_file = "output_video.mp4"
    
    print("\n🎨 Chọn chế độ hiển thị:")
    print("1. Hiển thị toàn bộ câu")
    print("2. Hiệu ứng gõ chữ")
    
    mode = input("Chọn (1 hoặc 2): ").strip()
    
    try:
        fontsize = int(input("\n🔤 Cỡ chữ (mặc định: 80): ").strip() or "80")
    except ValueError:
        fontsize = 80
    
    try:
        width = int(input("📐 Chiều rộng video (mặc định: 1920): ").strip() or "1920")
        height = int(input("📏 Chiều cao video (mặc định: 1080): ").strip() or "1080")
    except ValueError:
        width, height = 1920, 1080
    
    creator = TextToVideoCreator(text_file, (width, height))
    
    if not creator.read_and_split_sentences():
        return
    
    if mode == "2":
        creator.create_video_with_typing_effect(output_file, fontsize)
    else:
        creator.create_video_basic(output_file, fontsize)
    
    print("\n✨ Hoàn thành!")

if __name__ == "__main__":
    main()