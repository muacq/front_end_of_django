from ..models import *
from ..encoder import *
from ..util import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db.models import Count
from datetime import datetime

from ..response_helper import AceResponseError, ace_response, encode_response
from django.shortcuts import HttpResponse


def test(request):
    return HttpResponse('hello' + request.path.split('/')[-1])
