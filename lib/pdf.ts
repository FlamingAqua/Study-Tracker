'use client'

import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

export async function exportElementToPdf(elementId: string, fileName = 'mbbs-study-progress.pdf') {
  const element = document.getElementById(elementId)
  if (!element) throw new Error('PDF source element not found')

  const canvas = await html2canvas(element, { scale: 2, useCORS: true })
  const imgData = canvas.toDataURL('image/png')
  const pdf = new jsPDF('p', 'mm', 'a4')
  const pageWidth = pdf.internal.pageSize.getWidth()
  const pageHeight = (canvas.height * pageWidth) / canvas.width

  pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, pageHeight)
  pdf.save(fileName)
}
