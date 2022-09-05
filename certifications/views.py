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


def generate_cert_pdf(request,cert_no,as_IObytes=False):
    try:
        cert = Certificate.objects.get(cert_no=cert_no)
    except Certificate.DoesNotExist:
        raise Http404("Certificate does not exist")

    QRs = []
    qr = qrcode.QRCode(                  
        box_size=10,
        border=1,
    )
    qr.add_data(cert.issuer.url.strip("/")+'?cert_no='+cert.cert_no)

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

    # p.drawCentredString(210, 310, cert.course_en)
    # p.drawCentredString(600, 310,  arabify(cert.course_ar))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    if cert.image:
        p.drawImage(cert.image.name,170, 430, width=60, height=100)

    
    p.setFont('Almarai-Bold',18,leading=None)
    if len(cert.issuer.name_ar.split()) > 4:
        if len(cert.issuer.name_ar.split()) > 8:
            p.setFont('Almarai-Bold',14,leading=None)
        p.drawCentredString(600, 410, arabify(" ".join(cert.issuer.name_ar.split()[:4])))
        p.drawCentredString(600, 390, arabify(" ".join(cert.issuer.name_ar.split()[4:])))
    else:  
        p.drawCentredString(600, 410, arabify(cert.issuer.name_ar))
  
    p.drawCentredString(210, 410, cert.issuer.name_en)

    p.setFont('Almarai-Regular',17,leading=None)
    p.drawCentredString(600, 365, arabify("يشهد أن"))
    p.drawCentredString(210, 370, "Certifies that")

    p.setFont('Almarai-ExtraBold',17,leading=None)
    p.drawCentredString(600, 340, arabify(cert.name_ar))
    p.drawCentredString(210, 340, cert.name_en)

    p.setFont('Almarai-Regular',17,leading=None)
    p.drawCentredString(210, 310, "has completed the "+cert.course_type_en)
    p.drawCentredString(600, 310, arabify('قد إجتاز '+cert.course_type_ar))

    p.setFont('Almarai-Bold',17,leading=None)
    p.drawCentredString(210, 280, cert.course_en)
    p.drawCentredString(600, 280,  arabify(cert.course_ar))


    p.setFont('Almarai-Regular',12,leading=None)

    if cert.course_start:
        p.drawCentredString(210, 250, "from "+ cert.course_start.strftime("%d-%m-%Y") +" to "+cert.course_end.strftime("%d-%m-%Y"))
        p.drawCentredString(600, 250, cert.course_end.strftime("%Y-%m-%d")+' '+arabify('الى')+" "+cert.course_start.strftime("%Y-%m-%d")+' '+arabify('من'))
    else:
        p.drawCentredString(210, 250, "in "+cert.course_end.strftime("%d-%m-%Y"))
        p.drawCentredString(600, 250, cert.course_end.strftime("%Y-%m-%d")+' '+arabify('فى'))

    p.setFont('Almarai-Bold',12,leading=None)
    p.drawCentredString(210, 230, "and has participated actively and postively")
    p.drawCentredString(600, 230, arabify('وكان مشاركاً فيها بايجابية وفاعلية'))

    p.drawImage(cert.issuer.signature.path,50, 80, width=700, height=140)


    p.drawImage('static/generated/'+image_file,240, 80, width=50, height=50)
    p.setFont('Helvetica',9,leading=None)
    p.drawString(50, 70, "Certification no: "+cert.cert_no)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    if as_IObytes:
        return buffer
        
    return FileResponse(buffer, as_attachment=True, filename='Certification_'+cert.cert_no+'.pdf')
