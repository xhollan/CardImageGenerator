using System;
using System.Drawing;

namespace CardImageGenerator
{
    public static class CardDrawer
    {
        public static Bitmap DrawCard(Bitmap picture, string pinkText, string greenText, string brownText,
            string blueCircle, string greenCircle, string redCircle, string purpleCircle, string yellowCircle)
        {
            // Card size
            int width = 320;
            int height = 480;
            Bitmap bmp = new Bitmap(width, height);
            using (Graphics g = Graphics.FromImage(bmp))
            {
                g.Clear(Color.White);

                // Outer card border
                using (Pen borderPen = new Pen(Color.Black, 5))
                {
                    g.DrawRoundedRectangle(borderPen, 2, 2, width - 4, height - 4, 60);
                }

                // Top left (blue number)
                if (!string.IsNullOrWhiteSpace(blueCircle))
                {
                    using (Font font = new Font("Arial", 16, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.DeepSkyBlue))
                    {
                        g.DrawString(blueCircle, font, brush, 30, 30);
                    }
                }
                // Top left (green number)
                if (!string.IsNullOrWhiteSpace(greenCircle))
                {
                    using (Font font = new Font("Arial", 14, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.YellowGreen))
                    {
                        g.DrawString(greenCircle, font, brush, 80, 55);
                    }
                }
                // Top right (red number)
                if (!string.IsNullOrWhiteSpace(redCircle))
                {
                    using (Font font = new Font("Arial", 18, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.Red))
                    {
                        g.DrawString(redCircle, font, brush, width - 60, 30);
                    }
                }
                // Black line (top left)
                using (Pen blackPen = new Pen(Color.Black, 4))
                {
                    g.DrawLine(blackPen, 52, 55, 80, 25);
                }
                // Brown line (top center)
                using (Pen brownPen = new Pen(Color.SaddleBrown, 5))
                {
                    g.DrawLine(brownPen, 100, 45, 220, 45);
                }
                if (!string.IsNullOrWhiteSpace(brownText))
                {
                    using (Font font = new Font("Arial", 10, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.SaddleBrown)) // brown text
                    {
                        g.DrawString(brownText, font, brush, 130, 25);
                    }
                }
                // Pink text (main text, centered in the area where pink rectangle was)
                if (!string.IsNullOrWhiteSpace(pinkText))
                {
                    RectangleF pinkArea = new RectangleF(30, 170, width - 60, 100);
                    using (Font font = new Font("Arial", 16, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.DeepPink)) // pink text
                    {
                        g.DrawString(pinkText, font, brush, pinkArea);
                    }
                }
                // Bottom left (purple number)
                if (!string.IsNullOrWhiteSpace(purpleCircle))
                {
                    using (Font font = new Font("Arial", 18, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.MediumPurple))
                    {
                        g.DrawString(purpleCircle, font, brush, 30, height - 60);
                    }
                }
                // Bottom right (yellow number)
                if (!string.IsNullOrWhiteSpace(yellowCircle))
                {
                    using (Font font = new Font("Arial", 18, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.Gold))
                    {
                        g.DrawString(yellowCircle, font, brush, width - 70, height - 60);
                    }
                }
                // Bottom center (green text)
                if (!string.IsNullOrWhiteSpace(greenText))
                {
                    RectangleF greenArea = new RectangleF(width / 2 - 70, height - 70, 140, 40);
                    using (Font font = new Font("Arial", 12, FontStyle.Bold))
                    using (SolidBrush brush = new SolidBrush(Color.YellowGreen)) // green text
                    {
                        g.DrawString(greenText, font, brush, greenArea);
                    }
                }
            }
            return bmp;
        }

        private static void DrawCircleWithText(Graphics g, int x, int y, int radius, Color color, string text, Color textColor)
        {
            using (Pen pen = new Pen(color, 4))
            {
                g.DrawEllipse(pen, x, y, radius, radius);
            }
            if (!string.IsNullOrWhiteSpace(text))
            {
                using (Font font = new Font("Arial", 14, FontStyle.Bold))
                using (SolidBrush brush = new SolidBrush(textColor))
                {
                    var stringSize = g.MeasureString(text, font);
                    float cx = x + (radius - stringSize.Width) / 2;
                    float cy = y + (radius - stringSize.Height) / 2;
                    g.DrawString(text, font, brush, cx, cy);
                }
            }
        }

        // Overloads for colored text in circles
        private static void DrawCircleWithColoredText(Graphics g, int x, int y, int radius, Color circleColor, string text, Color textColor)
        {
            DrawCircleWithText(g, x, y, radius, circleColor, text, textColor);
        }

        // Extension for rounded rectangle
        private static void DrawRoundedRectangle(this Graphics g, Pen pen, int x, int y, int w, int h, int radius)
        {
            using (System.Drawing.Drawing2D.GraphicsPath path = new System.Drawing.Drawing2D.GraphicsPath())
            {
                path.AddArc(x, y, radius, radius, 180, 90);
                path.AddArc(x + w - radius, y, radius, radius, 270, 90);
                path.AddArc(x + w - radius, y + h - radius, radius, radius, 0, 90);
                path.AddArc(x, y + h - radius, radius, radius, 90, 90);
                path.CloseFigure();
                g.DrawPath(pen, path);
            }
        }
    }
}
