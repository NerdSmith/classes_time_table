from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render

from excel_parser.parser import excel_parse
from excel_parser.table_parser import parse_t
from .forms import ScheduleInpForm
from pytils.translit import slugify
from django.conf import settings

import os

def transliterate_filename(filename):
    name, ext = os.path.splitext(filename)
    name = slugify(name)
    return f'{name}{ext}'


def upload_file(request):
    if request.method == 'POST':
        form = ScheduleInpForm(request.POST, request.FILES)

        if form.is_valid():
            f = request.FILES["file"]
            fs = FileSystemStorage()
            new_name = transliterate_filename(f.name)
            already_loaded_f = fs.path(new_name)
            if not already_loaded_f:
                filename = fs.save(new_name, f)
            else:
                filename = new_name
            cab_time_t, all_cabs = excel_parse(fs.path(filename), 1)

            return render(request, 'home.html', {'form': form, "cab_time_t": cab_time_t, "cabs": all_cabs})
    else:
        form = ScheduleInpForm()
    return render(request, 'home.html', {'form': form, "cab_time_t": None, "cabs": None})
