CBES - Customizable Bulk Email Sender
CBES (Customizable Bulk Email Sender) is a Python tool designed to simplify the process of sending emails directly from your desktop. It is particularly useful for job seekers who want to reach out to potential employers or contacts without relying on web-based email services.

Audience
CBES is ideal for job seekers who:

Want to send personalized emails directly from their desktop.
Need to send emails to a single recipient or a list of recipients.
Seek a user-friendly tool for composing and sending emails efficiently.
Functionality
CBES offers the following key features:

Graphical User Interface (GUI):

CBES provides an intuitive GUI built with Tkinter, making it easy for users to interact with the tool without the need for extensive technical knowledge.
Email Composition:

Users can compose emails with a subject line, body text, and optional PDF attachment directly within the application.
Recipient Options:

CBES allows users to send emails to a single recipient or multiple recipients.
Single recipients can be specified by entering their email address, while multiple recipients can be imported from a text file.
Attachment Support:

Users can attach PDF files to their emails, enhancing the versatility of the emails being sent.
Credential Management:

CBES securely stores Gmail credentials, ensuring that users can send emails directly from their Gmail account without the need for manual login each time.
Validation and Error Handling:

The tool performs validation on input fields to ensure that required fields are filled out and that email addresses are in the correct format.
Error messages are displayed to users if any validation errors occur or if there are issues with sending the email.
Progress Indicator:

CBES includes a progress bar that provides users with feedback on the status of their email delivery, ensuring transparency throughout the sending process.
Installation and Usage
Installation
Clone the Repository:

git clone [https://github.com/yourusername/cbes.git](https://github.com/AliRajab12/cbes.git)

Navigate to the Directory:
cd cbes
Install Dependencies:
pip install -r requirements.txt
Configuration
Usage
Run the Script:
python cbes.py
Input Gmail Credentials (First Time Only):

Upon running the script for the first time, you will be prompted to input your Gmail credentials through a secure initial form.
Enter your Gmail email address and password and click "Save" to proceed.
Compose and Send Emails:

Once your credentials are saved, the main application window will appear.
Use the GUI interface to compose your email, specify recipients, and customize the message as desired.
Click the "Send Email" button to send your email(s).
Optional: Change Credentials:

If you need to change your Gmail credentials at any time, you can do so by selecting "Change Credentials" from the "Credentials" menu in the application.
License
This project is licensed under the Custom License - CBES Tool.
