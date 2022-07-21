from django.shortcuts import render
from django.utils import timezone
from certifications.models import Certificate
from django.http import HttpResponse, HttpResponseNotFound

import qrcode
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
###########reportlab Arabic support##########################
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
###################################################


def verify(request,cert_no):
    cert = Certificate.objects.filter(cert_no=cert_no)
    if cert.count() == 1:
        context = {'cert':cert[0]}
        return render(request,'certificate.html',context)
    else:
        return HttpResponseNotFound('<h1>Invalid certificate</h1>')

def arabify(arabic_text):
    #reshape the text       
    configuration = {
        'use_unshaped_instead_of_isolated': True,
    }
    reshaper = ArabicReshaper(configuration=configuration)
    rehaped_text = reshaper.reshape(arabic_text)
    bidi_text = get_display(rehaped_text)
    return bidi_text


def generate_cert_pdf(request,cert_no):
    try:
        cert = Certificate.objects.get(cert_no=cert_no)
    except Certificate.DoesNotExist:
        raise Http404("Certificate does not exist")

    url = request.GET.get('url')

    QRs = []
    qr = qrcode.QRCode(                  
        box_size=10,
        border=1,
    )
    qr.add_data(url)

    # QR in color are not compatible with all readers
    # img = qr.make_image(fill_color="white", back_color=(95, 207, 128))
    img = qr.make_image()
    image_file = 'QRcode_'+str(cert_no)+".png"
    # add accessible img URL
    QRs.append(image_file)    
    # Saving as an image file
    # print(os.getcwd())
    img.save('static/generated/'+image_file)


    ##########################reportlab Arabic support################

    #### add custome font ####
    pdfmetrics.registerFont(TTFont('Almarai-Regular', 'static/Almarai-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Almarai-Light', 'static/Almarai-Light.ttf'))
    pdfmetrics.registerFont(TTFont('Almarai-ExtraBold', 'static/Almarai-ExtraBold.ttf'))
    pdfmetrics.registerFont(TTFont('Almarai-Bold', 'static/Almarai-Bold.ttf'))


    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(letter))

    p.setTitle("Certification_"+cert.cert_no)


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont('Almarai-Bold',25,leading=None)
    p.drawCentredString(620, 500, arabify(cert.issuer_ar))
    p.drawCentredString(210, 500, cert.issuer_en)

    p.setFont('Almarai-Regular',24,leading=None)
    p.drawCentredString(620, 450, arabify("يشهد أن"))
    p.drawCentredString(210, 450, "Certifies that")

    p.setFont('Almarai-ExtraBold',20,leading=None)
    p.drawCentredString(620, 395, arabify(cert.name_ar))
    p.drawCentredString(210, 395, cert.name_en)

    p.setFont('Almarai-Regular',24,leading=None)
    p.drawCentredString(210, 350, "has completed the following course")
    p.drawCentredString(620, 350, arabify('قد إجتاز الدورة'))

    p.setFont('Almarai-Bold',20,leading=None)
    p.drawCentredString(210, 310, cert.course_en)
    p.drawCentredString(620, 310,  arabify(cert.course_ar))


    p.setFont('Almarai-Regular',20,leading=None)
    p.drawCentredString(210, 280, "in "+cert.course_end.strftime("%Y-%m-%d"))
    p.drawCentredString(620, 280, cert.course_end.strftime("%Y-%m-%d")+' '+arabify('في'))

    p.setFont('Almarai-Bold',15,leading=None)
    p.drawCentredString(210, 250, "and has participated actively and postively")
    p.drawCentredString(620, 250, arabify('وكان مشاركاً فيها بايجابية وفاعلية'))

    p.drawImage('static/generated/'+image_file,390, 50, width=50, height=50)
    p.setFont('Helvetica',10,leading=None)
    p.drawString(50, 40, "Certification no: "+cert.cert_no)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='Certification_'+cert.cert_no+'.pdf')
