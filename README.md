# CardImageGenerator

A simple Windows Forms app to generate custom playing card images based on user input.

## Features
- Upload an image for the card (yellow rectangle area)
- Enter text for pink rectangle (main text)
- Enter text for green rectangle (bottom center)
- Enter numbers for colored circles (top-left, top-right, bottom-left, bottom-right)
- Enter text for brown line (top center)
- Preview and save the generated card image

## How to Run
1. Open the solution in Visual Studio 2022 or newer.
2. Build and run the project.
3. Fill in all fields and upload a picture.
4. Click 'Generate Card Image' to preview and save your custom playing card.

## Dependencies
- .NET 6.0 or newer
- Windows Forms

---

**Project structure:**
- `Program.cs` - Entry point
- `MainForm.cs` - Main UI and logic
- `CardDrawer.cs` - Drawing logic
