
import os
from rentassist.settings import BASE_DIR
from rentassist.utils.response import exception_response
from apps.ocr.ocr import ocr
from .models import ElectricityUnit
from .serializers import ConfigBatti, ElectricityUnitSerializer
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
            try:
                user = request.user
                tenant = serializer.validated_data['tenant']
                image = request.data['image']
                print(image)
                obj = ElectricityUnit.objects.update(tenant=tenant, image=image)
                if obj:
                    print('got obj')
                path_to_image = 'static/meter-reader-images/' + str(image)
                image_path = os.path.join(BASE_DIR, path_to_image) 
                extracted_digits = ocr(image_path)
                print(extracted_digits)
                obj = ElectricityUnit.objects.get(tenant=tenant)
                if not extracted_digits:  
                    response = {
                        "success": False,
                        "message": "Could not run ocr"
                        }
                    return Response(response)
                    
                    
                else:
                    previous_meter_reading = obj.current_reading if obj.current_reading else 0
                    previous_month_units =obj.current_units
                    obj.image = image
                    obj.current_reading = extracted_digits
                    obj.current_units = extracted_digits - previous_meter_reading
                    obj.previous_month_reading = previous_meter_reading
                    obj.previous_month_units = previous_month_units
                    obj.save()
                    payable_units = extracted_digits - previous_meter_reading
    
                    response = {
                        "success": True,
                        "message": "Run OCR Successfully",
                        "data": serializer.data,
                        "total_payable_unit_this_month": payable_units,
                        "this_month_meter_reading": extracted_digits,
                        
                    }
                    return Response(response)
            except Exception as e:
                return exception_response(e, serializer)
        else:
            response = {
                "success": False,
                "message": "Invalid request"
            }
            return Response(response)
        

class ConfigureMeterAPIView(AuthByTokenMixin, GenericAPIView):
    """ At first the owner configures the meter count as when its time to pay rent, the tenant or owner scans the meter.
    So initial reading must be saved at first"""
    serializer_class = ConfigBatti
    def post(self, request, *args, **kwargs):
        serializer = ConfigBatti(data=request.data)
        user = request.user
        
        if not serializer.is_valid():
            response = {
                "success": False,
                "message": "Invalid request"
            }
            return Response(response)
        
        if not user.is_owner:
            response = {
                "success": False,
                "message": "Only Owner can set the initial meter reading"
            }
            return Response(response)
        try:

            tenant = serializer.validated_data['tenant']
            print(tenant)
            image = request.data['image']
            current_reading = serializer.validated_data['current_reading']
    
    
            obj = ElectricityUnit.objects.create(
                tenant=tenant,
                image=image,
                current_reading=current_reading,
                current_units=0,
                previous_month_reading = 0,
                previous_month_units = 0
            )
            obj.save()
    
            response = {
                "success":True,
                "message":"Successfully added meter readings"
            }
            return response(response)
        
        except Exception as e:
            return exception_response(e, serializer)