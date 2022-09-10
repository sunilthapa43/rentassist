import decimal as D
import os
from rentassist.settings import BASE_DIR

from apps.ocr.ocr import ocr
from .models import ElectricityUnit
from .serializers import ElectricityUnitSerializer
from rentassist.utils.views import AuthByTokenMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


class ElectricityUnitView(AuthByTokenMixin, GenericAPIView):
    serializer_class = ElectricityUnitSerializer
    parser_classes = [MultiPartParser]
    def post(self, request, *args, **kargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            image = request.data['image']
            obj = ElectricityUnit.objects.get_or_create(user=user, image=image)
            
            path_to_image = 'static/meter-reader-images/' + str(image)
            image_path = os.path.join(BASE_DIR, path_to_image) 
            extracted_digits = ocr(image_path)
            # TODO: filter by created, TimeStamped model
            obj = ElectricityUnit.objects.filter(user=user).first()
            if not extracted_digits:  
                obj.delete()
                
                
            else:
                previous_meter_reading = obj.current_reading
                previous_month_units = obj.current_units

                obj.current_reading = extracted_digits
                obj.current_units = extracted_digits - previous_month_units
                obj.previous_month_reading = previous_meter_reading
                obj.save()
                
            response = {
                "success": True,
                "message": "uploaded successfully",
                "data": serializer.data,
                "digits": extracted_digits
            }
            return Response(response)
        else:
            response = {
                "success": False,
                "message": "Inavalid request"
            }
            return Response(response)
        

# TODO: PREVIOUS MONTH METER READING, THIS MONTH READING,  obj.previous month reading = thisuser current month reading
# current reading = extracted reading 
# send to payment -> total payables =  internet pani batti maintainence nagarpalika fohr etc