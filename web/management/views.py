from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from . import mock_dbtools
# Create your views here.
# @login_required
def report(request):

    try:
        data_file = open("mock-data")
        data_list = []
        id = 1
        for line in data_file:
            line_data = line.split(',')
            data = {
                "id": id,
                "img_link": line_data[0].strip(),
                "name": line_data[1].strip(),
                "age": line_data[2].strip(),
                "emo": line_data[3].strip(),
                "checkin": line_data[4].strip(),
                "checkout": line_data[5].strip(),
                "prob": line_data[6].strip(),
            }
            data_list.append(data)
            id += 1

        for data in data_list:
            print(data)
        return render(request, 'report.html', {
            "data_list": data_list,
        })
    except IOError:
        print("cannot open mock-data file.")
    finally:
        data_file.close()


def crud(request, arg, img_pk=0):

    if arg == "save-record-to-database":
        try:
            mock_dbtools.save_record_to_database()
        except Http404:
            return HttpResponse("404 Error.")
        else:
            return HttpResponse("Saved all fake records to database.")
    # elif arg == "delete":
    #     try:
    #         dbtools.delete_img(img_pk)
    #     except Http404:
    #         return HttpResponse('Not found image data has primary key =', img_pk)
    #     else:
    #         return HttpResponse("Deleted image " )
    # elif arg == "delete-all":
    #     try:
    #         dbtools.delete_all()
    #     except :
    #         pass
    #     finally:
    #         return HttpResponse("Delete all successfully.")

    return HttpResponse("Argument is not valid.")
