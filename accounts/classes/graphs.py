from ..models import *

import random

def call_outcome_data(queryset):

    labels = []
    data = []
    colour = []

    for call in queryset:
        labels.append(call['contact_id__call_outcome'])
        data.append(call['full_count'])
        colour.append("rgba(" +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + ", 0.7)")

    context = {
        "labels": labels,
        "data": data,
        "colour": colour,
    }
    
    return context


def services_data(queryset):

    labels = []
    data = []
    colour = []

    for call in queryset:
        labels.append(call['service_type_id__service_type_name'])
        data.append(call['full_count'])
        colour.append("rgba(" +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + ", 0.7)")

    context = {
        "labels": labels,
        "data": data,
        "colour": colour,
    }
    
    return context


def brands_data(queryset):
    all_brands = Brand.objects.all()

    labels = []
    data = []
    colour = []

    for brand in all_brands:
        labels.append(brand.brand_name)
        data.append(0)
        colour.append("rgba(" +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + "," +
            str(random.randint(75, 220)) + ", 0.7)")

    for call in queryset:
        index = labels.index(call['contact_id__contact_session_id__brand_id__brand_name'])
        data[index] += 1

    context = {
        "labels": labels,
        "data": data,
        "colour": colour,
    }
    
    return context
