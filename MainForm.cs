using System;
using System.Drawing;
using System.Windows.Forms;

namespace CardImageGenerator
{
    public class MainForm : Form
    {
        // UI controls
        private PictureBox pictureBox;
        private Button previewButton;
        private Button generateButton;
        private TextBox pinkTextBox;
        private TextBox greenTextBox;
        private TextBox brownTextBox;
        private TextBox blueCircleTextBox;
        private TextBox greenCircleTextBox;
        private TextBox redCircleTextBox;
        private TextBox purpleCircleTextBox;
        private TextBox yellowCircleTextBox;
        private Bitmap lastPreviewImage;

        public MainForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.Text = "Playing Card Generator";
            this.Size = new Size(400, 700);
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;

            int margin = 10;
            int labelWidth = 130;
            int inputWidth = 200;
            int y = margin;


            // Pink text
            this.Controls.Add(new Label { Text = "Pink Rectangle Text:", Left = margin, Top = y, Width = labelWidth });
            pinkTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(pinkTextBox);
            y += 30;

            // Green text
            this.Controls.Add(new Label { Text = "Green Rectangle Text:", Left = margin, Top = y, Width = labelWidth });
            greenTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(greenTextBox);
            y += 30;

            // Brown line text
            this.Controls.Add(new Label { Text = "Brown Line Text:", Left = margin, Top = y, Width = labelWidth });
            brownTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(brownTextBox);
            y += 30;

            // Circles
            this.Controls.Add(new Label { Text = "Blue Circle Number:", Left = margin, Top = y, Width = labelWidth });
            blueCircleTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(blueCircleTextBox);
            y += 30;

            this.Controls.Add(new Label { Text = "Green Circle Number:", Left = margin, Top = y, Width = labelWidth });
            greenCircleTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(greenCircleTextBox);
            y += 30;

            this.Controls.Add(new Label { Text = "Red Circle Number:", Left = margin, Top = y, Width = labelWidth });
            redCircleTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(redCircleTextBox);
            y += 30;

            this.Controls.Add(new Label { Text = "Purple Circle Number:", Left = margin, Top = y, Width = labelWidth });
            purpleCircleTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(purpleCircleTextBox);
            y += 30;

            this.Controls.Add(new Label { Text = "Yellow Circle Number:", Left = margin, Top = y, Width = labelWidth });
            yellowCircleTextBox = new TextBox { Left = margin + labelWidth, Top = y, Width = inputWidth };
            this.Controls.Add(yellowCircleTextBox);
            y += 40;

            // Preview button
            previewButton = new Button { Text = "Preview", Left = margin, Top = y, Width = labelWidth + inputWidth };
            previewButton.Click += PreviewButton_Click;
            this.Controls.Add(previewButton);
            y += 35;

            // Generate button
            generateButton = new Button { Text = "Generate Card Image", Left = margin, Top = y, Width = labelWidth + inputWidth };
            generateButton.Click += GenerateButton_Click;
            this.Controls.Add(generateButton);
            y += 40;

            // Preview area
            pictureBox = new PictureBox { Left = margin, Top = y, Width = 320, Height = 480, BorderStyle = BorderStyle.FixedSingle, SizeMode = PictureBoxSizeMode.Zoom };
            this.Controls.Add(pictureBox);
        }

        private void PreviewButton_Click(object sender, EventArgs e)
        {
            // Generate and display preview image
            Bitmap card = CardDrawer.DrawCard(
                null, // No image
                pinkTextBox.Text,
                greenTextBox.Text,
                brownTextBox.Text,
                blueCircleTextBox.Text,
                greenCircleTextBox.Text,
                redCircleTextBox.Text,
                purpleCircleTextBox.Text,
                yellowCircleTextBox.Text
            );
            lastPreviewImage = card;
            pictureBox.Image = card;
        }

        private void GenerateButton_Click(object sender, EventArgs e)
        {
            if (lastPreviewImage == null)
            {
                MessageBox.Show("Please preview the card first.");
                return;
            }
            using (SaveFileDialog sfd = new SaveFileDialog())
            {
                sfd.Filter = "PNG Image|*.png";
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    lastPreviewImage.Save(sfd.FileName);
                    MessageBox.Show("Card image saved!");
                }
            }
        }
    }
}
