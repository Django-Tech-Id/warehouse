import pdfkit
from django.http import HttpResponse
from django.template import loader
from uuid import UUID

class to():
    def rupiah(value):
        str_value = str(value)
        separate_decimal = str_value.split(".")
        after_decimal = separate_decimal[0]
        before_decimal = separate_decimal[1]
        reverse = after_decimal[::-1]
        temp_reverse_value = ""
        for index, val in enumerate(reverse):
            if (index + 1) % 3 == 0 and index + 1 != len(reverse):
                temp_reverse_value = temp_reverse_value + val + "."
            else:
                temp_reverse_value = temp_reverse_value + val
        temp_result = temp_reverse_value[::-1]
        return "Rp " + temp_result + "," + before_decimal

    def pdf(request, template, context):
        html = loader.render_to_string(template, context)
        output= pdfkit.from_string(html, output_path=False)
        response = HttpResponse(content_type="application/pdf")
        response.write(output)
        return response


class validate():
    def uuid(value):
        try:
            val = UUID(value, version=4)
        except ValueError:
            return False
        return True
