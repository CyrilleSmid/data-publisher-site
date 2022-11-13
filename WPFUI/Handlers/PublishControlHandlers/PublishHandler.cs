using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using iText.Kernel.Pdf;
using iText.Kernel.Pdf.Canvas.Parser.Listener;
using iText.Kernel.Pdf.Canvas.Parser;
using System.Windows.Documents;

namespace WPFUI.Handlers.PublishControlHandlers
{
    public class PublishHandler
    {
        public PublishHandler()
        {

        }

        public void Upload(PdfDocument pdfDoc)
        {
            string docContent = ExtractTextFromPDF(pdfDoc);
        }

        private string ExtractTextFromPDF(PdfDocument pdfDoc)
        {
            string docContent = "";
            for (int page = 1; page <= pdfDoc.GetNumberOfPages(); page++)
            {
                ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
                docContent += PdfTextExtractor.GetTextFromPage(pdfDoc.GetPage(page), strategy);
            }
            return docContent;
        }

        //private static void ExtractTextFromPDF(string filePath)
        //{
        //    PdfReader pdfReader = new PdfReader(filePath);
        //    PdfDocument pdfDoc = new PdfDocument(pdfReader);
        //    for (int page = 1; page <= pdfDoc.GetNumberOfPages(); page++)
        //    {
        //        ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
        //        string pageContent = PdfTextExtractor.GetTextFromPage(pdfDoc.GetPage(page), strategy);
        //    }
        //    pdfDoc.Close();
        //    pdfReader.Close();
        //}
    }
}
