import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import threading
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from llama_index.core.agent.workflow import ReActAgent, AgentStream, ToolCallResult
from llama_index.llms.ollama import Ollama
from engines.note_engine import note_engine
from engines.app_engine import app_engine
from engines.document_engine import document_tool
from prompts import react_header
from tracker.tracker import GroqRequestTracker

load_dotenv()

class ModernWindowsAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
        self.tracker = GroqRequestTracker()
        self.chat_history = []
        self.agent = None
        
        self.add_message("assistant", "Welcome to Windows Assistant! I'm initializing in the background. You can start typing, and I'll be ready shortly.")
        
        self.root.after(100, self.initialize_heavy_components)
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Windows Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)    

        try:
            self.root.iconbitmap("icon.ico")   
        except:
            pass
  
        self.root.configure(bg='#1e1e1e')
    
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure modern dark theme styling"""
        self.style = ttk.Style()
        
        self.style.theme_use('clam')
        
        self.colors = {
            'bg_primary': '#1e1e1e',      # Main background (VS Code dark)
            'bg_secondary': '#252526',    # Secondary background (VS Code sidebar)
            'bg_tertiary': '#2d2d30',     # Tertiary background (VS Code input)
            'bg_hover': '#2a2d2e',        # Hover background
            'accent': '#007acc',          # VS Code blue
            'accent_hover': '#1177bb',    # Hover state
            'accent_light': '#4fc3f7',    # Light accent
            'success': '#4caf50',         # Success green
            'warning': '#ffb74d',         # Warning orange
            'danger': '#f48771',          # Error red
            'text_primary': '#cccccc',    # Primary text (VS Code)
            'text_secondary': '#969696',  # Secondary text
            'text_muted': '#6a6a6a',      # Muted text
            'border': '#3e3e42',          # Border color (VS Code)
            'border_light': '#464647',    # Light border
            'chat_user': '#1e3a8a',       # User message (blue theme)
            'chat_assistant': '#065f46',  # Assistant message (green theme)
            'input_bg': '#3c3c3c',        # Input background
            'input_border': '#464647',    # Input border
            'button_bg': '#0e639c',       # Button background
            'button_hover': '#1177bb',    # Button hover
            'scrollbar': '#424242',       # Scrollbar color
            'selection': '#264f78'        # Selection color
        }
        
        self.style.configure('Dark.TFrame',
                           background=self.colors['bg_secondary'],
                           borderwidth=0)
        
        self.style.configure('DarkSidebar.TFrame',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 16, 'normal'),
                           foreground=self.colors['text_primary'],
                           background=self.colors['bg_secondary'])
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 10),
                           foreground=self.colors['text_secondary'],
                           background=self.colors['bg_secondary'])
        
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 9),
                           foreground=self.colors['text_primary'],
                           background=self.colors['button_bg'],
                           borderwidth=1,
                           relief='flat',
                           focuscolor='none',
                           padding=(16, 10))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['button_hover']),
                                ('pressed', self.colors['accent'])],
                      relief=[('pressed', 'flat'),
                             ('active', 'flat')])
        
        self.style.configure('Status.TLabel',
                           font=('Segoe UI', 9),
                           foreground=self.colors['text_secondary'],
                           background=self.colors['bg_secondary'],
                           padding=(8, 4))
        
        self.style.configure('Dark.TLabelframe',
                           background=self.colors['bg_primary'],
                           borderwidth=1,
                           relief='flat',
                           bordercolor=self.colors['border'])
        
        self.style.configure('Dark.TLabelframe.Label',
                           font=('Segoe UI', 11, 'normal'),
                           foreground=self.colors['text_secondary'],
                           background=self.colors['bg_primary'])
        
        self.style.configure('DarkSidebar.TLabelframe',
                           background=self.colors['bg_secondary'],
                           borderwidth=1,
                           relief='flat',
                           bordercolor=self.colors['border'])
        
        self.style.configure('DarkSidebar.TLabelframe.Label',
                           font=('Segoe UI', 11, 'normal'),
                           foreground=self.colors['text_secondary'],
                           background=self.colors['bg_secondary'])
        
    def create_widgets(self):
        """Create and layout all widgets"""
        main_frame = ttk.Frame(self.root, padding="0", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        self.create_sidebar(main_frame)
        
        self.create_chat_area(main_frame)
        
        self.create_status_bar()
        
    def create_sidebar(self, parent):
        """Create the modern Cursor-style sidebar"""
        sidebar_frame = ttk.Labelframe(parent, text="", 
                                     padding="20", style='DarkSidebar.TLabelframe')
        sidebar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          padx=(0, 1), pady=0)
        sidebar_frame.configure(width=300)
        
        title_label = ttk.Label(sidebar_frame, text="Windows Assistant", style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        self.status_frame = ttk.Frame(sidebar_frame, style='DarkSidebar.TFrame')
        self.status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_indicator = tk.Canvas(self.status_frame, width=14, height=14, 
                                        highlightthickness=0, bg=self.colors['bg_primary'])
        self.status_indicator.pack(side=tk.LEFT)
        self.status_indicator.create_oval(2, 2, 12, 12, fill=self.colors['danger'], 
                                        outline=self.colors['border'], width=1)
        
        self.status_label = ttk.Label(self.status_frame, text="Initializing...", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(8, 0))
        
        separator1 = tk.Frame(sidebar_frame, height=1, bg=self.colors['border_light'])
        separator1.pack(fill=tk.X, pady=(0, 20))
        
        capabilities_label = ttk.Label(sidebar_frame, text="Capabilities", 
                                     font=('Segoe UI', 11, 'bold'),
                                     foreground=self.colors['accent'],
                                     background=self.colors['bg_primary'])
        capabilities_label.pack(anchor=tk.W, pady=(0, 8))
        
        capabilities_text = """App Launcher
Open any installed application

Note Taking  
Save notes to your notes file

Document Search
Search through PDF documents

Natural Conversation
Chat naturally with the assistant"""
        
        capabilities_display = tk.Text(sidebar_frame, height=8, wrap=tk.WORD, 
                                     font=('Segoe UI', 9), 
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_secondary'],
                                     relief=tk.FLAT, padx=15, pady=12,
                                     borderwidth=1,
                                     highlightthickness=1,
                                     highlightcolor=self.colors['border_light'],
                                     highlightbackground=self.colors['border'],
                                     insertbackground=self.colors['text_primary'],
                                     selectbackground=self.colors['selection'],
                                     selectforeground=self.colors['text_primary'])
        capabilities_display.insert(tk.END, capabilities_text)
        capabilities_display.configure(state=tk.DISABLED)
        capabilities_display.pack(fill=tk.X, pady=(0, 15))
        
        examples_label = ttk.Label(sidebar_frame, text="Example Commands", 
                                 font=('Segoe UI', 11, 'bold'),
                                 foreground=self.colors['accent'],
                                 background=self.colors['bg_primary'])
        examples_label.pack(anchor=tk.W, pady=(0, 8))
        
        examples_text = """Open Discord
Save note: Meeting at 3 PM
What is machine learning?
Search cloud computing"""
        
        examples_display = tk.Text(sidebar_frame, height=5, wrap=tk.WORD,
                                 font=('Segoe UI', 9), 
                                 bg=self.colors['bg_tertiary'],
                                 fg=self.colors['text_secondary'],
                                 relief=tk.FLAT, padx=15, pady=12,
                                 borderwidth=1,
                                 highlightthickness=1,
                                 highlightcolor=self.colors['border_light'],
                                 highlightbackground=self.colors['border'],
                                 insertbackground=self.colors['text_primary'],
                                 selectbackground=self.colors['selection'],
                                 selectforeground=self.colors['text_primary'])
        examples_display.insert(tk.END, examples_text)
        examples_display.configure(state=tk.DISABLED)
        examples_display.pack(fill=tk.X, pady=(0, 15))
        
        separator2 = tk.Frame(sidebar_frame, height=1, bg=self.colors['border_light'])
        separator2.pack(fill=tk.X, pady=(0, 20))
        
        button_frame = ttk.Frame(sidebar_frame, style='DarkSidebar.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 0))
        
        self.stats_button = ttk.Button(button_frame, text="Show Stats", 
                                     command=self.show_stats, style='Modern.TButton')
        self.stats_button.pack(fill=tk.X, pady=(0, 8))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Chat", 
                                     command=self.clear_chat, style='Modern.TButton')
        self.clear_button.pack(fill=tk.X)
        
    def create_chat_area(self, parent):
        """Create the modern Cursor-style chat area"""
        chat_frame = ttk.LabelFrame(parent, text="", 
                                  padding="20", style='Dark.TLabelframe')
        chat_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(1, 0), pady=0)
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        chat_text_frame = tk.Frame(chat_frame, bg=self.colors['bg_primary'])
        chat_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        chat_text_frame.columnconfigure(0, weight=1)
        chat_text_frame.rowconfigure(0, weight=1)

        self.chat_display = tk.Text(
            chat_text_frame, 
            wrap=tk.WORD, 
            font=('Segoe UI', 11),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            padx=20,
            pady=20,
            state=tk.DISABLED,
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=self.colors['accent_light'],
            highlightbackground=self.colors['border'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['selection'],
            selectforeground=self.colors['text_primary']
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        

        scrollbar = tk.Scrollbar(
            chat_text_frame,
            orient=tk.VERTICAL,
            command=self.chat_display.yview,
            bg=self.colors['bg_primary'],  # Same as background
            troughcolor=self.colors['bg_primary'],  # Same as background
            activebackground=self.colors['bg_primary'],  # Same as background
            highlightbackground=self.colors['bg_primary'],
            highlightcolor=self.colors['bg_primary'],
            borderwidth=0,
            relief=tk.FLAT,
            width=0  
        )
        # Don't grid the scrollbar - keep it hidden but functional
        # scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling instead
        def on_mousewheel(event):
            self.chat_display.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.chat_display.bind("<MouseWheel>", on_mousewheel)
        
        self.chat_display.tag_configure("user_header", 
                                      foreground=self.colors['accent_light'], 
                                      font=('Segoe UI', 10, 'normal'))
        self.chat_display.tag_configure("assistant_header", 
                                      foreground=self.colors['success'], 
                                      font=('Segoe UI', 10, 'normal'))
        self.chat_display.tag_configure("timestamp", 
                                      foreground=self.colors['text_muted'], 
                                      font=('Segoe UI', 9))
        self.chat_display.tag_configure("user_message", 
                                      lmargin1=20, lmargin2=20, rmargin=40,
                                      background=self.colors['chat_user'], 
                                      foreground=self.colors['text_primary'],
                                      relief=tk.FLAT, borderwidth=0,
                                      spacing1=10, spacing3=10)
        self.chat_display.tag_configure("assistant_message", 
                                      lmargin1=20, lmargin2=20, rmargin=40,
                                      background=self.colors['chat_assistant'],
                                      foreground=self.colors['text_primary'],
                                      relief=tk.FLAT, borderwidth=0,
                                      spacing1=10, spacing3=10)
        
        input_container = ttk.Frame(chat_frame, style='Dark.TFrame')
        input_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        input_container.columnconfigure(0, weight=1)
        
        self.input_entry = tk.Text(input_container, height=3, wrap=tk.WORD, 
                                 font=('Segoe UI', 11), relief=tk.FLAT,
                                 bg=self.colors['input_bg'], 
                                 fg=self.colors['text_primary'],
                                 padx=18, pady=15,
                                 borderwidth=1,
                                 highlightthickness=2,
                                 highlightcolor=self.colors['accent_light'],
                                 highlightbackground=self.colors['input_border'],
                                 insertbackground=self.colors['accent_light'],
                                 selectbackground=self.colors['selection'],
                                 selectforeground=self.colors['text_primary'])
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        self.input_entry.bind('<Return>', self.on_enter_key)
        self.input_entry.bind('<Control-Return>', lambda e: self.input_entry.insert(tk.INSERT, '\n'))
        
        self.send_button = ttk.Button(input_container, text="Send", 
                                    command=self.send_message, style='Modern.TButton')
        self.send_button.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.input_entry.configure(state=tk.DISABLED)
        self.send_button.configure(state=tk.DISABLED)
        
    def create_status_bar(self):
        """Create modern Cursor-style status bar at bottom"""
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=32)
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        status_frame.grid_propagate(False)
        
        border_frame = tk.Frame(status_frame, bg=self.colors['border'], height=1)
        border_frame.pack(fill=tk.X)
        
        self.status_bar = tk.Label(status_frame, text="Initializing Windows Assistant...", 
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_secondary'],
                                 font=('Segoe UI', 9),
                                 anchor=tk.W, padx=20, pady=8)
        self.status_bar.pack(fill=tk.BOTH, expand=True)
        
    def initialize_heavy_components(self):
        """Initialize heavy components after UI is shown"""
        self.setup_agent()
        
        self.root.after(2000, self.start_background_pdf_indexing)
        
    def start_background_pdf_indexing(self):
        """Start PDF indexing in background after everything else is ready"""
        def index_pdfs():
            try:
                self.root.after(0, lambda: self.status_bar.configure(
                    text="Indexing documents in background...", fg=self.colors['text_muted']))
                
                from engines.document_engine import get_doc_engine
                get_doc_engine()
                
                self.root.after(0, lambda: self.status_bar.configure(
                    text="Ready - All systems online", fg=self.colors['success']))
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.configure(
                    text="Ready", fg=self.colors['success']))
        
        threading.Thread(target=index_pdfs, daemon=True).start()
        
    def setup_agent(self):
        """Initialize the agent in a separate thread - optimized for speed"""
        def init_agent():
            try:
                self.root.after(0, lambda: self.status_bar.configure(
                    text="Initializing agent...", fg=self.colors['warning']))
                
                
                # from llama_index.llms.groq import Groq
                # llm = Groq(model="groq/compound", api_key=os.getenv("GROQ_API_KEY"))

                llm = Ollama(
                    model="qwen3:4b",
                    request_timeout=15.0,  
                    context_window=4000,  
                )
                
                agent = ReActAgent(
                    tools=[note_engine, app_engine, document_tool],
                    llm=llm,
                    max_iterations=1
                )
                
                agent.update_prompts({"react_header": react_header})
                self.agent = agent
                
                self.root.after(0, self.on_agent_ready)
                
            except Exception as e:
                self.root.after(0, lambda: self.on_agent_error(str(e)))
        
        threading.Thread(target=init_agent, daemon=True).start()
        
    def on_agent_ready(self):
        """Called when agent is successfully initialized"""
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(2, 2, 12, 12, fill=self.colors['success'], 
                                        outline=self.colors['border'], width=1)
        self.status_label.configure(text="Online")
        self.status_bar.configure(text="Ready - Windows Assistant is online and ready to help!",
                                fg=self.colors['success'])
        
        self.input_entry.configure(state=tk.NORMAL)
        self.send_button.configure(state=tk.NORMAL)
        self.input_entry.focus()
        
        self.add_message("assistant", "I'm now fully initialized and ready to help! I can open applications, take notes, search documents, and answer questions. What would you like to do?")
        
    def on_agent_error(self, error):
        """Called when agent initialization fails"""
        self.status_label.configure(text="Offline")
        self.status_bar.configure(text=f"Error: {error}", fg=self.colors['danger'])
        messagebox.showerror("Initialization Error", 
                           f"Failed to initialize agent:\n{error}\n\nPlease make sure Ollama is running with the qwen3:4b model.")
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if event.state & 0x4: 
            return 
        else:
            self.send_message()
            return "break"  
            
    def send_message(self):
        """Send user message and get agent response"""
        message = self.input_entry.get("1.0", tk.END).strip()
        if not message:
            return
            
        if not hasattr(self, 'agent') or self.agent is None:
            self.add_message("assistant", "Please wait, I'm still initializing. Try again in a moment.")
            return
            
        self.input_entry.delete("1.0", tk.END)
        
        self.add_message("user", message)
        
        self.input_entry.configure(state=tk.DISABLED)
        self.send_button.configure(state=tk.DISABLED)
        self.status_bar.configure(text="Thinking...", fg=self.colors['warning'])
        
        def process_message():
            try:
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        raise RuntimeError("Loop is closed")
                except RuntimeError or DeprecationWarning:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                response = loop.run_until_complete(self.get_agent_response(message))
                
                self.root.after(0, lambda: self.on_response_received(response))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_response_error(str(e)))
        
        threading.Thread(target=process_message, daemon=True).start()
        
    async def get_agent_response(self, prompt):
        """Get response from the agent - optimized"""
        try:
            response = await self.prompt_agent(prompt)
            
            try:
                self.tracker.request_times.append(time.time())
                self.tracker._save_today_file()
            except:
                pass 
            
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"
            
    async def prompt_agent(self, prompt):
        """Prompt the agent and return response - optimized for speed"""
        handler = self.agent.run(prompt)
        
        
        response = await handler
        return response
        
    def on_response_received(self, response):
        """Called when agent response is received"""
        self.add_message("assistant", response)
        
         
        self.input_entry.configure(state=tk.NORMAL)
        self.send_button.configure(state=tk.NORMAL)
        self.status_bar.configure(text="Ready", fg=self.colors['success'])
        self.input_entry.focus()
        
    def on_response_error(self, error):
        """Called when there's an error getting response"""
        self.add_message("assistant", f"Sorry, I encountered an error: {error}")
        
         
        self.input_entry.configure(state=tk.NORMAL)
        self.send_button.configure(state=tk.NORMAL)
        self.status_bar.configure(text="Error occurred", fg=self.colors['danger'])
        self.input_entry.focus()
        
    def add_message(self, sender, message):
        """Add a message to the chat display with modern styling"""
        self.chat_display.configure(state=tk.NORMAL)
        
         
        timestamp = datetime.now().strftime("%H:%M")
        
         
        self.chat_display.insert(tk.END, "\n")
        
        if sender == "user":
             
            self.chat_display.insert(tk.END, f"You  •  {timestamp}\n", "user_header")
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
        else:
             
            self.chat_display.insert(tk.END, f"Assistant  •  {timestamp}\n", "assistant_header")
            self.chat_display.insert(tk.END, f"{message}\n", "assistant_message")
        
         
        self.chat_display.insert(tk.END, "\n")
        
         
        self.chat_display.see(tk.END)
        self.chat_display.configure(state=tk.DISABLED)
        
         
        self.chat_history.append({"sender": sender, "message": message, "timestamp": timestamp})
        
    def show_stats(self):
        """Show request statistics"""
        stats = self.tracker.get_stats()
        stats_text = f"""Request Statistics:

Requests per minute: {stats['RPM']}
Requests per day: {stats['RPD']}
Data file: {stats['File']}

Total messages in this session: {len(self.chat_history)}"""
        
        messagebox.showinfo("Statistics", stats_text)
        
    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?"):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.configure(state=tk.DISABLED)
            self.chat_history.clear()
            self.add_message("assistant", "Chat cleared. How can I help you?")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = ModernWindowsAssistant()
    app.run()

if __name__ == "__main__":
    main()
