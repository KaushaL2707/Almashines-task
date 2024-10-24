from django.shortcuts import render,redirect
from .models import Contects
import vobject
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    data=Contects.objects.all()
    context = {"data": data}
    return render(request,"index.html",context)

def insertData(request):
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        print(name,email,number)
        query = Contects(name=name,number=number, email=email)
        query.save()
        return redirect("/")
    return render(request,"index.html")
        
def updateData(request,id):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')

        edit=Contects.objects.get(id=id)
        edit.name=name
        edit.email=email
        edit.number=number
        edit.save()
        return redirect("/")
    
    d=Contects.objects.get(id=id)
    context = {"d": d}

    return render(request,"edit.html",context)

def deleteData(request,id):
    d=Contects.objects.get(id=id)
    d.delete()
    return redirect("/")

# Contact export to VCF
def export_vcf(request):
    contacts = Contects.objects.all()
    
    output_vcf = vobject.vCard()
    
    for contact in contacts:
        vcard = vobject.vCard()
        vcard.add('version')
        vcard.version.value = '3.0'
        vcard.add('fn').value = contact.name
        vcard.add('tel').value = str(contact.number)
        vcard.add('email').value = contact.email
        output_vcf.add(vcard)
    
    response = HttpResponse(output_vcf.serialize(), content_type='text/x-vcard')
    response['Content-Disposition'] = 'attachment; filename="contacts.vcf"'
    
    return response

# Contact import from VCF
def import_vcf(request):
    if request.method == 'POST':
        vcf_file = request.FILES['vcf_file']
        
        try:
            vcard = vobject.readOne(vcf_file.read())
            for contact in vcard.contents['fn']:
                name = contact.value
                phone = vcard.tel.value if 'tel' in vcard.contents else None
                email = vcard.email.value if 'email' in vcard.contents else None
                
                # Create a new contact or update an existing one
                Contects.objects.create(name=name, number=phone, email=email)
            messages.success(request, "Contacts imported successfully!")
        except Exception as e:
            messages.error(request, f"Error while importing contacts: {str(e)}")
        return redirect('/')
    
    return render(request, 'index.html')

def find_duplicates():
    contacts = Contects.objects.all()
    duplicates = {}
    
    for contact in contacts:
        key = (contact.name, contact.number, contact.email)
        if key in duplicates:
            duplicates[key].append(contact)
        else:
            duplicates[key] = [contact]
    
    # Filter out unique contacts
    return {key: val for key, val in duplicates.items() if len(val) > 1}



def merge_duplicate_contacts(contact_ids):
    # Retrieve contacts to be merged
    contacts = Contects.objects.filter(id__in=contact_ids)

    # Assuming you want to keep the first contact and discard the rest
    master_contact = contacts.first()

    # Merge data as needed; here we'll just keep the first and delete the rest
    for contact in contacts[1:]:
        # Combine data (customize as needed)
        master_contact.email = master_contact.email or contact.email
        master_contact.number = master_contact.number or contact.number
        master_contact.save()

        # Delete the merged contact
        contact.delete()

def merge_contacts(request):
    if request.method == "POST":
        # Get the contact IDs from the form
        contact_ids = request.POST.get('contact_ids').split(',')
        merge_duplicate_contacts(contact_ids)  # Call the merge function
        return redirect('/')  # Redirect to a suitable page after merging

    duplicates = find_duplicates()  # Call the function to find duplicates
    return render(request, 'merge_contacts.html', {'duplicates': duplicates})