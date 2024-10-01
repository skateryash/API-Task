from .models import FEmployee, SEmployee, Job
from .serializer import FEmployeeSerializer, SEmployeeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def add(request):
    try:
        data = request.data['file_data']
        job = Job.objects.create(name=f"JOB_{Job.objects.count() + 1}")

        femployees_to_create = []
        femployees_to_update = []
        semployees_to_create = []
        semployees_to_update = []

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
                    femployee.source = job
                    femployees_to_update.append(femployee)
                else:
                    femployees_to_create.append(FEmployee(
                        id = fserializer.validated_data.get('id'),
                        name = fserializer.validated_data.get('name'),
                        email = fserializer.validated_data.get('email'),
                        mobile = fserializer.validated_data.get('mobile'),
                        department = fserializer.validated_data.get('department'),
                        designation = fserializer.validated_data.get('designation'),
                        source = job
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
                    semployee.source = job
                    semployees_to_update.append(semployee)
                else:
                    semployees_to_create.append(SEmployee(
                        id = sserializer.validated_data.get('id'),
                        name = sserializer.validated_data.get('name'),
                        email = sserializer.validated_data.get('email'),
                        mobile = sserializer.validated_data.get('mobile'),
                        department = sserializer.validated_data.get('department'),
                        salary = sserializer.validated_data.get('salary'),
                        source = job
                        ))
            else:
                return Response({
                    'status': 'Failure',
                    'message': sserializer.errors
                }, status.HTTP_400_BAD_REQUEST)
        
        if femployees_to_create:
            FEmployee.objects.bulk_create(femployees_to_create)
        if femployees_to_update:
            FEmployee.objects.bulk_update(femployees_to_update, ['id', 'name', 'email', 'mobile', 'department', 'designation', 'status', 'source'])

        if semployees_to_create:
            SEmployee.objects.bulk_create(semployees_to_create)
        if semployees_to_update:
            SEmployee.objects.bulk_update(semployees_to_update, ['id', 'name', 'email', 'mobile', 'department', 'salary', 'status', 'source'])

        job.status = 'Success'
        job.save()
        return Response({'status': 'success', 'message': 'Data Operation Successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal Server Error'})
    


@api_view(['GET'])
def get(request):
    jobs = Job.objects.all()

    all_jobs = []

    for job in jobs:
        all_jobs.append({'name': job.name, 'status': job.status})

    return Response({'data': all_jobs})
