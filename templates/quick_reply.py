from copy import deepcopy as copy

def add_quick_reply(data, job_title, intent):
    data_with_qr_added = copy(data)
    data_with_qr_added.append({'title':job_title, 'payload':f"/{intent}"})

    return data_with_qr_added