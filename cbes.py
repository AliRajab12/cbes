import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

# Create the main application window
root = tk.Tk()
root.title("CBES - Customizable Bulk Email Sender")


# Disable the main window initially
root.withdraw()

# Load environment variables from .env file
load_dotenv()

# Function to save credentials to .env file
def save_credentials(email, password):
    with open('.env', 'w') as f:
        f.write(f'GMAIL_USER=\'{email}\'\n')
        f.write(f'GMAIL_PASSWORD=\'{password}\'')

# Function to handle saving credentials from initial form
def save_initial_credentials(initial_window, email_entry, password_entry):
    email = email_entry.get()
    password = password_entry.get()
    if email and password:
        save_credentials(email, password)
        initial_window.destroy()  # Close the initial window after saving
        # Re-enable the main window
        root.deiconify()
        global gmail_user, gmail_password
        gmail_user = email
        gmail_password = password
    else:
        messagebox.showerror("Error", "Both email and password are required.")

# Function to open initial credential entry form
def open_initial_form():
    initial_window = tk.Toplevel(root)
    initial_window.title("Enter Gmail Credentials")

    email_label = ttk.Label(initial_window, text="Email:")
    email_label.grid(row=0, column=0, padx=10, pady=5)
    email_entry = ttk.Entry(initial_window)
    email_entry.grid(row=0, column=1, padx=10, pady=5)

    password_label = ttk.Label(initial_window, text="Password:")
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry = ttk.Entry(initial_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    save_button = ttk.Button(initial_window, text="Save", command=lambda: save_initial_credentials(initial_window, email_entry, password_entry))
    save_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Make the initial window modal
    initial_window.grab_set()
    initial_window.protocol("WM_DELETE_WINDOW", lambda: initial_window.destroy())  # Close only the credentials form

    # Wait for the Toplevel window to close before allowing interaction with root window
    root.wait_window(initial_window)
    # Reload environment variables after the initial form is closed
    load_dotenv()

# Check if GMAIL_USER and GMAIL_PASSWORD are already set in .env file
if not (os.getenv('GMAIL_USER') and os.getenv('GMAIL_PASSWORD')):
    open_initial_form()  # If not set, open initial form for user to enter credentials
else:
    # Re-enable the main window if credentials are already set
    root.deiconify()

# Email credentials
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

# Add a menu bar to the main window
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
credentials_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Credentials", menu=credentials_menu)
credentials_menu.add_command(label="Change Credentials", command=open_initial_form)

# Define variables for the GUI fields
subject_var = tk.StringVar()
body_var = tk.StringVar()
to_email_var = tk.StringVar()
multiple_emails_var = tk.StringVar()
pdf_path_var = tk.StringVar()
recipient_option_var = tk.StringVar(value="single")

# Function to select the PDF file
def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_path_var.set(pdf_path)

# Function to select a text file with email addresses
def select_email_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            email_list = file.read()
        email_text_area.config(state=tk.NORMAL)
        email_text_area.delete(1.0, tk.END)
        email_text_area.insert(tk.END, email_list)
        multiple_emails_var.set(email_list.replace('\n', ','))
        # email_text_area.config(state=tk.DISABLED)  # Make the text area read-only

# Function to validate input fields
def validate_fields():
    if recipient_option_var.get() == "single":
        recipient_email = to_email_var.get()
        if not recipient_email:
            messagebox.showerror("Error", "Recipient email is required.")
            return False
        if not validate_email(recipient_email):
            messagebox.showerror("Error", "Please enter a valid email address for the recipient.")
            return False
    else:
        if not multiple_emails_var.get():
            messagebox.showerror("Error", "At least one recipient email is required.")
            return False
    if not subject_var.get():
        messagebox.showerror("Error", "Subject is required.")
        return False
    if not body_var.get():
        messagebox.showerror("Error", "Email body is required.")
        return False
    if not (gmail_user and gmail_password):
        messagebox.showerror("Error", "Gmail credentials are not set.")
    return True

# Function to validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to send email
def send_email():
    if not validate_fields():
        return

    # Start the progress bar
    progress_bar.grid(row=10, column=0, columnspan=3, pady=10)
    progress_bar.start()

    def send():
        recipients = []
        if recipient_option_var.get() == "single":
            recipients.append(to_email_var.get())
        else:
            recipients.extend(multiple_emails_var.get().split(','))

        subject = subject_var.get()
        body = body_var.get()
        pdf_path = pdf_path_var.get()

        msg = MIMEMultipart('alternative')
        msg['From'] = gmail_user
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if pdf_path:
            try:
                with open(pdf_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(pdf_path)}"')
                msg.attach(part)
            except Exception as e:
                print(f"Error reading PDF file: {e}")

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            for recipient in recipients:
                msg['To'] = recipient
                server.sendmail(gmail_user, recipient, text)
            server.quit()
            root.after(0, lambda: messagebox.showinfo("Success", f"Email sent successfully to {', '.join(recipients)}"))
        except Exception as e:
                root.after(0, lambda error=e: messagebox.showerror("Error", f"Failed to send email: {str(error)}"))

        finally:
            # Stop the progress bar in the main thread
            root.after(0, lambda: progress_bar.stop())
            root.after(0, lambda: progress_bar.grid_remove())

    # Run the email sending process in a separate thread
    threading.Thread(target=send).start()


# Function to toggle recipient input fields based on selection
def toggle_recipient_fields():
    if recipient_option_var.get() == "single":
        to_email_entry.grid(row=1, column=1, padx=10, pady=5)
        email_text_area.grid_remove()
        select_file_button.grid_remove()
        # read_only_label.grid_remove()
    else:
        to_email_entry.grid_remove()
        email_text_area.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
        select_file_button.grid(row=1, column=3, padx=10, pady=5)
        # read_only_label.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# Function to clear all input fields
def clear_fields():
    subject_var.set("")
    body_var.set("")
    to_email_var.set("")
    multiple_emails_var.set("")
    pdf_path_var.set("")
    email_text_area.config(state=tk.NORMAL)
    email_text_area.delete(1.0, tk.END)
    email_text_area.config(state=tk.NORMAL)
    toggle_recipient_fields()

# Function to update multiple_emails_var when the text area content changes
def update_multiple_emails_var(event):
    multiple_emails_var.set(email_text_area.get("1.0", tk.END).strip().replace('\n', ','))

# Create the GUI elements
ttk.Radiobutton(root, text="Single", variable=recipient_option_var, value="single", command=toggle_recipient_fields).grid(row=0, column=0, padx=5, pady=5)
ttk.Radiobutton(root, text="Multiple", variable=recipient_option_var, value="multiple", command=toggle_recipient_fields).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(root, text="Recipient:").grid(row=1, column=0, padx=10, pady=5)
to_email_entry = ttk.Entry(root, textvariable=to_email_var)
to_email_entry.grid(row=1, column=1, padx=10, pady=5)

email_text_area = tk.Text(root, height=5, width=40)
email_text_area.bind("<KeyRelease>", update_multiple_emails_var)  # Bind key release event to update variable

select_file_button = ttk.Button(root, text="Select File (.txt)", command=select_email_file)

# read_only_label = ttk.Label(root, text="Email addresses are read-only and cannot be edited.", foreground="red")

ttk.Label(root, text="Subject:").grid(row=3, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=subject_var).grid(row=3, column=1, columnspan=2, padx=10, pady=5)

ttk.Label(root, text="Body:").grid(row=4, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=body_var).grid(row=4, column=1, columnspan=2, padx=10, pady=5)

ttk.Label(root, text="PDF Attachment:").grid(row=5, column=0, padx=10, pady=5)
ttk.Entry(root, textvariable=pdf_path_var).grid(row=5, column=1, columnspan=1, padx=10, pady=5)
ttk.Button(root, text="Browse", command=select_pdf).grid(row=5, column=2, padx=10, pady=5)

ttk.Button(root, text="Send Email", command=send_email).grid(row=6, column=0, columnspan=3, pady=10)
ttk.Button(root, text="Clear", command=clear_fields).grid(row=7, column=0, columnspan=3, pady=10)

progress_bar = ttk.Progressbar(root, mode='indeterminate')

# Initially toggle recipient fields based on default selection
toggle_recipient_fields()

root.mainloop()

