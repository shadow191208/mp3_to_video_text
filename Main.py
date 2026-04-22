"""
FILE: Main.py
Chức năng: Giao diện chính cho phép chọn chức năng và file
Cài đặt: pip install tkinter (đã có sẵn trong Python)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import sys
import os
import threading
from datetime import datetime
import traceback
import locale

# Thiết lập encoding cho output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
        sys.stderr.reconfigure(encoding='utf-8', errors='ignore')
    except:
        pass

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Text Converter - Tool xử lý video và text")
        self.root.geometry("850x750")
        self.root.resizable(True, True)
        
        # Biến lưu trữ
        self.input_file_path = tk.StringVar()
        self.output_folder_path = tk.StringVar(value=os.getcwd())  # Mặc định là thư mục hiện tại
        self.output_text_name = tk.StringVar(value="text")
        self.output_video_name = tk.StringVar(value="output_video")
        self.selected_mode = tk.StringVar(value="1")
        self.language = tk.StringVar(value="vi-VN")
        self.video_mode = tk.StringVar(value="1")
        self.font_size = tk.IntVar(value=80)
        self.video_width = tk.IntVar(value=1920)
        self.video_height = tk.IntVar(value=1080)
        
        # Màu sắc
        self.bg_color = "#2c3e50"
        self.fg_color = "#ecf0f1"
        self.button_color = "#3498db"
        self.button_hover = "#2980b9"
        self.success_color = "#27ae60"
        self.error_color = "#e74c3c"
        
        # Thiết lập giao diện
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Tiêu đề
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🎬 VIDEO TEXT CONVERTER 🎬", 
                               font=("Arial", 20, "bold"),
                               fg=self.button_color)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Chuyển đổi Video ↔ Text một cách dễ dàng",
                                 font=("Arial", 10),
                                 fg=self.fg_color)
        subtitle_label.pack()
        
        # Khung chọn chức năng
        mode_frame = ttk.LabelFrame(main_frame, text=" Chọn chức năng ", padding="10")
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="1️⃣ Chuyển Video → Text (Âm thanh sang chữ)", 
                       variable=self.selected_mode, value="1").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="2️⃣ Chuyển Text → Video (Tạo video từ chữ)", 
                       variable=self.selected_mode, value="2").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Khung chọn file
        file_frame = ttk.LabelFrame(main_frame, text=" Chọn file đầu vào ", padding="10")
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Đường dẫn file
        path_frame = ttk.Frame(file_frame)
        path_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        ttk.Label(path_frame, text="Đường dẫn file:").grid(row=0, column=0, sticky=tk.W)
        
        self.file_entry = ttk.Entry(path_frame, textvariable=self.input_file_path, width=50)
        self.file_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(path_frame, text="📂 Chọn file", command=self.select_file).grid(row=1, column=1)
        
        # Thông tin file
        self.file_info_label = ttk.Label(file_frame, text="", foreground="gray")
        self.file_info_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Khung chọn thư mục đích
        output_folder_frame = ttk.LabelFrame(main_frame, text=" Chọn thư mục lưu kết quả ", padding="10")
        output_folder_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        folder_path_frame = ttk.Frame(output_folder_frame)
        folder_path_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        folder_path_frame.columnconfigure(0, weight=1)
        
        ttk.Label(folder_path_frame, text="Thư mục đích:").grid(row=0, column=0, sticky=tk.W)
        
        self.folder_entry = ttk.Entry(folder_path_frame, textvariable=self.output_folder_path, width=50)
        self.folder_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_path_frame, text="📁 Chọn thư mục", command=self.select_output_folder).grid(row=1, column=1)
        
        # Hiển thị thông tin thư mục
        self.folder_info_label = ttk.Label(output_folder_frame, text="", foreground="gray")
        self.folder_info_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.update_folder_info()
        
        # Khung tên file output
        name_frame = ttk.Frame(output_folder_frame)
        name_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        name_frame.columnconfigure(1, weight=1)
        
        ttk.Label(name_frame, text="Tên file text (không đuôi):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(name_frame, textvariable=self.output_text_name, width=20).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(name_frame, text=".txt", foreground="gray").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(name_frame, text="Tên file video (không đuôi):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        ttk.Entry(name_frame, textvariable=self.output_video_name, width=20).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        ttk.Label(name_frame, text=".mp4", foreground="gray").grid(row=1, column=2, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # Khung tùy chỉnh (hiển thị theo mode)
        self.custom_frame = ttk.LabelFrame(main_frame, text=" Tùy chỉnh ", padding="10")
        self.custom_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Frame cho các tùy chỉnh theo mode
        self.mode1_frame = ttk.Frame(self.custom_frame)
        self.mode2_frame = ttk.Frame(self.custom_frame)
        
        # Tùy chỉnh cho Mode 1 (Video → Text)
        ttk.Label(self.mode1_frame, text="Ngôn ngữ nhận dạng:").grid(row=0, column=0, sticky=tk.W, pady=5)
        lang_combo = ttk.Combobox(self.mode1_frame, textvariable=self.language, 
                                  values=["vi-VN (Tiếng Việt)", "en-US (Tiếng Anh)", "zh-CN (Tiếng Trung)"],
                                  state="readonly", width=30)
        lang_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        lang_combo.current(0)
        
        # Tùy chỉnh cho Mode 2 (Text → Video)
        row = 0
        ttk.Label(self.mode2_frame, text="Chế độ hiển thị:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(self.mode2_frame, text="Hiển thị toàn bộ câu", 
                       variable=self.video_mode, value="1").grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Radiobutton(self.mode2_frame, text="Hiệu ứng gõ chữ", 
                       variable=self.video_mode, value="2").grid(row=row, column=2, sticky=tk.W, padx=(10, 0))
        
        row += 1
        ttk.Label(self.mode2_frame, text="Cỡ chữ:").grid(row=row, column=0, sticky=tk.W, pady=5)
        font_spinbox = ttk.Spinbox(self.mode2_frame, from_=20, to=200, textvariable=self.font_size, width=10)
        font_spinbox.grid(row=row, column=1, sticky=tk.W, padx=(10, 0))
        
        row += 1
        ttk.Label(self.mode2_frame, text="Kích thước video:").grid(row=row, column=0, sticky=tk.W, pady=5)
        size_frame = ttk.Frame(self.mode2_frame)
        size_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, padx=(10, 0))
        ttk.Label(size_frame, text="Width:").pack(side=tk.LEFT)
        ttk.Spinbox(size_frame, from_=640, to=3840, textvariable=self.video_width, width=8).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(size_frame, text="Height:").pack(side=tk.LEFT)
        ttk.Spinbox(size_frame, from_=480, to=2160, textvariable=self.video_height, width=8).pack(side=tk.LEFT)
        
        # Mặc định hiển thị mode1
        self.mode1_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cập nhật giao diện khi đổi mode
        self.selected_mode.trace('w', self.on_mode_change)
        
        # Khung xử lý
        process_frame = ttk.LabelFrame(main_frame, text=" Xử lý ", padding="10")
        process_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.process_button = ttk.Button(process_frame, text="▶ BẮT ĐẦU XỬ LÝ", command=self.start_processing)
        self.process_button.pack()
        
        # Khung log
        log_frame = ttk.LabelFrame(main_frame, text=" Log xử lý ", padding="10")
        log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=70, 
                                                   bg="black", fg="white",
                                                   font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Thanh progress
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Nút clear log
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="🗑 Xóa log", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Lưu log", command=self.save_log).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.rowconfigure(6, weight=1)
        
        # Log khởi tạo
        self.log("✅ Ứng dụng đã khởi động thành công!")
        self.log(f"📁 Thư mục lưu mặc định: {self.output_folder_path.get()}")
        self.log("💡 Hướng dẫn: Chọn chức năng -> Chọn file -> Tùy chỉnh -> Bắt đầu xử lý")
        
        # Kiểm tra thư viện
        self.check_libraries()
    
    def update_folder_info(self):
        """Cập nhật thông tin thư mục"""
        folder = self.output_folder_path.get()
        if os.path.exists(folder):
            # Kiểm tra quyền ghi
            try:
                test_file = os.path.join(folder, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                self.folder_info_label.config(text=f"✅ Thư mục hợp lệ - Có quyền ghi", foreground="green")
            except:
                self.folder_info_label.config(text=f"⚠️ Thư mục không có quyền ghi!", foreground="red")
        else:
            self.folder_info_label.config(text=f"❌ Thư mục không tồn tại!", foreground="red")
    
    def select_output_folder(self):
        """Chọn thư mục đích"""
        folder = filedialog.askdirectory(title="Chọn thư mục lưu kết quả", initialdir=self.output_folder_path.get())
        if folder:
            self.output_folder_path.set(folder)
            self.update_folder_info()
            self.log(f"📁 Đã chọn thư mục lưu: {folder}")
    
    def check_libraries(self):
        """Kiểm tra các thư viện cần thiết"""
        self.log("\n🔍 Đang kiểm tra thư viện...")
        
        # Kiểm tra moviepy
        try:
            import importlib
            importlib.import_module('moviepy')
            self.log("✅ moviepy: Đã cài đặt")
        except ImportError:
            self.log("❌ moviepy: CHƯA CÀI ĐẶT - Vui lòng chạy: pip install moviepy", is_error=True)
        
        # Kiểm tra speech_recognition
        try:
            import importlib
            importlib.import_module('speech_recognition')
            self.log("✅ speech_recognition: Đã cài đặt")
        except ImportError:
            self.log("❌ speech_recognition: CHƯA CÀI ĐẶT - Vui lòng chạy: pip install speechrecognition", is_error=True)
        
        self.log("")
        
    def on_mode_change(self, *args):
        """Xử lý khi thay đổi mode"""
        if self.selected_mode.get() == "1":
            self.mode2_frame.pack_forget()
            self.mode1_frame.pack(fill=tk.BOTH, expand=True)
            self.log("📹 Chế độ: Video → Text (Chuyển âm thanh thành chữ)")
        else:
            self.mode1_frame.pack_forget()
            self.mode2_frame.pack(fill=tk.BOTH, expand=True)
            self.log("📝 Chế độ: Text → Video (Tạo video từ nội dung text)")
    
    def select_file(self):
        """Mở dialog chọn file"""
        if self.selected_mode.get() == "1":
            filetypes = [("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Chọn file video", filetypes=filetypes)
            if filename:
                self.input_file_path.set(filename)
                self.update_file_info()
                self.log(f"📁 Đã chọn file video: {os.path.basename(filename)}")
        else:
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Chọn file text", filetypes=filetypes)
            if filename:
                self.input_file_path.set(filename)
                self.update_file_info()
                self.log(f"📁 Đã chọn file text: {os.path.basename(filename)}")
    
    def update_file_info(self):
        """Cập nhật thông tin file"""
        filepath = self.input_file_path.get()
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            if size < 1024:
                size_str = f"{size} bytes"
            elif size < 1024 * 1024:
                size_str = f"{size/1024:.2f} KB"
            else:
                size_str = f"{size/(1024*1024):.2f} MB"
            
            self.file_info_label.config(text=f"✅ File: {os.path.basename(filepath)} - Kích thước: {size_str}")
        else:
            self.file_info_label.config(text="")
    
    def log(self, message, is_error=False):
        """Thêm message vào log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if is_error:
            self.log_text.insert(tk.END, f"[{timestamp}] ❌ {message}\n", "error")
            self.log_text.tag_config("error", foreground="red")
        else:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Xóa log"""
        self.log_text.delete(1.0, tk.END)
        self.log("Log đã được xóa")
    
    def save_log(self):
        """Lưu log ra file"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log(f"💾 Đã lưu log vào {filename}")
    
    def start_processing(self):
        """Bắt đầu xử lý"""
        # Kiểm tra file đầu vào
        input_file = self.input_file_path.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Lỗi", "Vui lòng chọn file đầu vào hợp lệ!")
            self.log("LỖI: Chưa chọn file đầu vào hoặc file không tồn tại", is_error=True)
            return
        
        # Kiểm tra thư mục đích
        output_folder = self.output_folder_path.get()
        if not os.path.exists(output_folder):
            messagebox.showerror("Lỗi", "Thư mục đích không tồn tại!\nVui lòng chọn thư mục hợp lệ.")
            self.log(f"LỖI: Thư mục đích không tồn tại: {output_folder}", is_error=True)
            return
        
        # Kiểm tra quyền ghi
        try:
            test_file = os.path.join(output_folder, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except:
            messagebox.showerror("Lỗi", f"Không có quyền ghi vào thư mục:\n{output_folder}")
            self.log(f"LỖI: Không có quyền ghi vào thư mục: {output_folder}", is_error=True)
            return
        
        # Kiểm tra file xử lý
        if self.selected_mode.get() == "1":
            if not os.path.exists("audio_to_text.py"):
                messagebox.showerror("Lỗi", "Không tìm thấy file audio_to_text.py!")
                self.log("LỖI: Không tìm thấy file audio_to_text.py", is_error=True)
                return
        else:
            if not os.path.exists("text_to_video.py"):
                messagebox.showerror("Lỗi", "Không tìm thấy file text_to_video.py!")
                self.log("LỖI: Không tìm thấy file text_to_video.py", is_error=True)
                return
        
        # Vô hiệu hóa nút xử lý
        self.process_button.config(state='disabled', text="⏳ ĐANG XỬ LÝ...")
        self.progress.start(10)
        
        # Chạy xử lý trong thread riêng
        thread = threading.Thread(target=self.process, daemon=True)
        thread.start()
    
    def process(self):
        """Xử lý theo mode đã chọn"""
        try:
            if self.selected_mode.get() == "1":
                self.process_video_to_text()
            else:
                self.process_text_to_video()
        except Exception as e:
            error_msg = f"Lỗi không xác định: {str(e)}\n{traceback.format_exc()}"
            self.log(error_msg, is_error=True)
            messagebox.showerror("Lỗi nghiêm trọng", f"Đã xảy ra lỗi:\n{str(e)}")
        finally:
            self.root.after(0, self.finish_processing)
    
    def process_video_to_text(self):
        """Xử lý video -> text"""
        self.log("="*50)
        self.log("🎬 BẮT ĐẦU CHUYỂN ĐỔI VIDEO → TEXT")
        self.log("="*50)
        
        input_file = self.input_file_path.get()
        output_folder = self.output_folder_path.get()
        output_filename = self.output_text_name.get().strip()
        if not output_filename:
            output_filename = "text"
        output_file = os.path.join(output_folder, f"{output_filename}.txt")
        
        lang_value = self.language.get().split()[0]
        
        self.log(f"📹 File nguồn: {input_file}")
        self.log(f"📁 Thư mục đích: {output_folder}")
        self.log(f"📄 File đích: {output_file}")
        self.log(f"🌐 Ngôn ngữ: {self.language.get()}")
        
        # Tạo script tạm
        script_content = f'''import sys
import os
import traceback
import io

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')
    except:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from audio_to_text import AudioToTextConverter
    
    converter = AudioToTextConverter()
    success = converter.process_video(r"{input_file}", r"{output_file}", "{lang_value}")
    
    if not success:
        print("ERROR: Quá trình xử lý thất bại")
        sys.exit(1)
    else:
        print("SUCCESS: Xử lý thành công")
        sys.exit(0)
        
except ImportError as e:
    print(f"ERROR: Không thể import module audio_to_text - {{e}}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {{str(e)}}")
    traceback.print_exc()
    sys.exit(1)
'''
        
        temp_script = "temp_convert.py"
        try:
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            self.log("🔄 Đang xử lý...")
            
            result = subprocess.run([sys.executable, temp_script], 
                                  capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore', timeout=3600)
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if "ERROR" in line:
                            self.log(line, is_error=True)
                        elif "SUCCESS" in line:
                            self.log("✅ " + line)
                        else:
                            self.log(f"   {line}")
            
            if result.returncode == 0:
                self.log("✅ Chuyển đổi thành công!")
                self.log(f"📄 Kết quả: {output_file}")
                
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    self.log(f"📊 Tổng số ký tự: {len(content)}")
                    messagebox.showinfo("Thành công", f"Chuyển đổi hoàn tất!\n\nFile text đã lưu tại:\n{output_file}\n\nTổng số ký tự: {len(content)}")
                else:
                    self.log("⚠️ Không tìm thấy file output!", is_error=True)
            else:
                error_msg = result.stderr if result.stderr else "Không có chi tiết"
                self.log("❌ CHUYỂN ĐỔI THẤT BẠI!", is_error=True)
                self.log(f"Lỗi: {error_msg[:500]}", is_error=True)
                messagebox.showerror("Lỗi", f"Chuyển đổi thất bại!\n{error_msg[:300]}")
                
        except subprocess.TimeoutExpired:
            self.log("❌ Lỗi timeout!", is_error=True)
            messagebox.showerror("Lỗi", "Xử lý quá lâu (>1 giờ)!")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", is_error=True)
            messagebox.showerror("Lỗi", str(e))
        finally:
            if os.path.exists(temp_script):
                try:
                    os.remove(temp_script)
                except:
                    pass
    
    def process_text_to_video(self):
        """Xử lý text -> video"""
        self.log("="*50)
        self.log("🎬 BẮT ĐẦU CHUYỂN ĐỔI TEXT → VIDEO")
        self.log("="*50)
        
        input_file = self.input_file_path.get()
        output_folder = self.output_folder_path.get()
        output_filename = self.output_video_name.get().strip()
        if not output_filename:
            output_filename = "output_video"
        
        # Thêm hậu tố cho chế độ gõ chữ
        if self.video_mode.get() == "2":
            output_file = os.path.join(output_folder, f"{output_filename}_typing.mp4")
        else:
            output_file = os.path.join(output_folder, f"{output_filename}.mp4")
        
        # Kiểm tra file text
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
                if not content:
                    self.log("❌ File text rỗng!", is_error=True)
                    messagebox.showerror("Lỗi", "File text không có nội dung!")
                    return
        except Exception as e:
            self.log(f"❌ Lỗi đọc file: {e}", is_error=True)
            messagebox.showerror("Lỗi", f"Không thể đọc file text!\n{e}")
            return
        
        self.log(f"📄 File nguồn: {input_file}")
        self.log(f"📁 Thư mục đích: {output_folder}")
        self.log(f"🎥 File đích: {output_file}")
        self.log(f"📊 Số ký tự: {len(content)}")
        self.log(f"🎨 Chế độ: {'Gõ chữ' if self.video_mode.get() == '2' else 'Toàn câu'}")
        self.log(f"🔤 Cỡ chữ: {self.font_size.get()}")
        self.log(f"📐 Kích thước: {self.video_width.get()}x{self.video_height.get()}")
        
        # Tạo script tạm
        script_content = f'''import sys
import os
import traceback
import io

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')
    except:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from text_to_video import TextToVideoCreator
    
    creator = TextToVideoCreator(r"{input_file}", ({self.video_width.get()}, {self.video_height.get()}))
    
    if not creator.read_and_split_sentences():
        print("ERROR: Không thể đọc file text")
        sys.exit(1)
    
    if len(creator.sentences) == 0:
        print("ERROR: Không có câu nào")
        sys.exit(1)
    
    print(f"INFO: Tìm thấy {{len(creator.sentences)}} câu")
    
    if {self.video_mode.get()} == 2:
        success = creator.create_video_with_typing_effect(r"{output_file}", {self.font_size.get()})
    else:
        success = creator.create_video_basic(r"{output_file}", {self.font_size.get()})
    
    if success:
        print("SUCCESS: Tạo video thành công")
        sys.exit(0)
    else:
        print("ERROR: Tạo video thất bại")
        sys.exit(1)
        
except ImportError as e:
    print(f"ERROR: Import error - {{e}}")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {{str(e)}}")
    traceback.print_exc()
    sys.exit(1)
'''
        
        temp_script = "temp_create_video.py"
        try:
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            self.log("🔄 Đang tạo video...")
            
            result = subprocess.run([sys.executable, temp_script], 
                                  capture_output=True, text=True, 
                                  encoding='utf-8', errors='ignore', timeout=1800)
            
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        if "ERROR" in line:
                            self.log(line, is_error=True)
                        elif "SUCCESS" in line:
                            self.log("✅ " + line)
                        elif "INFO" in line:
                            self.log(f"ℹ️ {line}")
                        else:
                            self.log(f"   {line}")
            
            if result.returncode == 0:
                self.log("✅ Tạo video thành công!")
                if os.path.exists(output_file):
                    size = os.path.getsize(output_file) / (1024*1024)
                    self.log(f"📊 Kích thước: {size:.2f} MB")
                    messagebox.showinfo("Thành công", f"Tạo video hoàn tất!\n\nVideo đã lưu tại:\n{output_file}\n\nKích thước: {size:.2f} MB")
                else:
                    self.log("⚠️ Không tìm thấy file output!", is_error=True)
            else:
                error_msg = result.stderr if result.stderr else "Không có chi tiết"
                self.log("❌ TẠO VIDEO THẤT BẠI!", is_error=True)
                self.log(f"Lỗi: {error_msg[:500]}", is_error=True)
                messagebox.showerror("Lỗi", f"Tạo video thất bại!\n{error_msg[:300]}")
                
        except subprocess.TimeoutExpired:
            self.log("❌ Lỗi timeout!", is_error=True)
            messagebox.showerror("Lỗi", "Xử lý quá lâu (>30 phút)!")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", is_error=True)
            messagebox.showerror("Lỗi", str(e))
        finally:
            if os.path.exists(temp_script):
                try:
                    os.remove(temp_script)
                except:
                    pass
    
    def finish_processing(self):
        """Kết thúc xử lý"""
        self.progress.stop()
        self.process_button.config(state='normal', text="▶ BẮT ĐẦU XỬ LÝ")
        self.log("="*50)
        self.log("✨ XỬ LÝ HOÀN TẤT!")
        self.log("="*50)

def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()