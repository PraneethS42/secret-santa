import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import textwrap

# Used to store a list of emails to names (removed for privacy)
email_to_name = {'email': 'name'}

# Test emails to check if program works
test_emails = {'email': 'name'}


def scramble_names(mapping: dict[str, str]):
    """
    Return a list of scrambled names, ensuring no one person receives themselves.
    """
    names = list(mapping.values())
    emails = list(mapping.keys())
    output = {}

    while True:
        # Shuffle emails
        random.shuffle(names)

        # Assign each email to a shuffled name
        for i in range(len(names)):
            output[emails[i]] = names[i]

        # Check if every email is mapped to a different person
        flag = False
        for email in output:
            if output[email] == mapping[email]:
                flag = True

        # If it is, then break the loop, otherwise continue iterating
        if not flag:
            break
        output = {}

    return output


def encrypt_name(name: str):
    """
    Encrypt a message using a one-time pad key cryptosystem, making each name 13 characters
    """
    # Create the 13 character key
    name = name.upper()
    key = ""
    for _ in range(12):
        key += chr(random.randint(65, 90))

    # Also make the name 13 characters long
    while len(name) != 12:
        side = random.randint(1, 2)
        if side == 1:
            name = chr(random.randint(65, 90)) + name
        else:
            name = name + chr(random.randint(65, 90))

    # Add them together and round off
    # print(name, key)
    message = ""
    for i in range(12):
        message += chr((ord(name[i])-65 + ord(key[i])-65) % 26 + 65)

    return [key, message]


email_paired = scramble_names(email_to_name)

sender_email = "_"
sender_password = "_"  # 16 letter password from Google
image_path = "an image you want to add to the email"  # can be removed
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, sender_password)

    # Now, send every email
    for email, name in email_paired.items():
        pair = encrypt_name(email_paired[email])
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = "enter subject line"

        body = textwrap.dedent(f"""
            enter email message
            """)

        message.attach(MIMEText(body, "plain"))

        # Attach the image
        with open(image_path, "rb") as img_file:
            img = MIMEImage(img_file.read())
            img.add_header("Content-Disposition", f"attachment; filename={image_path.split('/')[-1]}")
            message.attach(img)

        # Send the email
        server.send_message(message)
        print(f"Email sent to {name} ({email})!")
