
from decimal import Decimal
import os
from rentassist.runocr import run_ocr
from rentassist.settings import BASE_DIR
from rentassist.utils.response import exception_response, prepare_response
from apps.ocr.ocr import ocr
from .models import ElectricityUnit, Ocr
from .serializers import  ElectricityUnitSerializer,  RunOcrSerializer
from rentassist.utils.views import AuthByTokenMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class ElectricityUnitView(AuthByTokenMixin, GenericAPIView):
    serializer_class = ElectricityUnitSerializer
    def post(self, request, *args, **kargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                tenant = serializer.validated_data['tenant']
                current_reading = serializer.validated_data['current_reading']
                obj = ElectricityUnit.objects.filter(tenant=tenant).first()
                previous_meter_reading = obj.current_reading if obj.current_reading else 0
                previous_month_units =obj.current_units
                obj.current_reading = current_reading
                obj.current_units = current_reading - previous_meter_reading
                obj.previous_month_reading = previous_meter_reading
                obj.previous_month_units = previous_month_units
                obj.save()
                payable_units = current_reading - previous_meter_reading

                response = {
                    "success": True,
                    "message": "Updated meter readings successfully",
                    "data": serializer.data,
                    "total_payable_unit_this_month": payable_units,
                    "this_month_meter_reading": current_reading,
                    
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
    serializer_class = ElectricityUnitSerializer
    def post(self, request, *args, **kwargs):
        serializer = ElectricityUnitSerializer(data=request.data)
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
            current_reading = serializer.validated_data['current_reading']
            obj = ElectricityUnit.objects.filter(tenant=tenant)
            if obj.count() == 0:
                obj = ElectricityUnit.objects.create(
                    tenant=tenant,
                    current_reading=current_reading,
                    current_units=0,
                    previous_month_reading = 0,
                    previous_month_units = 0
                )
                obj.save()
            
                response = prepare_response(
                    success=True,
                    message="successfully added electricity details",
                    data= serializer.data
                )
                return Response(response)
            
            elif obj.count() == 1:
                instance =  ElectricityUnit.objects.get(tenant=tenant)  
                instance.tenant=tenant
                instance.current_reading=current_reading
                instance.current_units=0
                instance.previous_month_reading = 0
                instance.previous_month_units = 0  
                instance.save()
        
                response = prepare_response(
                    success=True,
                    message="successfully added electricity details",
                    data= serializer.data
                )
                return Response(response)
        except Exception as e:
            return exception_response(e, serializer)

    
# class RunOcrAPIView(AuthByTokenMixin, GenericAPIView):
#     serializer_class = RunOcrSerializer
#     queryset = Ocr.objects.all()


#     def post(self, request, *args, **kwargs):
#         serializer = RunOcrSerializer(data=request.data)
#         if not serializer.is_valid():
#             response = {
#                 "success": False,
#                 "message": "Invalid request"
#             }
#             return Response(response)
#         if not request.user.is_owner:
#             response =prepare_response(
#                 success=False,
#                 message='you are not allowed to ocr')
#             return Response(response)
#         try: 
#             image = request.data['image']
#             obj = Ocr.objects.create(image=image, image_name=str(image))
#             obj.save()
#             path_to_image = 'static/meter-reader-images/' + str(image)
#             image_path = os.path.join(BASE_DIR, path_to_image) 
#             reading = ocr(image_path)
#             print(type(reading))
#             if reading:
#                 obj = Ocr.objects.filter(image_name=str(image)).first()
#                 obj.extracted_digits = reading
#                 obj.save()
#                 print('comes here')
#                 response = prepare_response(
#                     success=True,
#                     message = "Successfully ran ocr",
#                     data =reading
#                 )
                
#                 return Response(response)

#             else:  
#                 response = {
#                     "success": False,
#                     "message": "Could not run ocr"
#                     }
#                 return Response(response)
#         except Exception as e:
#           return exception_response(e, serializer)


class RunOcrAPIView(AuthByTokenMixin, GenericAPIView):
    serializer_class = RunOcrSerializer
    queryset = Ocr.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = RunOcrSerializer(data=request.data)
        if not serializer.is_valid():
            response = {
                "success": False,
                "message": "Invalid request"
            }
            return Response(response)
        if not request.user.is_owner:
            response =prepare_response(
                success=False,
                message='you are not allowed to ocr')
            return Response(response)
        try: 
            image = request.data['image']
            obj = Ocr.objects.create(image=image, image_name=str(image))
            obj.save()
            path_to_image = 'static/meter-reader-images/' + str(image)
            image_path = os.path.join(BASE_DIR, path_to_image) 
            # reading = ocr(image_path)
            result = run_ocr(filename=image_path)
            
            if result == "":
                obj = Ocr.objects.filter(image_name=str(image)).first()
                reading = obj.extracted_digits
                response = prepare_response(
                    success=True,
                    message='successfully ran ocr',
                    data = reading
                )
                return Response(response)
            else:
               
                data =Decimal(result[:5] + '.' + result[5:])
                obj = Ocr.objects.filter(image_name=str(image)).first()
                obj.extracted_digits = data
                obj.save()
                response = prepare_response(
                    success=True,
                    message = "Successfully ran ocr",
                    data =data
                )
                
                return Response(response)
            
        except Exception as e:
          return exception_response(e, serializer)