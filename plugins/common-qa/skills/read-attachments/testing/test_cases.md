# Test Cases: read-attachments

## TC-001: Ticket with Image Attachments
- **Input:** Ticket ID with .png and .jpg attachments
- **Expected:** Images processed, visual context extracted

## TC-002: Ticket with Text Attachments
- **Input:** Ticket ID with .md and .json attachments
- **Expected:** Text files decoded, content summarized

## TC-003: Ticket with No Attachments
- **Input:** Ticket ID with no attachments
- **Expected:** Empty summary (total: 0), no error

## TC-004: Ticket with Unsupported Formats Only
- **Input:** Ticket ID with .xlsx and .pdf attachments
- **Expected:** All skipped with warning messages, images/text counts = 0
