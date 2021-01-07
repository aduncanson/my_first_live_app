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
