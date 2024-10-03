from .models import FEmployee, SEmployee, Job
from .serializer import FEmployeeSerializer, SEmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json

@api_view(['POST'])
def add(request):
    try:
        data = request.data['file_data']
        job = Job.objects.create(name=f"JOB_{Job.objects.count() + 1}")

        femployees_to_create = []
        semployees_to_create = []

        for emp_data in data:
            fserializer = FEmployeeSerializer(data=emp_data)
            if fserializer.is_valid():
                femployee = FEmployee.objects.filter(id=emp_data['id']).first()
                if femployee:
                    femployee.name = fserializer.validated_data.get('name', femployee.name)
                    femployee.email = fserializer.validated_data.get('email', femployee.email)
                    femployee.mobile = fserializer.validated_data.get('mobile', femployee.mobile)
                    femployee.department = fserializer.validated_data.get('department', femployee.department)
                    femployee.designation = fserializer.validated_data.get('designation', femployee.designation)
                    femployee.status = 'Updated'
                    femployee.save()
                    femployee.job.add(job)
                else:
                    femployees_to_create.append(FEmployee(
                        id = fserializer.validated_data.get('id'),
                        name = fserializer.validated_data.get('name'),
                        email = fserializer.validated_data.get('email'),
                        mobile = fserializer.validated_data.get('mobile'),
                        department = fserializer.validated_data.get('department'),
                        designation = fserializer.validated_data.get('designation'),
                    ))
            else:
                return Response({
                    'status': 'Failure',
                    'message': fserializer.errors
                }, status.HTTP_400_BAD_REQUEST)
            
            sserializer = SEmployeeSerializer(data=emp_data)
            if sserializer.is_valid():
                semployee = SEmployee.objects.filter(id=emp_data['id']).first()
                if semployee:
                    semployee.name = sserializer.validated_data.get('name', semployee.name)
                    semployee.email = sserializer.validated_data.get('email', semployee.email)
                    semployee.mobile = sserializer.validated_data.get('mobile', semployee.mobile)
                    semployee.department = sserializer.validated_data.get('department', semployee.department)
                    semployee.salary = sserializer.validated_data.get('salary')
                    semployee.status = 'Updated'
                    semployee.save()
                    semployee.job.add(job)
                else:
                    semployees_to_create.append(SEmployee(
                        id = sserializer.validated_data.get('id'),
                        name = sserializer.validated_data.get('name'),
                        email = sserializer.validated_data.get('email'),
                        mobile = sserializer.validated_data.get('mobile'),
                        department = sserializer.validated_data.get('department'),
                        salary = sserializer.validated_data.get('salary'),
                        ))
            else:
                return Response({
                    'status': 'Failure',
                    'message': sserializer.errors
                }, status.HTTP_400_BAD_REQUEST)
        
        if femployees_to_create:
            FEmployee.objects.bulk_create(femployees_to_create)
        
        if semployees_to_create:
            SEmployee.objects.bulk_create(semployees_to_create)

        for emp in femployees_to_create:
            emp.job.add(job)

        for emp in semployees_to_create:
            emp.job.add(job)
        
        job.status = 'Success'
        job.save()
        return Response({'status': 'success', 'message': 'Data Operation Successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal Server Error'})
    
@api_view(['GET'])
def get(request):
    try:
        params = request.query_params

        if params:
            params = json.loads(params['ids'])
            jobs = Job.objects.filter(id__in=params)
        else:
            jobs = Job.objects.all()

        result = {}

        for job in jobs:
            emp1 = FEmployee.objects.filter(job=job.id)
            emp2 = SEmployee.objects.filter(job=job.id)

            emp1_created_id = [emp.id for emp in emp1 if emp.status == "Created"]
            emp1_updated_id = [emp.id for emp in emp1 if emp.status == "Updated"]

            emp2_created_id = [emp.id for emp in emp2 if emp.status == "Created"]
            emp2_updated_id = [emp.id for emp in emp2 if emp.status == "Updated"]

            result[job.name] = {
                "Status": job.status,
                "Employee1": {
                    "Created Count": len(emp1_created_id),
                    "Created Ids": emp1_created_id,
                    "Updated Count": len(emp1_updated_id),
                    "Updated IDs": emp1_updated_id
                },
                "Employee2": {
                    "Created Count": len(emp2_created_id),
                    "Created Ids": emp2_created_id,
                    "Updated Count": len(emp2_updated_id),
                    "Updated IDs": emp2_updated_id
                },
            }

        return Response(result)
    except:
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal Server Error'})
