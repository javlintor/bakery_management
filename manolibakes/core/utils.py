def get_post_data(request):
    data = str(request.body).replace("'", "").split("&")[1:]
    data = [d.split("=") for d in data]
    return data
