

def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    if not request:
        return False, ""
    request_method = request.split(' ')[0]
    print("Method: {m}".format(m=request_method))
    print("Request Body: {b}".format(b=request))
    if "\n" in request:
        if request_method == "GET" or request_method == "HEAD":
            file_requested = request.split(' ')[1]
            # If get has parameters ('?'), ignore them
            file_requested = file_requested.split('?')[0]
            print("Serving web page [{fp}]".format(fp=file_requested))
            return True, file_requested
        return False, ""



def main():
    validate_http_request("GET /~fdc/sample.html HTTP/1.1\r\n")





if __name__ == "__main__":
# Call the main handler function
    main()